"""Validation utilities for common data types.

This module provides functions for validating various input formats
including email addresses. All validators follow consistent patterns
for error handling and return values.
"""

import re
from typing import Optional


def validate_email_format(email: str) -> bool:
    """
    Validate the format of an email address according to RFC 5322.

    This function validates email format only, not whether the email
    address actually exists. It uses a practical subset of RFC 5322
    standards suitable for modern email validation.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.

    Raises:
        TypeError: If the input is not a string type. The exception message
            includes the actual type received for debugging.

    Examples:
        >>> validate_email_format("user@example.com")
        True

        >>> validate_email_format("john.doe+filter@company.org")
        True

        >>> validate_email_format("invalid.email")
        False

        >>> validate_email_format("user@domain..com")  # Consecutive dots
        False

        >>> validate_email_format(123)  # Non-string input
        Traceback (most recent call last):
            ...
        TypeError: Email must be a string type. Received 'int' instead.

    Note:
        - Validates format only, not email existence
        - Supports common special characters (+, -, _, ., %)
        - Prevents consecutive dots anywhere in the email
        - Requires 2+ character TLD (top-level domain)
        - Maximum email length: 254 characters (per RFC 5321)
        - Whitespace is automatically stripped before validation

    Performance:
        The function uses compiled regex for efficient validation.
        Typical validation time: < 1ms per email address.
    """
    # Explicit type checking with informative error message
    if not isinstance(email, str):
        raise TypeError(
            f"Email must be a string type. Received '{type(email).__name__}' instead."
        )

    # Handle empty string case
    if not email:
        return False

    # Strip leading/trailing whitespace
    email = email.strip()

    # Check length constraints according to RFC 5321
    if not (3 <= len(email) <= 254):  # minimum valid: a@b
        return False

    # Early validation checks for common invalid patterns
    # These checks are faster than regex and catch common errors
    invalid_patterns = [
        "..",  # Consecutive dots
        ".@",  # Dot before @
        "@.",  # @ before dot
    ]

    for pattern in invalid_patterns:
        if pattern in email:
            return False

    # Check for invalid start/end characters
    if email[0] in ".@" or email[-1] in ".@":
        return False

    # Build regex pattern from components for better readability
    # Each component is documented for maintainability

    # Local part: username before @ symbol
    # Allows: letters, numbers, and special chars (._%-+)
    local_part = r"[a-zA-Z0-9._%+-]+"

    # Domain first segment: immediately after @
    # Allows: letters, numbers, and hyphens
    domain_segment = r"[a-zA-Z0-9-]+"

    # Additional domain segments: subdomains
    # Each must start with a dot, followed by allowed chars
    subdomain_segments = r"(\.[a-zA-Z0-9-]+)*"

    # Top-level domain: final segment
    # Must be at least 2 alphabetic characters
    tld = r"\.[a-zA-Z]{2,}"

    # Combine components into complete pattern
    # Pattern is anchored with ^ and $ to match entire string
    email_pattern = f"^{local_part}@{domain_segment}{subdomain_segments}{tld}$"

    # Compile regex for better performance
    compiled_pattern = re.compile(email_pattern)

    # Perform regex validation
    return bool(compiled_pattern.match(email))


def is_valid_email(email: str) -> bool:
    """
    Alias for validate_email_format for backward compatibility.

    This function is deprecated and will be removed in version 2.0.0.
    New code should use validate_email_format() directly.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.

    Raises:
        TypeError: If the input is not a string type.

    See Also:
        validate_email_format: The primary function for email validation.
    """
    return validate_email_format(email)


def validate_email_exists(email: str) -> Optional[bool]:
    """
    Placeholder for future email existence validation.

    This function would check if an email address actually exists
    by performing DNS lookups and SMTP verification.

    Args:
        email (str): The email address to verify.

    Returns:
        Optional[bool]: None (not implemented).

    Note:
        Not implemented. Use validate_email_format() for format validation.
    """
    # Future implementation placeholder
    return None
