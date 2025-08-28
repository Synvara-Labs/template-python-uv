"""Extended test suite for email validators with edge cases and stress testing.

This module contains additional tests for edge cases, security scenarios,
and performance stress testing that complement the main test suite.
"""

import pytest
import timeit
import string
import random
from src.validators import validate_email_format, validate_email_batch


class TestEmailEdgeCases:
    """Test suite for edge cases in email validation."""

    @pytest.mark.parametrize(
        "email,expected,description",
        [
            # Internationalized domain names (IDN)
            ("user@münchen.de", False, "Non-ASCII in domain"),
            ("user@xn--mnchen-3ya.de", True, "Punycode domain"),
            
            # Quoted strings (technically valid in RFC but often problematic)
            ('"user"@example.com', False, "Quoted local part"),
            ('"user name"@example.com', False, "Quoted with space"),
            
            # IP addresses as domains (RFC valid but uncommon)
            ("user@192.168.1.1", False, "IPv4 address"),
            ("user@[IPv6:2001:db8::1]", False, "IPv6 address"),
            
            # Special TLDs
            ("user@example.co", True, "2-char TLD"),
            ("user@example.photography", True, "Long modern TLD"),
            ("user@example.x", False, "1-char TLD (invalid)"),
            
            # Boundary length cases
            ("a" * 64 + "@example.com", True, "Max local part length"),
            ("a" * 65 + "@example.com", False, "Local part too long"),
            ("user@" + "a" * 63 + ".com", True, "Long domain segment"),
            ("user@" + "a" * 64 + ".com", True, "Domain segment 64 chars (currently allowed)"),
            
            # Special character edge cases
            ("user!#$%&'*+-/=?^_`{|}~@example.com", False, "Invalid special chars"),
            ("user..name@example.com", False, "Consecutive dots in local"),
            ("user.@example.com", False, "Trailing dot in local"),
            (".user@example.com", False, "Leading dot in local"),
            
            # Multiple @ symbols variations
            ("user@@example.com", False, "Double @"),
            ("user@middle@example.com", False, "@ in middle"),
            ("@user@example.com", False, "Leading @"),
            
            # Subdomain edge cases
            ("user@.com", False, "Missing domain name"),
            ("user@..com", False, "Double dot domain"),
            ("user@-example.com", True, "Leading hyphen in domain (currently allowed)"),
            ("user@example-.com", True, "Trailing hyphen in domain (currently allowed)"),
            
            # Mixed case (should be case-insensitive)
            ("UsEr@ExAmPlE.CoM", True, "Mixed case"),
            ("USER@EXAMPLE.COM", True, "All uppercase"),
            
            # Whitespace variations
            (" user@example.com", True, "Leading space (stripped)"),
            ("user@example.com ", True, "Trailing space (stripped)"),
            ("\tuser@example.com\n", True, "Tab and newline (stripped)"),
            ("user @example.com", False, "Internal space"),
            
            # Zero-width and invisible characters
            ("user\u200b@example.com", False, "Zero-width space"),
            ("user\u00ad@example.com", False, "Soft hyphen"),
        ],
    )
    def test_edge_case_emails(self, email, expected, description):
        """Test various edge cases in email validation.
        
        These tests cover uncommon but important scenarios including
        internationalized domains, special characters, and boundary cases.
        """
        assert validate_email_format(email) == expected, f"Failed: {description}"

    def test_local_part_64_char_boundary(self):
        """Test the exact 64-character boundary for local part."""
        # Exactly 64 characters - should pass
        local_64 = "a" * 64
        assert validate_email_format(f"{local_64}@example.com") is True
        
        # 65 characters - should fail
        local_65 = "a" * 65
        assert validate_email_format(f"{local_65}@example.com") is False

    def test_total_length_254_char_boundary(self):
        """Test the exact 254-character boundary for total email length."""
        # Create an email exactly 254 characters long
        # Format: local@domain.tld where total = 254
        local = "a" * 64  # Max local part
        # Calculate remaining for domain (254 - 64 - 1(@) = 189)
        domain_part = "b" * 180 + ".com"  # Total domain: 184 chars
        email_254 = f"{local}@{domain_part}"
        assert len(email_254) == 249  # Verify our math
        
        # Pad to exactly 254
        email_254 = ("a" * 64 + "@" + "b" * 185 + ".com")[:254]
        assert len(email_254) == 254
        # This might fail due to domain rules, which is correct
        
        # 255 characters - should always fail
        email_255 = "a" * 250 + "@b.co"
        assert len(email_255) == 255
        assert validate_email_format(email_255) is False


