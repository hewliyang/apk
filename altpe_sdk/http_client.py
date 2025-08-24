"""HTTP client for the Alternatives.PE SDK."""

import asyncio
import threading
from typing import Any, Optional

import httpx
from httpx import Response

from .config import AltPEConfig
from .exceptions import (
    AltPEException,
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
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        config: Optional[AltPEConfig] = None,
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

        self._token: Optional[str] = None

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
            raise AltPEException(message, response.status_code)


class HTTPClient(BaseHTTPClient):
    """Async HTTP client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        config: Optional[AltPEConfig] = None,
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
                return self._token
            elif response.status_code == 422:
                raise AuthenticationError("Invalid client credentials")
            else:
                raise AuthenticationError(f"Authentication failed: {response.text}")

    async def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
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

        return self._handle_response(response)

    async def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make GET request."""
        return await self._make_request("GET", url, params=params, headers=headers)

    async def post(
        self,
        url: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make POST request."""
        return await self._make_request(
            "POST", url, params=params, data=data, headers=headers
        )

    async def put(
        self,
        url: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make PUT request."""
        return await self._make_request(
            "PUT", url, params=params, data=data, headers=headers
        )

    async def delete(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make DELETE request."""
        return await self._make_request("DELETE", url, params=params, headers=headers)


class SyncHTTPClient(BaseHTTPClient):
    """Sync HTTP client for Alternatives.PE API."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        config: Optional[AltPEConfig] = None,
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
                return self._token
            elif response.status_code == 422:
                raise AuthenticationError("Invalid client credentials")
            else:
                raise AuthenticationError(f"Authentication failed: {response.text}")

    def _make_request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
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

        return self._handle_response(response)

    def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make GET request."""
        return self._make_request("GET", url, params=params, headers=headers)

    def post(
        self,
        url: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make POST request."""
        return self._make_request(
            "POST", url, params=params, data=data, headers=headers
        )

    def put(
        self,
        url: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make PUT request."""
        return self._make_request("PUT", url, params=params, data=data, headers=headers)

    def delete(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Make DELETE request."""
        return self._make_request("DELETE", url, params=params, headers=headers)
