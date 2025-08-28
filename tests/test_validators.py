"""Unit tests for validators module."""

import pytest
from src.validators import validate_email_format, is_valid_email


class TestEmailValidation:
    """Test suite for email validation function."""
    
    @pytest.mark.parametrize("email", [
        "user@example.com",
        "john.doe@company.org", 
        "alice_bob@domain.co.uk",
        "test123@test-domain.com",
        "user+tag@example.io",
        "user.name+tag@example.com",
        "x@y.com",  # Minimum valid format
        "user%test@example.org",
        "_test@example.com",
    ])
    def test_valid_email_formats(self, email):
        """Test that valid email addresses are accepted."""
        assert validate_email_format(email) is True
    
    @pytest.mark.parametrize("email", [
        "",                      # Empty string
        "notanemail",           # No @ symbol
        "@example.com",         # No username
        "user@",                # No domain
        "user@domain",          # No extension
        "user @example.com",    # Space in username
        "user@exam ple.com",    # Space in domain
        "user@domain..com",     # Consecutive dots in domain
        "user..name@example.com", # Consecutive dots in username
        ".user@example.com",    # Starts with dot
        "user.@example.com",    # Ends with dot before @
        "user@.example.com",    # Dot after @
        "user@example.com.",    # Ends with dot
        "@",                    # Just @ symbol
        "user@@example.com",    # Double @
        "user@",                # Missing domain
        "user@domain.c",        # TLD too short (1 char)
        "a" * 255 + "@test.com", # Too long (>254 chars)
    ])
    def test_invalid_email_formats(self, email):
        """Test that invalid email addresses are rejected."""
        assert validate_email_format(email) is False
    
    def test_type_validation(self):
        """Test that non-string types raise TypeError."""
        with pytest.raises(TypeError, match="Email must be a string"):
            validate_email_format(None)
        
        with pytest.raises(TypeError, match="Email must be a string"):
            validate_email_format(123)
        
        with pytest.raises(TypeError, match="Email must be a string"):
            validate_email_format([])
        
        with pytest.raises(TypeError, match="Email must be a string"):
            validate_email_format({})
    
    def test_email_with_whitespace(self):
        """Test that emails with leading/trailing whitespace are handled."""
        assert validate_email_format("  user@example.com  ") is True
        assert validate_email_format("\tuser@example.com\n") is True
        assert validate_email_format("   ") is False  # Only whitespace
    
    def test_special_characters_in_email(self):
        """Test emails with various special characters."""
        # Valid special characters
        assert validate_email_format("user+filter@example.com") is True
        assert validate_email_format("user-name@example.com") is True
        assert validate_email_format("user_name@example.com") is True
        assert validate_email_format("user.name@example.com") is True
        
        # Invalid special characters
        assert validate_email_format("user#name@example.com") is False
        assert validate_email_format("user*name@example.com") is False
    
    def test_international_domains(self):
        """Test emails with various TLD lengths."""
        assert validate_email_format("user@example.co") is True  # 2 chars
        assert validate_email_format("user@example.com") is True  # 3 chars
        assert validate_email_format("user@example.info") is True  # 4 chars
        assert validate_email_format("user@example.museum") is True  # 6 chars
        assert validate_email_format("user@example.engineering") is True  # 11 chars
    
    def test_subdomain_emails(self):
        """Test emails with subdomains."""
        assert validate_email_format("user@mail.example.com") is True
        assert validate_email_format("user@mail.server.example.com") is True
        assert validate_email_format("user@deeply.nested.subdomain.example.com") is True
    
    def test_backward_compatibility(self):
        """Test that is_valid_email alias still works."""
        # Should be an alias to validate_email_format
        assert is_valid_email == validate_email_format
        assert is_valid_email("test@example.com") is True
        assert is_valid_email("invalid") is False
    
    def test_edge_case_lengths(self):
        """Test email length edge cases."""
        # Maximum valid length (254 chars)
        local = "a" * 64  # Max local part
        domain = "b" * 63 + "." + "c" * 63 + ".com"  # Valid domain
        long_valid = f"{local}@{domain}"[:254]
        assert len(long_valid) <= 254
        
        # Minimum valid (a@b is technically not valid due to TLD requirement)
        assert validate_email_format("a@b.co") is True
        assert validate_email_format("a@b") is False  # No TLD
    
    @pytest.mark.parametrize("email,expected", [
        ("USER@EXAMPLE.COM", True),  # Case sensitivity
        ("User@Example.Com", True),
        ("uSeR@eXaMpLe.CoM", True),
    ])
    def test_case_sensitivity(self, email, expected):
        """Test that email validation is case-insensitive."""
        assert validate_email_format(email) == expected