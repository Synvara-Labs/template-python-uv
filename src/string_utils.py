"""String manipulation utilities for common text transformations.

This module provides functions for converting between different text cases
commonly used in programming and documentation.
"""

import re
from typing import List


# Precompile regex patterns for better performance
_CONSECUTIVE_CAPS = re.compile(r'([A-Z]+)([A-Z][a-z])')
_CAMEL_BOUNDARY = re.compile(r'([a-z0-9])([A-Z])')
_NON_ALNUM = re.compile(r'[^a-zA-Z0-9]+')
_WHITESPACE = re.compile(r'\s+')


def _tokenize_string(text: str) -> List[str]:
    """
    Tokenize a string into words based on case transitions, delimiters, and numbers.
    
    This shared tokenizer ensures consistent behavior across all case conversion functions.
    
    Args:
        text: Input string to tokenize
        
    Returns:
        List of word tokens
        
    Examples:
        >>> _tokenize_string("HelloWorld")
        ['Hello', 'World']
        >>> _tokenize_string("XMLHttpRequest")
        ['XML', 'Http', 'Request']
        >>> _tokenize_string("snake_case_example")
        ['snake', 'case', 'example']
    """
    if not text:
        return []
    
    # First, replace non-alphanumeric with spaces
    text = _NON_ALNUM.sub(' ', text)
    
    # Handle consecutive capitals (e.g., XMLHttp -> XML Http)
    text = _CONSECUTIVE_CAPS.sub(r'\1 \2', text)
    
    # Insert space before capitals preceded by lowercase/digit
    text = _CAMEL_BOUNDARY.sub(r'\1 \2', text)
    
    # Split on whitespace and filter empty strings
    tokens = text.split()
    
    return [token for token in tokens if token]


def to_snake_case(text: str) -> str:
    """Convert a string to snake_case.
    
    Args:
        text: Input string to convert
        
    Returns:
        String converted to snake_case
        
    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("XMLHttpRequest")
        'xml_http_request'
        >>> to_snake_case("IOError")
        'io_error'
        >>> to_snake_case("convert-to-snake")
        'convert_to_snake'
        >>> to_snake_case("multiple   spaces")
        'multiple_spaces'
        >>> to_snake_case("__already__snake__")
        'already_snake'
    """
    tokens = _tokenize_string(text)
    if not tokens:
        return ""
    
    return '_'.join(token.lower() for token in tokens)


def to_camel_case(text: str) -> str:
    """Convert a string to camelCase.
    
    Args:
        text: Input string to convert
        
    Returns:
        String converted to camelCase
        
    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("some-variable-name")
        'someVariableName'
        >>> to_camel_case("Convert to camel")
        'convertToCamel'
        >>> to_camel_case("HelloWorld")
        'helloWorld'
        >>> to_camel_case("XMLHttpRequest")
        'xmlHttpRequest'
        >>> to_camel_case("__multiple__delimiters__")
        'multipleDelimiters'
    """
    tokens = _tokenize_string(text)
    if not tokens:
        return ""
    
    # First token lowercase, rest capitalized
    return tokens[0].lower() + ''.join(token.capitalize() for token in tokens[1:])


def to_pascal_case(text: str) -> str:
    """Convert a string to PascalCase.
    
    Args:
        text: Input string to convert
        
    Returns:
        String converted to PascalCase
        
    Examples:
        >>> to_pascal_case("hello_world")
        'HelloWorld'
        >>> to_pascal_case("some-variable-name")
        'SomeVariableName'
        >>> to_pascal_case("convert to pascal")
        'ConvertToPascal'
        >>> to_pascal_case("helloWorld")
        'HelloWorld'
        >>> to_pascal_case("XMLHttpRequest")
        'XmlHttpRequest'
        >>> to_pascal_case("__multiple__delimiters__")
        'MultipleDelimiters'
    """
    tokens = _tokenize_string(text)
    if not tokens:
        return ""
    
    return ''.join(token.capitalize() for token in tokens)


def to_kebab_case(text: str) -> str:
    """Convert a string to kebab-case.
    
    Args:
        text: Input string to convert
        
    Returns:
        String converted to kebab-case
        
    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("XMLHttpRequest")
        'xml-http-request'
        >>> to_kebab_case("some_variable_name")
        'some-variable-name'
        >>> to_kebab_case("multiple   spaces")
        'multiple-spaces'
        >>> to_kebab_case("--already--kebab--")
        'already-kebab'
    """
    tokens = _tokenize_string(text)
    if not tokens:
        return ""
    
    return '-'.join(token.lower() for token in tokens)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix.
    
    If the text needs truncation and max_length is too small to accommodate
    the suffix meaningfully, returns an empty string.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix (must be non-negative)
        suffix: String to append when truncating (default: "...")
        
    Returns:
        Truncated text with suffix if needed, empty string if max_length
        is too small for meaningful truncation
        
    Raises:
        ValueError: If max_length is negative
        
    Examples:
        >>> truncate_text("This is a long text", 10)
        'This is...'
        >>> truncate_text("Short", 10)
        'Short'
        >>> truncate_text("Exactly ten", 11)
        'Exactly ten'
        >>> truncate_text("Too long", -1)
        Traceback (most recent call last):
            ...
        ValueError: max_length must be non-negative, got -1
    """
    if max_length < 0:
        raise ValueError(f"max_length must be non-negative, got {max_length}")
    
    if len(text) <= max_length:
        return text
    
    # If max_length is too small for meaningful truncation, return empty
    if max_length < len(suffix) + 1:  # Need at least 1 char + suffix
        return ""
    
    return text[:max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """Count the number of words in a text.
    
    Words are defined as sequences of characters separated by whitespace.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
        
    Examples:
        >>> word_count("Hello world")
        2
        >>> word_count("  Multiple   spaces  ")
        2
        >>> word_count("")
        0
        >>> word_count("One-word")  # Hyphenated counts as one
        1
        >>> word_count("Line\\nbreak\\tand\\ttabs")
        3
    """
    if not text:
        return 0
    
    words = text.split()
    return len(words)


def is_mixed_case(text: str) -> bool:
    """Check if a string contains both uppercase and lowercase letters.
    
    Args:
        text: String to check
        
    Returns:
        True if string has both cases, False otherwise
        
    Examples:
        >>> is_mixed_case("HelloWorld")
        True
        >>> is_mixed_case("ALLCAPS")
        False
        >>> is_mixed_case("lowercase")
        False
        >>> is_mixed_case("noLetters123")
        False
    """
    has_upper = any(c.isupper() for c in text)
    has_lower = any(c.islower() for c in text)
    return has_upper and has_lower


def remove_extra_whitespace(text: str) -> str:
    """Remove extra whitespace from a string.
    
    Collapses multiple spaces into single spaces and trims
    leading/trailing whitespace.
    
    Args:
        text: Text to clean
        
    Returns:
        Text with normalized whitespace
        
    Examples:
        >>> remove_extra_whitespace("  Hello   world  ")
        'Hello world'
        >>> remove_extra_whitespace("Multiple\\n\\nlines")
        'Multiple lines'
        >>> remove_extra_whitespace("\\t\\tTabs\\t\\t")
        'Tabs'
    """
    if not text:
        return ""
    
    # Replace all whitespace sequences with single space
    text = _WHITESPACE.sub(' ', text)
    # Strip leading/trailing whitespace
    return text.strip()