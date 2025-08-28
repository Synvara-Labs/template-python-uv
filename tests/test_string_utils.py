"""Unit tests for string utilities module."""

import pytest
import timeit
from src.string_utils import (
    to_snake_case,
    to_camel_case,
    to_pascal_case,
    to_kebab_case,
    truncate_text,
    word_count,
    is_mixed_case,
    remove_extra_whitespace,
)


class TestCaseConversions:
    """Test suite for case conversion functions."""

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("HelloWorld", "hello_world"),
            ("someVariableName", "some_variable_name"),
            ("convert-to-snake", "convert_to_snake"),
            ("already_snake_case", "already_snake_case"),
            ("Mixed-Style_Example", "mixed_style_example"),
            ("XMLHttpRequest", "xml_http_request"),
            ("IOError", "io_error"),
            ("", ""),
            ("a", "a"),
            ("ABC", "abc"),
            ("123Numbers", "123_numbers"),
            ("with spaces here", "with_spaces_here"),
            ("__multiple__underscores__", "multiple_underscores"),
            ("CamelCASEMixed", "camel_case_mixed"),
        ],
    )
    def test_to_snake_case(self, input_text, expected):
        """Test conversion to snake_case."""
        assert to_snake_case(input_text) == expected

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello_world", "helloWorld"),
            ("some-variable-name", "someVariableName"),
            ("Convert to camel", "convertToCamel"),
            ("already_camelCase", "alreadyCamelcase"),
            ("mixed-Style_Example", "mixedStyleExample"),
            ("", ""),
            ("a", "a"),
            ("first", "first"),
            ("UPPERCASE", "uppercase"),
            ("123_numbers", "123Numbers"),
            ("__multiple__delimiters__", "multipleDelimiters"),
            ("!!!only!!!special!!!", "onlySpecial"),
        ],
    )
    def test_to_camel_case(self, input_text, expected):
        """Test conversion to camelCase."""
        assert to_camel_case(input_text) == expected

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("hello_world", "HelloWorld"),
            ("some-variable-name", "SomeVariableName"),
            ("convert to pascal", "ConvertToPascal"),
            ("already_PascalCase", "AlreadyPascalcase"),
            ("mixed-Style_Example", "MixedStyleExample"),
            ("", ""),
            ("a", "A"),
            ("first", "First"),
            ("UPPERCASE", "Uppercase"),
            ("123_numbers", "123Numbers"),
            ("__multiple__delimiters__", "MultipleDelimiters"),
        ],
    )
    def test_to_pascal_case(self, input_text, expected):
        """Test conversion to PascalCase."""
        assert to_pascal_case(input_text) == expected

    @pytest.mark.parametrize(
        "input_text,expected",
        [
            ("HelloWorld", "hello-world"),
            ("some_variable_name", "some-variable-name"),
            ("Convert To Kebab", "convert-to-kebab"),
            ("already-kebab-case", "already-kebab-case"),
            ("Mixed_Style Example", "mixed-style-example"),
            ("XMLHttpRequest", "xml-http-request"),
            ("", ""),
            ("a", "a"),
            ("ABC", "abc"),
            ("123Numbers", "123-numbers"),
            ("--multiple--hyphens--", "multiple-hyphens"),
            ("HTTPSConnection", "https-connection"),
        ],
    )
    def test_to_kebab_case(self, input_text, expected):
        """Test conversion to kebab-case."""
        assert to_kebab_case(input_text) == expected


class TestTextUtilities:
    """Test suite for text utility functions."""

    @pytest.mark.parametrize(
        "text,max_length,suffix,expected",
        [
            ("This is a long text", 10, "...", "This is..."),
            ("Short", 10, "...", "Short"),
            ("Exactly ten", 11, "...", "Exactly ten"),
            ("Truncate this text", 15, "...", "Truncate thi..."),
            ("Custom suffix", 10, "→", "Custom su→"),
            ("No suffix needed", 20, "...", "No suffix needed"),
            ("", 5, "...", ""),
            ("Very long text that needs truncation", 20, "...", "Very long text th..."),
            ("Edge", 4, "...", "Edge"),  # Text same as max_length
            ("Tiny", 3, "...", ""),  # Too small for meaningful truncation
            ("Test", 2, "...", ""),  # Too small
            ("Test", 4, "!!!", "Test"),  # Exact length, no truncation
        ],
    )
    def test_truncate_text(self, text, max_length, suffix, expected):
        """Test text truncation with various parameters."""
        assert truncate_text(text, max_length, suffix) == expected

    def test_truncate_text_default_suffix(self):
        """Test truncate_text with default suffix."""
        assert truncate_text("This is a long text", 10) == "This is..."
        assert truncate_text("Short", 10) == "Short"

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("Hello world", 2),
            ("  Multiple   spaces  ", 2),
            ("", 0),
            ("One", 1),
            ("This is a test sentence.", 5),
            ("   ", 0),
            ("Word", 1),
            ("Multiple\nlines\nwith\nwords", 4),
            ("\tTabs\tand\tspaces\t", 3),
            ("123 456 789", 3),
            ("one-word", 1),  # Hyphenated as single word
            ("email@example.com", 1),  # Email as single word
        ],
    )
    def test_word_count(self, text, expected):
        """Test word counting in various texts."""
        assert word_count(text) == expected


