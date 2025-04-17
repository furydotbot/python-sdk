"""
Custom exceptions for the FURY SDK.
"""
from typing import Dict, Optional


class FurySDKError(Exception):
    """Base exception for FURY SDK."""
    pass


class FuryAPIError(FurySDKError):
    """Exception raised when an API request fails."""
    
    def __init__(self, status_code: Optional[int] = None, message: str = "", error_data: Optional[Dict] = None):
        """
        Initialize the exception.
        
        Args:
            status_code: HTTP status code
            message: Error message
            error_data: Raw error data from the API
        """
        self.status_code = status_code
        self.error_data = error_data or {}
        super().__init__(message)
        
    def __str__(self) -> str:
        """String representation of the error."""
        if self.status_code:
            return f"API Error ({self.status_code}): {super().__str__()}"
        return f"API Error: {super().__str__()}"


class ValidationError(FurySDKError):
    """Exception raised when input validation fails."""
    pass