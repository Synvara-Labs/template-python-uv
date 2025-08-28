"""Unit tests for string utilities module."""

import pytest
from src.string_utils import (
    to_snake_case,
    to_camel_case,
    to_pascal_case,
    to_kebab_case,
    truncate_text,
    word_count,
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
            ("Tiny", 3, "...", "..."),
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
        ],
    )
    def test_word_count(self, text, expected):
        """Test word counting in various texts."""
        assert word_count(text) == expected


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

    def test_special_characters(self):
        """Test conversions with special characters."""
        assert to_snake_case("hello@world#test") == "hello@world#test"
        assert to_camel_case("hello@world#test") == "hello@world#test"
        assert to_pascal_case("hello@world#test") == "Hello@world#test"
        assert to_kebab_case("hello@world#test") == "hello@world#test"

    def test_consecutive_delimiters(self):
        """Test conversions with consecutive delimiters."""
        assert to_snake_case("hello__world") == "hello__world"
        assert to_camel_case("hello__world") == "helloWorld"
        assert to_pascal_case("hello--world") == "HelloWorld"
        assert to_kebab_case("hello  world") == "hello-world"

    def test_truncate_edge_cases(self):
        """Test truncation edge cases."""
        # Suffix longer than max_length
        assert truncate_text("Test", 2, "...") == ".."
        assert truncate_text("Test", 0, "...") == ""
        
        # Text exactly at max_length
        assert truncate_text("12345", 5, "...") == "12345"
        
        # Empty text
        assert truncate_text("", 10, "...") == ""