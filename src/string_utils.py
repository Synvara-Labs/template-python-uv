"""String manipulation utilities for common text transformations.

This module provides functions for converting between different text cases
commonly used in programming and documentation.
"""

import re
from typing import List


def to_snake_case(text: str) -> str:
    """Convert a string to snake_case.
    
    Args:
        text: Input string to convert
        
    Returns:
        String converted to snake_case
        
    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("someVariableName")
        'some_variable_name'
        >>> to_snake_case("convert-to-snake")
        'convert_to_snake'
    """
    # Replace hyphens and spaces with underscores
    text = re.sub(r'[-\s]+', '_', text)
    # Insert underscore before capital letters (including consecutive caps)
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
    # Convert to lowercase
    return text.lower()


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
    """
    # Split on non-alphanumeric characters
    words = re.split(r'[_\-\s]+', text)
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
    """
    # Split on non-alphanumeric characters
    words = re.split(r'[_\-\s]+', text)
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
        >>> to_kebab_case("some_variable_name")
        'some-variable-name'
        >>> to_kebab_case("Convert To Kebab")
        'convert-to-kebab'
    """
    # Replace underscores and spaces with hyphens
    text = re.sub(r'[_\s]+', '-', text)
    # Insert hyphen before capital letters (including consecutive caps)
    text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', text)
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)
    # Convert to lowercase
    return text.lower()


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncating (default: "...")
        
    Returns:
        Truncated text with suffix if needed
        
    Examples:
        >>> truncate_text("This is a long text", 10)
        'This is...'
        >>> truncate_text("Short", 10)
        'Short'
        >>> truncate_text("Exactly ten", 11)
        'Exactly ten'
    """
    if len(text) <= max_length:
        return text
    
    if max_length <= len(suffix):
        return suffix[:max_length]
    
    return text[:max_length - len(suffix)] + suffix


def word_count(text: str) -> int:
    """Count the number of words in a text.
    
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
    """
    words = text.split()
    return len(words)