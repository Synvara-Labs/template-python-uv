"""Unit tests for validators module."""

import pytest
from src.validators import is_valid_email


class TestEmailValidation:
    """Test suite for email validation function."""
    
    def test_valid_emails(self):
        """Test that valid email addresses are accepted."""
        valid_emails = [
            "user@example.com",
            "john.doe@company.org",
            "alice_bob@domain.co.uk",
            "test123@test-domain.com",
            "user+tag@example.io",
        ]
        
        for email in valid_emails:
            assert is_valid_email(email) is True, f"Failed for: {email}"
    
    def test_invalid_emails(self):
        """Test that invalid email addresses are rejected."""
        invalid_emails = [
            "",                    # Empty string
            "notanemail",         # No @ symbol
            "@example.com",       # No username
            "user@",              # No domain
            "user@domain",        # No extension
            "user @example.com",  # Space in username
            "user@exam ple.com",  # Space in domain
            None,                 # None value
            123,                  # Non-string
        ]
        
        for email in invalid_emails:
            assert is_valid_email(email) is False, f"Failed for: {email}"
    
    def test_email_with_whitespace(self):
        """Test that emails with leading/trailing whitespace are handled."""
        assert is_valid_email("  user@example.com  ") is True
        assert is_valid_email("\tuser@example.com\n") is True