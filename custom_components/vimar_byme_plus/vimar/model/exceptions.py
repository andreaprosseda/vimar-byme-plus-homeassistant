"""Exceptions for Vimar integration."""


class CodeNotValidException(Exception):
    """Error to indicate the setup code is not valid."""


class PermissionDeniedException(Exception):
    """Error to indicate the setup code or credentals are not valid."""


class VimarErrorResponseException(Exception):
    """Error to indicate the interaction with Vimar Gateway fails with an error."""

    def __init__(self, message) -> None:
        """Initialize message for error."""
        super().__init__(message)
        self.message = message