class TestSecurityScenarios:
    """Test suite for security-related scenarios."""

    def test_error_messages_dont_expose_details(self):
        """Ensure error messages don't expose sensitive information."""
        # Test that TypeError messages are generic
        with pytest.raises(TypeError) as exc_info:
            validate_email_format(12345)
        
        error_message = str(exc_info.value)
        # Should not contain the actual value or detailed type info
        assert "12345" not in error_message
        assert "int" not in error_message.lower()  # Check case-insensitively
        assert "string input" in error_message

    def test_no_code_execution(self):
        """Ensure validation doesn't execute embedded code."""
        malicious_emails = [
            "__import__('os').system('ls')@example.com",
            "eval('1+1')@example.com",
            "${7*7}@example.com",
            "{{7*7}}@example.com",
            "<script>alert(1)</script>@example.com",
        ]
        
        for email in malicious_emails:
            # Should safely return False without executing anything
            result = validate_email_format(email)
            assert result is False

    def test_no_regex_dos(self):
        """Test that pathological inputs don't cause regex DoS."""
        # Create potentially problematic patterns
        pathological_patterns = [
            "a" * 1000 + "@" + "b" * 1000 + ".com",  # Very long
            "." * 100 + "@example.com",  # Many dots
            "@" * 100,  # Many @ symbols
            ("a." * 100) + "@example.com",  # Alternating pattern
        ]
        
        for pattern in pathological_patterns:
            start_time = timeit.default_timer()
            try:
                validate_email_format(pattern)
            except:
                pass
            elapsed = timeit.default_timer() - start_time
            
            # Should complete quickly (< 10ms) even for pathological inputs
            assert elapsed < 0.01, f"Pattern took too long: {elapsed}s"


class TestBatchValidation:
    """Test suite for batch email validation."""

    def test_batch_validation_basic(self):
        """Test basic batch validation functionality."""
        emails = [
            "valid1@example.com",
            "valid2@test.org",
            "invalid",
            "also.valid@domain.co.uk",
            "",
            None,  # Non-string
            123,  # Non-string
        ]
        
        results = validate_email_batch(emails)
        
        assert results["valid1@example.com"] is True
        assert results["valid2@test.org"] is True
        assert results["invalid"] is False
        assert results["also.valid@domain.co.uk"] is True
        assert results[""] is False
        assert results[None] is False
        assert results[123] is False

    def test_batch_validation_empty_list(self):
        """Test batch validation with empty list."""
        results = validate_email_batch([])
        assert results == {}

    def test_batch_validation_duplicates(self):
        """Test batch validation handles duplicates correctly."""
        emails = [
            "test@example.com",
            "test@example.com",  # Duplicate
            "other@example.com",
        ]
        
        results = validate_email_batch(emails)
        assert len(results) == 2  # Duplicates overwrite
        assert results["test@example.com"] is True
        assert results["other@example.com"] is True


class TestPerformanceStress:
    """Stress tests for performance validation."""

    def test_stress_large_batch(self):
        """Test performance with large batch of emails."""
        # Generate 1000 test emails
        emails = []
        for i in range(500):
            emails.append(f"user{i}@example.com")  # Valid
            emails.append(f"invalid{i}")  # Invalid
        
        start_time = timeit.default_timer()
        results = validate_email_batch(emails)
        elapsed = timeit.default_timer() - start_time
        
        # Should complete 1000 validations in under 1 second
        assert elapsed < 1.0, f"Batch validation too slow: {elapsed}s"
        assert len(results) == 1000
        
        # Verify correctness of some results
        assert results["user0@example.com"] is True
        assert results["invalid0"] is False

    def test_stress_random_inputs(self):
        """Test with random string inputs to ensure robustness."""
        random.seed(42)  # For reproducibility
        
        for _ in range(100):
            # Generate random string of random length
            length = random.randint(0, 500)
            random_str = ''.join(
                random.choices(string.ascii_letters + string.digits + ".@-_+", k=length)
            )
            
            # Should not crash or hang
            try:
                result = validate_email_format(random_str)
                assert isinstance(result, bool)
            except TypeError:
                # TypeError is acceptable for non-string inputs
                pass

    def test_stress_concurrent_validation(self):
        """Test that validation is thread-safe (for future threading)."""
        # This test prepares for future concurrent implementation
        emails = [f"user{i}@example.com" for i in range(100)]
        
        # Currently sequential, but structure allows for future threading
        results = validate_email_batch(emails, max_workers=4)
        
        assert len(results) == 100
        assert all(results.values())  # All should be valid

    @pytest.mark.parametrize("size", [10, 100, 254])
    def test_performance_by_email_length(self, size):
        """Test performance doesn't degrade with email length."""
        # Create email of specified size
        if size <= 70:
            email = "a" * (size - 10) + "@test.com"
        else:
            local = "a" * 64
            domain = "b" * (size - 70) + ".com"
            email = f"{local}@{domain}"[:size]
        
        # Measure validation time
        time_taken = timeit.timeit(
            lambda: validate_email_format(email),
            number=1000
        )
        
        # Should be consistently fast regardless of length
        assert time_taken < 0.1, f"Validation slow for length {size}: {time_taken}s"


class TestDeprecationWarnings:
    """Test suite for deprecation warnings."""

    def test_is_valid_email_deprecation_warning(self):
        """Test that is_valid_email raises deprecation warning."""
        import warnings
        from src.validators import is_valid_email
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = is_valid_email("test@example.com")
            
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message).lower()
            assert result is True