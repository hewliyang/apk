"""HTTP client for the Alternatives.PE SDK."""

import asyncio
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import anyio
import httpx
from httpx import Response

from .config import AltPEConfig
from .exceptions import (
    AltPEError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .models import ErrorResponse, TokenResponse


class BaseHTTPClient:
    """Base HTTP client with shared logic."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        config: AltPEConfig | None = None,
    ):
        """Initialize base HTTP client."""
        self.config = config or AltPEConfig()

        # Override config with explicit parameters
        if client_id:
            self.config.client_id = client_id
        if client_secret:
            self.config.client_secret = client_secret

        if not self.config.client_id or not self.config.client_secret:
            raise ValueError("client_id and client_secret must be provided")

        self._token: str | None = None
        # Optional JSONL logging configuration
        self._log_enabled: bool = bool(getattr(self.config, "log_requests", False))
        self._log_dir: Path = Path(
            getattr(self.config, "log_dir", "altpe-logs")
        ).expanduser()

    def _redact(self, obj: Any) -> Any:
        sensitive = {"authorization", "client_secret", "client_id", "token"}
        if isinstance(obj, dict):
            return {
                k: ("***REDACTED***" if k.lower() in sensitive else self._redact(v))
                for k, v in obj.items()
            }
        if isinstance(obj, list):
            return [self._redact(v) for v in obj]
        return obj

    def _build_log_entry(
        self,
        *,
        method: str,
        url: str,
        params: dict[str, Any] | None,
        data: dict[str, Any] | None,
        headers: dict[str, str] | None,
        response: Response,
    ) -> dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        try:
            response_json: Any | None = response.json()
            response_text: str | None = None
        except Exception:
            response_json = None
            response_text = response.text

        return {
            "timestamp": timestamp,
            "method": method,
            "url": url,
            "request": {
                "params": self._redact(params or {}),
                "data": self._redact(data or {}),
                "headers": self._redact(headers or {}),
            },
            "response": {
                "status_code": response.status_code,
                "json": self._redact(response_json)
                if response_json is not None
                else None,
                "text": response_text if response_json is None else None,
            },
        }

    async def _append_jsonl_async(self, entry: dict[str, Any]) -> None:
        if not self._log_enabled:
            return
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self._log_dir / f"requests-{day}.jsonl"
        try:
            await anyio.Path(self._log_dir).mkdir(parents=True, exist_ok=True)
            async with await anyio.open_file(str(log_file), "a", encoding="utf-8") as f:
                await f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            # Never let logging failures break core functionality
            pass

    def _append_jsonl_sync(self, entry: dict[str, Any]) -> None:
        if not self._log_enabled:
            return
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self._log_dir / f"requests-{day}.jsonl"
        try:
            self._log_dir.mkdir(parents=True, exist_ok=True)
            with log_file.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def _handle_response(self, response: Response) -> Response:
        """Handle HTTP response and raise appropriate exceptions."""
        if response.is_success:
            return response

        try:
            error_data = response.json()
            error_response = ErrorResponse(**error_data)
            message = error_response.message or str(error_response.errors)
        except Exception:
            message = response.text or f"HTTP {response.status_code}"

        if response.status_code == 401:
            # Clear token to force re-authentication
            self._token = None
            raise AuthenticationError(message, response.status_code)
        elif response.status_code == 404:
            raise NotFoundError(message, response.status_code)
        elif response.status_code == 422:
            raise ValidationError(message, response.status_code)
        elif response.status_code == 429:
            raise RateLimitError(message, response.status_code)
        elif response.status_code >= 500:
            raise ServerError(message, response.status_code)
        else:
            raise AltPEError(message, response.status_code)


class HTTPClient(BaseHTTPClient):
    """Async HTTP client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        config: AltPEConfig | None = None,
    ):
        """Initialize async HTTP client."""
        super().__init__(client_id, client_secret, config)
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
        )
        self._token_lock = asyncio.Lock()

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def _get_token(self) -> str:
        """Get or refresh access token."""
        if self._token:
            return self._token

        async with self._token_lock:
            if self._token:
                return self._token

            data = {
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            }

            response = await self._client.post(
                "/api/v2/oauth/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                token_response = TokenResponse(**response.json())
                self._token = token_response.token
                if self._log_enabled:
                    await self._append_jsonl_async(
                        self._build_log_entry(
                            method="POST",
                            url="/api/v2/oauth/token",
                            params=None,
                            data=data,
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            response=response,
                        )
                    )
                return self._token
            elif response.status_code == 422:
                raise AuthenticationError("Invalid client credentials")
            else:
                raise AuthenticationError(f"Authentication failed: {response.text}")

    async def _make_request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        authenticated: bool = True,
    ) -> Response:
        """Make HTTP request."""
        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        if authenticated:
            token = await self._get_token()
            request_headers["Authorization"] = f"Bearer {token}"

        response = await self._client.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=request_headers,
        )
        if self._log_enabled:
            await self._append_jsonl_async(
                self._build_log_entry(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    response=response,
                )
            )
        return self._handle_response(response)

    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make GET request."""
        return await self._make_request("GET", url, params=params, headers=headers)

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make POST request."""
        return await self._make_request(
            "POST", url, params=params, data=data, headers=headers
        )

    async def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make PUT request."""
        return await self._make_request(
            "PUT", url, params=params, data=data, headers=headers
        )

    async def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make DELETE request."""
        return await self._make_request("DELETE", url, params=params, headers=headers)


class SyncHTTPClient(BaseHTTPClient):
    """Sync HTTP client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        config: AltPEConfig | None = None,
    ):
        """Initialize sync HTTP client."""
        super().__init__(client_id, client_secret, config)
        self._client = httpx.Client(
            base_url=self.config.base_url,
            timeout=self.config.timeout,
        )
        self._token_lock = threading.Lock()

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        """Sync context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        self.close()

    def _get_token(self) -> str:
        """Get or refresh access token."""
        if self._token:
            return self._token

        with self._token_lock:
            if self._token:
                return self._token

            data = {
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            }

            response = self._client.post(
                "/api/v2/oauth/token",
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 200:
                token_response = TokenResponse(**response.json())
                self._token = token_response.token
                if self._log_enabled:
                    self._append_jsonl_sync(
                        self._build_log_entry(
                            method="POST",
                            url="/api/v2/oauth/token",
                            params=None,
                            data=data,
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded"
                            },
                            response=response,
                        )
                    )
                return self._token
            elif response.status_code == 422:
                raise AuthenticationError("Invalid client credentials")
            else:
                raise AuthenticationError(f"Authentication failed: {response.text}")

    def _make_request(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        authenticated: bool = True,
    ) -> Response:
        """Make HTTP request."""
        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        if authenticated:
            token = self._get_token()
            request_headers["Authorization"] = f"Bearer {token}"

        response = self._client.request(
            method=method,
            url=url,
            params=params,
            json=data,
            headers=request_headers,
        )
        if self._log_enabled:
            self._append_jsonl_sync(
                self._build_log_entry(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=request_headers,
                    response=response,
                )
            )
        return self._handle_response(response)

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make GET request."""
        return self._make_request("GET", url, params=params, headers=headers)

    def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make POST request."""
        return self._make_request(
            "POST", url, params=params, data=data, headers=headers
        )

    def put(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make PUT request."""
        return self._make_request("PUT", url, params=params, data=data, headers=headers)

    def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Make DELETE request."""
        return self._make_request("DELETE", url, params=params, headers=headers)
