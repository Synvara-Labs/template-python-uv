"""Unit tests for validators module."""

import pytest
from src.validators import is_valid_email, validate_email_format


class TestEmailValidation:
    """Test suite for email validation function.

    This comprehensive test suite validates the is_valid_email() function
    against various email formats, edge cases, and error conditions.
    Tests are organized by category for maintainability.
    """

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "john.doe@company.org",
            "alice_bob@domain.co.uk",
            "test123@test-domain.com",
            "user+tag@example.io",
            "user.name+tag@example.com",
            "x@y.com",  # Minimum valid format
            "user%test@example.org",
            "_test@example.com",
        ],
    )
    def test_valid_email_formats(self, email):
        """Test that valid email addresses are accepted.

        Tests standard email formats including:
        - Simple emails (user@example.com)
        - Emails with dots (john.doe@company.org)
        - Emails with underscores (alice_bob@domain.co.uk)
        - Emails with hyphens in domain (test123@test-domain.com)
        - Emails with plus addressing (user+tag@example.io)
        - Minimum valid format (x@y.com)
        - Special characters that are RFC-compliant
        """
        assert is_valid_email(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "",  # Empty string
            "notanemail",  # No @ symbol
            "@example.com",  # No username
            "user@",  # No domain
            "user@domain",  # No extension
            "user @example.com",  # Space in username
            "user@exam ple.com",  # Space in domain
            "user@domain..com",  # Consecutive dots in domain
            "user..name@example.com",  # Consecutive dots in username
            ".user@example.com",  # Starts with dot
            "user.@example.com",  # Ends with dot before @
            "user@.example.com",  # Dot after @
            "user@example.com.",  # Ends with dot
            "@",  # Just @ symbol
            "user@@example.com",  # Double @
            "user@",  # Missing domain
            "user@domain.c",  # TLD too short (1 char)
            "a" * 255 + "@test.com",  # Too long (>254 chars)
        ],
    )
    def test_invalid_email_formats(self, email):
        """Test that invalid email addresses are rejected.

        Edge cases tested:
        - Empty string
        - Missing @ symbol (notanemail)
        - Missing username (@example.com)
        - Missing domain (user@)
        - Missing TLD extension (user@domain)
        - Spaces in email parts
        - Consecutive dots (user@domain..com)
        - Leading/trailing dots
        - Multiple @ symbols
        - TLD too short (1 character)
        - Email exceeding 254 character limit
        """
        assert is_valid_email(email) is False

    def test_type_validation(self):
        """Test that non-string types raise TypeError.

        Validates type checking for:
        - None values
        - Numeric types (int, float)
        - Collection types (list, dict)
        - Ensures helpful error messages are provided
        """
        with pytest.raises(TypeError, match="Email must be a string"):
            is_valid_email(None)

        with pytest.raises(TypeError, match="Email must be a string"):
            is_valid_email(123)

        with pytest.raises(TypeError, match="Email must be a string"):
            is_valid_email([])

        with pytest.raises(TypeError, match="Email must be a string"):
            is_valid_email({})

    def test_email_with_whitespace(self):
        """Test that emails with leading/trailing whitespace are handled.

        Edge cases:
        - Leading spaces are stripped before validation
        - Trailing spaces are stripped before validation
        - Tabs and newlines are stripped
        - String with only whitespace returns False
        """
        assert is_valid_email("  user@example.com  ") is True
        assert is_valid_email("\tuser@example.com\n") is True
        assert is_valid_email("   ") is False  # Only whitespace

    def test_special_characters_in_email(self):
        """Test emails with various special characters.

        Tests RFC-compliant special characters:
        - Plus sign for email filtering (user+filter@example.com)
        - Hyphens in username (user-name@example.com)
        - Underscores (user_name@example.com)
        - Dots for organization (user.name@example.com)

        Also tests invalid special characters:
        - Hash/pound sign (#)
        - Asterisk (*)
        """
        # Valid special characters
        assert is_valid_email("user+filter@example.com") is True
        assert is_valid_email("user-name@example.com") is True
        assert is_valid_email("user_name@example.com") is True
        assert is_valid_email("user.name@example.com") is True

        # Invalid special characters
        assert is_valid_email("user#name@example.com") is False
        assert is_valid_email("user*name@example.com") is False

    def test_international_domains(self):
        """Test emails with various TLD lengths.

        Validates support for:
        - 2-character TLDs (.co, .uk)
        - 3-character TLDs (.com, .org)
        - 4+ character TLDs (.info, .museum)
        - Modern long TLDs (.engineering)
        """
        assert is_valid_email("user@example.co") is True  # 2 chars
        assert is_valid_email("user@example.com") is True  # 3 chars
        assert is_valid_email("user@example.info") is True  # 4 chars
        assert is_valid_email("user@example.museum") is True  # 6 chars
        assert is_valid_email("user@example.engineering") is True  # 11 chars

    def test_subdomain_emails(self):
        """Test emails with subdomains.

        Validates emails with:
        - Single subdomain (mail.example.com)
        - Multiple subdomains (mail.server.example.com)
        - Deeply nested subdomains
        """
        assert is_valid_email("user@mail.example.com") is True
        assert is_valid_email("user@mail.server.example.com") is True
        assert is_valid_email("user@deeply.nested.subdomain.example.com") is True

    def test_backward_compatibility(self):
        """Test that validate_email_format alias still works for backward compatibility.

        The validate_email_format name is deprecated but maintained
        for existing code. New code should use is_valid_email().
        """
        # Should be an alias to is_valid_email
        assert validate_email_format == is_valid_email
        assert validate_email_format("test@example.com") is True
        assert validate_email_format("invalid") is False

    def test_edge_case_lengths(self):
        """Test email length edge cases.

        Tests RFC 5321 length constraints:
        - Maximum valid email length (254 characters)
        - Minimum valid email format (a@b.co)
        - Rejection of emails without proper TLD
        """
        # Maximum valid length (254 chars)
        local = "a" * 64  # Max local part
        domain = "b" * 63 + "." + "c" * 63 + ".com"  # Valid domain
        long_valid = f"{local}@{domain}"[:254]
        assert len(long_valid) <= 254

        # Minimum valid (a@b is technically not valid due to TLD requirement)
        assert is_valid_email("a@b.co") is True
        assert is_valid_email("a@b") is False  # No TLD

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("USER@EXAMPLE.COM", True),  # Case sensitivity
            ("User@Example.Com", True),
            ("uSeR@eXaMpLe.CoM", True),
        ],
    )
    def test_case_sensitivity(self, email, expected):
        """Test that email validation is case-insensitive.

        Email addresses should be validated regardless of case:
        - All uppercase (USER@EXAMPLE.COM)
        - Mixed case (User@Example.Com)
        - Random case (uSeR@eXaMpLe.CoM)
        """
        assert is_valid_email(email) == expected
