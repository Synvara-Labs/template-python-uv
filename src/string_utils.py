"""String manipulation utilities for common text transformations.

This module provides functions for converting between different text cases
commonly used in programming and documentation.
"""

import re


# Precompile regex patterns for better performance
_CONSECUTIVE_CAPS = re.compile(r'([A-Z]+)([A-Z][a-z])')
_CAMEL_BOUNDARY = re.compile(r'([a-z0-9])([A-Z])')
_NON_ALNUM = re.compile(r'[^a-zA-Z0-9]+')
_WHITESPACE = re.compile(r'\s+')


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
    if not text:
        return ""
    
    # Replace non-alphanumeric with underscores
    text = _NON_ALNUM.sub('_', text)
    
    # Handle consecutive capitals
    text = _CONSECUTIVE_CAPS.sub(r'\1_\2', text)
    
    # Insert underscore before capitals preceded by lowercase/digit
    text = _CAMEL_BOUNDARY.sub(r'\1_\2', text)
    
    # Convert to lowercase and remove redundant underscores
    text = text.lower()
    text = re.sub(r'_+', '_', text)  # Collapse multiple underscores
    text = text.strip('_')  # Remove leading/trailing underscores
    
    return text


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
        >>> to_camel_case("__multiple__delimiters__")
        'multipleDelimiters'
        >>> to_camel_case("123_start_with_number")
        '123StartWithNumber'
    """
    if not text:
        return ""
    
    # Split on non-alphanumeric characters
    words = _NON_ALNUM.split(text)
    # Filter empty strings
    words = [w for w in words if w]
    
    if not words:
        return ""
    
    # First word lowercase, rest title case
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])


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
        >>> to_pascal_case("__multiple__delimiters__")
        'MultipleDelimiters'
        >>> to_pascal_case("123_start_with_number")
        '123StartWithNumber'
    """
    if not text:
        return ""
    
    # Split on non-alphanumeric characters
    words = _NON_ALNUM.split(text)
    # Filter empty strings and capitalize each word
    return ''.join(w.capitalize() for w in words if w)


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
    if not text:
        return ""
    
    # Replace non-alphanumeric with hyphens
    text = _NON_ALNUM.sub('-', text)
    
    # Handle consecutive capitals
    text = _CONSECUTIVE_CAPS.sub(r'\1-\2', text)
    
    # Insert hyphen before capitals preceded by lowercase/digit
    text = _CAMEL_BOUNDARY.sub(r'\1-\2', text)
    
    # Convert to lowercase and clean up hyphens
    text = text.lower()
    text = re.sub(r'-+', '-', text)  # Collapse multiple hyphens
    text = text.strip('-')  # Remove leading/trailing hyphens
    
    return text


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix.
    
    If the text needs truncation and max_length is too small to accommodate
    the suffix meaningfully, returns an empty string.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncating (default: "...")
        
    Returns:
        Truncated text with suffix if needed, empty string if max_length
        is too small for meaningful truncation
        
    Examples:
        >>> truncate_text("This is a long text", 10)
        'This is...'
        >>> truncate_text("Short", 10)
        'Short'
        >>> truncate_text("Exactly ten", 11)
        'Exactly ten'
        >>> truncate_text("Too long", 2, "...")
        ''
        >>> truncate_text("Custom", 5, "→")
        'Cust→'
    """
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