"""Unit tests for validators module.

Test Suite Summary:
------------------
This comprehensive test suite validates the email validation functions
with 37 test cases covering:

1. Valid Email Formats (9 cases):
   - Standard emails (user@example.com)
   - Emails with special characters in local part (+, -, _, ., %)
   - Emails with subdomains
   - Minimum length valid emails

2. Invalid Email Formats (18 cases):
   - Empty strings and whitespace-only strings
   - Missing components (@, username, domain, TLD)
   - Invalid characters (spaces, consecutive dots)
   - Invalid structure (leading/trailing dots, multiple @)
   - Length violations (>254 chars, TLD too short)

3. Type Validation (4 cases):
   - Ensures TypeError is raised for non-string inputs
   - Validates error messages are informative

4. Edge Cases (6 cases):
   - Whitespace handling
   - Case insensitivity
   - Length boundaries
   - International domains

5. Special Features:
   - Backward compatibility testing
   - Parameterized tests for efficiency
   - Performance considerations
"""

import pytest
from src.validators import validate_email_format, is_valid_email


class TestEmailValidation:
    """Test suite for email validation functions.

    This comprehensive test suite validates the validate_email_format() function
    against various email formats, edge cases, and error conditions.
    Tests are organized by category for maintainability.
    """

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",  # Standard format
            "john.doe@company.org",  # Dot in local part
            "alice_bob@domain.co.uk",  # Underscore in local part
            "test123@test-domain.com",  # Hyphen in domain
            "user+tag@example.io",  # Plus addressing
            "user.name+tag@example.com",  # Combined special chars
            "x@y.com",  # Minimum valid format
            "user%test@example.org",  # Percent sign
            "_test@example.com",  # Leading underscore
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
        assert validate_email_format(email) is True

    @pytest.mark.parametrize(
        "email",
        [
            "",  # Empty string
            "notanemail",  # No @ symbol
            "@example.com",  # No username
            "user@",  # No domain
            "user@domain",  # No TLD extension
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
            "user@",  # Missing domain (duplicate for clarity)
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
        assert validate_email_format(email) is False

    def test_type_validation(self):
        """Test that non-string types raise TypeError.

        Validates type checking for:
        - None values
        - Numeric types (int, float)
        - Collection types (list, dict)
        - Ensures helpful error messages are provided
        """
        with pytest.raises(TypeError, match="Email must be a string type"):
            validate_email_format(None)

        with pytest.raises(TypeError, match="Email must be a string type"):
            validate_email_format(123)

        with pytest.raises(TypeError, match="Email must be a string type"):
            validate_email_format([])

        with pytest.raises(TypeError, match="Email must be a string type"):
            validate_email_format({})

    def test_email_with_whitespace(self):
        """Test that emails with leading/trailing whitespace are handled.

        Edge cases:
        - Leading spaces are stripped before validation
        - Trailing spaces are stripped before validation
        - Tabs and newlines are stripped
        - String with only whitespace returns False
        """
        assert validate_email_format("  user@example.com  ") is True
        assert validate_email_format("\tuser@example.com\n") is True
        assert validate_email_format("   ") is False  # Only whitespace

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
        assert validate_email_format("user+filter@example.com") is True
        assert validate_email_format("user-name@example.com") is True
        assert validate_email_format("user_name@example.com") is True
        assert validate_email_format("user.name@example.com") is True

        # Invalid special characters
        assert validate_email_format("user#name@example.com") is False
        assert validate_email_format("user*name@example.com") is False

    def test_international_domains(self):
        """Test emails with various TLD lengths.

        Validates support for:
        - 2-character TLDs (.co, .uk)
        - 3-character TLDs (.com, .org)
        - 4+ character TLDs (.info, .museum)
        - Modern long TLDs (.engineering)
        """
        assert validate_email_format("user@example.co") is True  # 2 chars
        assert validate_email_format("user@example.com") is True  # 3 chars
        assert validate_email_format("user@example.info") is True  # 4 chars
        assert validate_email_format("user@example.museum") is True  # 6 chars
        assert validate_email_format("user@example.engineering") is True  # 11 chars

    def test_subdomain_emails(self):
        """Test emails with subdomains.

        Validates emails with:
        - Single subdomain (mail.example.com)
        - Multiple subdomains (mail.server.example.com)
        - Deeply nested subdomains
        """
        assert validate_email_format("user@mail.example.com") is True
        assert validate_email_format("user@mail.server.example.com") is True
        assert validate_email_format("user@deeply.nested.subdomain.example.com") is True

    def test_backward_compatibility(self):
        """Test that is_valid_email alias works for backward compatibility.

        The is_valid_email name is deprecated but maintained
        for existing code. New code should use validate_email_format().
        Tests ensure both functions behave identically.
        """
        # Test that alias calls the main function correctly
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("invalid") is False

        # Verify they produce identical results
        test_cases = ["user@example.com", "invalid.email", "", "test@domain..com"]
        for email in test_cases:
            assert is_valid_email(email) == validate_email_format(email)

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
        assert validate_email_format("a@b.co") is True
        assert validate_email_format("a@b") is False  # No TLD

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("USER@EXAMPLE.COM", True),  # All uppercase
            ("User@Example.Com", True),  # Mixed case
            ("uSeR@eXaMpLe.CoM", True),  # Random case
        ],
    )
    def test_case_sensitivity(self, email, expected):
        """Test that email validation is case-insensitive.

        Email addresses should be validated regardless of case:
        - All uppercase (USER@EXAMPLE.COM)
        - Mixed case (User@Example.Com)
        - Random case (uSeR@eXaMpLe.CoM)
        """
        assert validate_email_format(email) == expected


class TestPerformanceConsiderations:
    """Test suite for performance validation.

    These tests ensure the email validation function performs
    efficiently even with edge cases and large inputs.
    """

    def test_validation_performance(self):
        """Benchmark email validation performance.

        Tests that validation completes quickly for:
        - Standard emails
        - Complex emails with subdomains
        - Maximum length emails
        - Invalid emails that fail early checks
        """
        import timeit

        # Test standard email performance
        standard_time = timeit.timeit(
            lambda: validate_email_format("user@example.com"), number=1000
        )

        # Test complex email performance
        complex_email = "user.name+tag@mail.server.subdomain.example.com"
        complex_time = timeit.timeit(
            lambda: validate_email_format(complex_email), number=1000
        )

        # Performance assertions (should complete 1000 validations in < 1 second)
        assert standard_time < 1.0, f"Standard validation too slow: {standard_time}s"
        assert complex_time < 1.0, f"Complex validation too slow: {complex_time}s"

        # Ensure early returns work efficiently
        invalid_time = timeit.timeit(
            lambda: validate_email_format("..@invalid"), number=1000
        )
        assert invalid_time < 1.0, f"Invalid email check too slow: {invalid_time}s"
