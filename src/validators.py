"""Validation utilities for common data types.

This module provides functions for validating various input formats
including email addresses. All validators follow consistent patterns
for error handling and return values.
"""

import re
from typing import Optional


def is_valid_email(email: str) -> bool:
    """Check if a string is a valid email address format.

    This function validates email format only, not whether the email
    address actually exists. It follows a subset of RFC 5322 standards
    for practical email validation.

    Args:
        email: The email address string to validate.

    Returns:
        bool: True if the email format is valid, False otherwise.

    Raises:
        TypeError: If email is not a string type.

    Examples:
        >>> is_valid_email("user@example.com")
        True

        >>> is_valid_email("john.doe+filter@company.org")
        True

        >>> is_valid_email("invalid.email")
        False

        >>> is_valid_email("user@domain..com")  # Consecutive dots
        False

    Note:
        - Validates format only, not email existence
        - Supports common special characters (+, -, _, .)
        - Prevents consecutive dots in domain
        - Requires 2+ character TLD
        - Maximum email length: 254 characters (per RFC 5321)

    Edge Cases Handled:
        - Empty strings return False
        - Whitespace is stripped before validation
        - Consecutive dots anywhere in email return False
        - Leading/trailing dots return False
        - Missing @ symbol returns False
        - Missing domain or TLD returns False
        - Email length > 254 chars returns False
    """
    # Type checking with explicit error
    if not isinstance(email, str):
        raise TypeError(f"Email must be a string, got {type(email).__name__}")

    # Check for empty string explicitly
    if len(email) == 0:
        return False

    # Strip whitespace
    email = email.strip()

    # Check length constraints (RFC 5321)
    if len(email) > 254 or len(email) < 3:  # minimum: a@b
        return False

    # Email validation regex pattern (RFC 5322 subset for practical use)
    # Pattern breakdown for maintainability:
    # ^[a-zA-Z0-9._%+-]+   : Local part (username)
    #                        - Alphanumeric characters
    #                        - Common special chars: . _ % + -
    #                        - At least one character required
    # @                    : Required @ separator
    # [a-zA-Z0-9-]+        : Domain name first part
    #                        - Alphanumeric and hyphens
    #                        - At least one character
    # (\.[a-zA-Z0-9-]+)*   : Additional domain parts (subdomains)
    #                        - Optional, can have multiple
    #                        - Each starts with a dot
    # \.[a-zA-Z]{2,}$      : Top-level domain (TLD)
    #                        - Starts with a dot
    #                        - At least 2 alphabetic characters
    #                        - Anchored to end of string
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$"

    # Additional validation: no consecutive dots anywhere
    if ".." in email:
        return False

    # Check if email starts or ends with a dot
    if email.startswith(".") or email.endswith("."):
        return False

    # Check for @ symbol at start or end
    if email.startswith("@") or email.endswith("@"):
        return False

    # Check for dot immediately before @
    if ".@" in email:
        return False

    # Check for @ immediately after dot
    if "@." in email:
        return False

    return bool(re.match(pattern, email))


# Backward compatibility alias (deprecated)
# This alias is maintained for backward compatibility with existing code.
# New code should use is_valid_email() directly.
# Will be removed in version 2.0.0
validate_email_format = is_valid_email


def validate_email_exists(email: str) -> Optional[bool]:
    """Placeholder for future email existence validation.

    This function would check if an email address actually exists
    by performing DNS lookups and SMTP verification.

    Args:
        email: The email address to verify.

    Returns:
        Optional[bool]: None (not implemented).

    Note:
        Not implemented. Use is_valid_email() for format validation.
    """
    # Future implementation placeholder
    return None
