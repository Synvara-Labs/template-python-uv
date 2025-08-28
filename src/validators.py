"""Validation utilities for common data types."""

import re


def is_valid_email(email: str) -> bool:
    """Validate if a string is a valid email address.
    
    Uses a simple regex pattern to validate email format.
    This covers most common email formats but is not exhaustive.
    
    Args:
        email: The email address string to validate.
        
    Returns:
        True if the email format is valid, False otherwise.
        
    Examples:
        >>> is_valid_email("user@example.com")
        True
        
        >>> is_valid_email("invalid.email")
        False
        
        >>> is_valid_email("user@")
        False
    """
    if not email or not isinstance(email, str):
        return False
    
    # Simple email regex pattern
    # Matches: username@domain.extension
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email.strip()))