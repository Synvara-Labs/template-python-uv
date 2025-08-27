"""Example module to demonstrate the template functionality with robust validation.

Security Note:
    This module implements input validation and sanitization. If using in web contexts,
    additional XSS prevention measures should be applied at the presentation layer
    (e.g., HTML escaping, Content Security Policy headers).
"""

import html
import logging
from typing import Any

# Configure logging for error handling
logger = logging.getLogger(__name__)


def _validate_string_input(value: Any, param_name: str) -> str:
    """Validate and sanitize string input.
    
    Helper function to validate string inputs and provide consistent error handling.
    
    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.
    
    Returns:
        Sanitized string value.
    
    Raises:
        TypeError: If value is not a string.
        ValueError: If value is empty or contains only whitespace.
    """
    if not isinstance(value, str):
        error_msg = f"{param_name} must be a string. Received {type(value).__name__} instead."
        logger.error(f"Type validation failed: {error_msg}")
        raise TypeError(error_msg)
    
    # Explicit whitespace validation
    if not value or value.isspace():
        error_msg = f"{param_name} cannot be empty or contain only whitespace."
        logger.error(f"Value validation failed: {error_msg}")
        raise ValueError(error_msg)
    
    # Strip whitespace for sanitization
    sanitized = value.strip()
    if not sanitized:  # Double-check after stripping
        error_msg = f"{param_name} cannot be empty after removing whitespace."
        logger.error(f"Value validation failed: {error_msg}")
        raise ValueError(error_msg)
    
    return sanitized


def _validate_integer_input(value: Any, param_name: str) -> int:
    """Validate integer input with flexible type checking.
    
    Helper function to ensure input is an integer or integer-compatible type.
    Uses isinstance for flexibility with integer subclasses while excluding booleans.
    
    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.
    
    Returns:
        The validated integer value.
    
    Raises:
        TypeError: If value is not an integer or is a boolean.
    """
    # Check for boolean first (since bool is a subclass of int)
    if isinstance(value, bool):
        error_msg = f"{param_name} must be an integer. Received boolean instead."
        logger.error(f"Type validation failed: {error_msg}")
        raise TypeError(error_msg)
    
    # Now check for integer (allows int subclasses)
    if not isinstance(value, int):
        received_type = type(value).__name__
        error_msg = f"{param_name} must be an integer. Received {received_type} instead."
        if isinstance(value, float):
            error_msg += f" (value: {value}). Please convert to integer if needed."
        logger.error(f"Type validation failed: {error_msg}")
        raise TypeError(error_msg)
    
    return value


def greet(name: str) -> str:
    """Return a personalized greeting message.
    
    This function creates a welcome message for the given name. It includes
    input validation to ensure the name is a valid non-empty string.
    
    Security Note:
        For web contexts, the output should be HTML-escaped to prevent XSS attacks.
        Use html.escape() or template engine auto-escaping when rendering.
    
    Args:
        name: The name of the person to greet. Must be a non-empty string.
            Leading and trailing whitespace will be stripped.
    
    Returns:
        A formatted greeting message string (not HTML-escaped).
    
    Raises:
        TypeError: If name is not a string.
        ValueError: If name is empty or contains only whitespace.
    
    Examples:
        >>> greet("Alice")
        'Hello, Alice! Welcome to the Python uv template.'
        
        >>> greet("  Bob  ")
        'Hello, Bob! Welcome to the Python uv template.'
        
        >>> # For web context (not done automatically):
        >>> html.escape(greet("Alice"))
        'Hello, Alice! Welcome to the Python uv template.'
    """
    try:
        sanitized_name = _validate_string_input(name, "Name")
        return f"Hello, {sanitized_name}! Welcome to the Python uv template."
    except (TypeError, ValueError) as e:
        # Re-raise with original exception for proper error propagation
        raise


def add_numbers(a: int, b: int) -> int:
    """Add two integer numbers together.
    
    This function performs addition of two integers with type validation
    to ensure both arguments are integers (excluding booleans but allowing int subclasses).
    
    Args:
        a: The first integer to add.
        b: The second integer to add.
    
    Returns:
        The sum of a and b as an integer.
    
    Raises:
        TypeError: If either a or b is not an integer. Provides helpful messages
                  for common mistakes like passing floats.
    
    Examples:
        >>> add_numbers(2, 3)
        5
        
        >>> add_numbers(-5, 10)
        5
        
        >>> add_numbers(0, 0)
        0
        
        >>> # This will raise TypeError with helpful message:
        >>> # add_numbers(2.5, 3)
        >>> # TypeError: First argument must be an integer. Received float instead. (value: 2.5). Please convert to integer if needed.
    
    Note:
        Python 3 has unlimited integer precision, so overflow is not a concern.
    """
    try:
        validated_a = _validate_integer_input(a, "First argument")
        validated_b = _validate_integer_input(b, "Second argument")
        return validated_a + validated_b
    except TypeError as e:
        # Re-raise with the detailed error message from validation
        raise


def safe_greet(name: str, default: str = "Guest") -> str:
    """Safely greet a user with fallback to default.
    
    This function provides a safe wrapper around greet() with error recovery.
    Useful in contexts where graceful degradation is preferred over exceptions.
    
    Args:
        name: The name to greet.
        default: Default name to use if validation fails (default: "Guest").
    
    Returns:
        A greeting message string.
    
    Examples:
        >>> safe_greet("Alice")
        'Hello, Alice! Welcome to the Python uv template.'
        
        >>> safe_greet("")  # Falls back to default
        'Hello, Guest! Welcome to the Python uv template.'
        
        >>> safe_greet(None)  # Falls back to default
        'Hello, Guest! Welcome to the Python uv template.'
    """
    try:
        return greet(name)
    except (TypeError, ValueError) as e:
        logger.warning(f"Invalid input for greeting, using default: {e}")
        return greet(default)


def greet_for_web(name: str) -> str:
    """Return an HTML-safe personalized greeting message.
    
    This function is specifically designed for web contexts where XSS prevention
    is critical. It automatically HTML-escapes the output.
    
    Args:
        name: The name of the person to greet. Must be a non-empty string.
    
    Returns:
        An HTML-escaped greeting message safe for web rendering.
    
    Raises:
        TypeError: If name is not a string.
        ValueError: If name is empty or contains only whitespace.
    
    Examples:
        >>> greet_for_web("Alice")
        'Hello, Alice! Welcome to the Python uv template.'
        
        >>> greet_for_web("<script>alert('XSS')</script>")
        'Hello, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;! Welcome to the Python uv template.'
    """
    greeting = greet(name)
    return html.escape(greeting)


if __name__ == "__main__":
    # Example usage with error handling
    try:
        print(greet("Developer"))
        print(f"2 + 3 = {add_numbers(2, 3)}")
        
        # Demonstrate safe_greet
        print(safe_greet(""))  # Will use default "Guest"
        
        # Demonstrate web-safe greeting
        print("Web-safe:", greet_for_web("<script>alert('test')</script>"))
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"Error: {e}")