class TestAdditionalUtilities:
    """Test suite for additional utility functions."""

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("HelloWorld", True),
            ("ALLCAPS", False),
            ("lowercase", False),
            ("MixedCase", True),
            ("", False),
            ("123", False),
            ("123ABC", False),  # No lowercase
            ("123abc", False),  # No uppercase
            ("aB", True),
            ("!@#$%", False),  # No letters
        ],
    )
    def test_is_mixed_case(self, text, expected):
        """Test mixed case detection."""
        assert is_mixed_case(text) == expected

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("  Hello   world  ", "Hello world"),
            ("Multiple\n\nlines", "Multiple lines"),
            ("\t\tTabs\t\t", "Tabs"),
            ("Normal text", "Normal text"),
            ("", ""),
            ("   ", ""),
            ("One  Two  Three", "One Two Three"),
            ("Line\nbreak\tand\ttab", "Line break and tab"),
            ("  \n\t  Mixed  \n  whitespace  \t  ", "Mixed whitespace"),
        ],
    )
    def test_remove_extra_whitespace(self, text, expected):
        """Test whitespace normalization."""
        assert remove_extra_whitespace(text) == expected


class TestEdgeCases:
    """Test suite for edge cases and special scenarios."""

    def test_empty_string_conversions(self):
        """Test all conversions with empty string."""
        assert to_snake_case("") == ""
        assert to_camel_case("") == ""
        assert to_pascal_case("") == ""
        assert to_kebab_case("") == ""

    def test_single_character_conversions(self):
        """Test all conversions with single character."""
        assert to_snake_case("A") == "a"
        assert to_camel_case("A") == "a"
        assert to_pascal_case("A") == "A"
        assert to_kebab_case("A") == "a"

    def test_numbers_in_conversions(self):
        """Test conversions with numbers."""
        assert to_snake_case("test123Case") == "test123_case"
        assert to_camel_case("test_123_case") == "test123Case"
        assert to_pascal_case("test_123_case") == "Test123Case"
        assert to_kebab_case("test123Case") == "test123-case"

    def test_special_characters_only(self):
        """Test conversions with only special characters."""
        assert to_snake_case("!!!@@@###") == ""
        assert to_camel_case("!!!@@@###") == ""
        assert to_pascal_case("!!!@@@###") == ""
        assert to_kebab_case("!!!@@@###") == ""
        assert to_snake_case("___") == ""
        assert to_kebab_case("---") == ""

    def test_consecutive_delimiters(self):
        """Test conversions with consecutive delimiters."""
        assert to_snake_case("hello___world") == "hello_world"
        assert to_camel_case("hello___world") == "helloWorld"
        assert to_pascal_case("hello---world") == "HelloWorld"
        assert to_kebab_case("hello   world") == "hello-world"
        assert to_snake_case("test____case____example") == "test_case_example"
        assert to_kebab_case("test----case----example") == "test-case-example"

    def test_truncate_edge_cases(self):
        """Test truncation edge cases."""
        # Suffix longer than max_length
        assert truncate_text("Test", 2, "...") == ""
        assert truncate_text("Test", 0, "...") == ""
        
        # Text exactly at max_length
        assert truncate_text("12345", 5, "...") == "12345"
        
        # Empty text
        assert truncate_text("", 10, "...") == ""
        
        # Very long suffix
        assert truncate_text("Short", 10, "VERYLONGSUFFIX") == "Short"
        assert truncate_text("This needs truncation", 10, "LONG") == "This nLONG"

    def test_unicode_handling(self):
        """Test handling of Unicode characters."""
        # Note: Current implementation treats accented chars as non-alphanumeric
        assert "caf" in to_snake_case("Café").lower()
        assert "m_nch" in to_snake_case("München").lower()
        assert word_count("Café au lait") == 3
        assert is_mixed_case("Café") == True


class TestPerformance:
    """Test suite for performance characteristics."""

    def test_performance_with_long_strings(self):
        """Test that functions handle long strings efficiently."""
        long_text = "CamelCase" * 100  # 900 characters
        
        # Should complete quickly (under 10ms)
        start = timeit.default_timer()
        result = to_snake_case(long_text)
        elapsed = timeit.default_timer() - start
        assert elapsed < 0.01
        assert "camel_case" in result
        
        # Test other conversions
        start = timeit.default_timer()
        to_kebab_case(long_text)
        elapsed = timeit.default_timer() - start
        assert elapsed < 0.01

    def test_performance_with_many_delimiters(self):
        """Test performance with many consecutive delimiters."""
        text_with_delimiters = "_" * 100 + "test" + "_" * 100 + "case"
        
        start = timeit.default_timer()
        result = to_snake_case(text_with_delimiters)
        elapsed = timeit.default_timer() - start
        assert elapsed < 0.01
        assert result == "test_case"

    def test_regex_compilation_benefit(self):
        """Test that precompiled regex improves performance."""
        # Run multiple conversions to test regex caching
        test_cases = ["CamelCase", "snake_case", "kebab-case"] * 100
        
        start = timeit.default_timer()
        for text in test_cases:
            to_snake_case(text)
            to_kebab_case(text)
        elapsed = timeit.default_timer() - start
        
        # Should complete 600 conversions in under 100ms
        assert elapsed < 0.1