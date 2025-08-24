"""Exceptions for the Alternatives.PE SDK."""

from typing import Any, Optional


class AltPEException(Exception):
    """Base exception for Alternatives.PE SDK."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(AltPEException):
    """Authentication error."""

    pass


class NotFoundError(AltPEException):
    """Resource not found error."""

    pass


class ValidationError(AltPEException):
    """Validation error."""

    def __init__(self, message: str, errors: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.errors = errors


class RateLimitError(AltPEException):
    """Rate limit exceeded error."""

    pass


class ServerError(AltPEException):
    """Server error."""

    pass
