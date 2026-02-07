"""Custom exceptions for URL Shortener application."""


class CodeAlreadyExistsError(Exception):
    """Raised when trying to create URL with existing code."""

    pass


class CodeNotFoundError(Exception):
    """Raised when code is not found in database."""

    pass


class InvalidURLError(Exception):
    """Raised when URL is invalid."""

    pass


class InvalidCodeError(Exception):
    """Raised when code format is invalid."""

    pass
