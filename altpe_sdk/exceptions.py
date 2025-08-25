"""Exceptions for the Alternatives.PE SDK."""

from typing import Any


class AltPEError(Exception):
    """Base exception for Alternatives.PE SDK."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(AltPEError):
    """Authentication error."""

    pass


class NotFoundError(AltPEError):
    """Resource not found error."""

    pass


class ValidationError(AltPEError):
    """Validation error."""

    def __init__(self, message: str, errors: dict[str, Any] | None = None):
        super().__init__(message)
        self.errors = errors


class RateLimitError(AltPEError):
    """Rate limit exceeded error."""

    pass


class ServerError(AltPEError):
    """Server error."""

    pass


# Backwards-compat alias
AltPEException = AltPEError
