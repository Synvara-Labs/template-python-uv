"""Example module to demonstrate the template functionality with robust validation."""

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
        ValueError: If value is empty after stripping whitespace.
    """
    if not isinstance(value, str):
        error_msg = f"{param_name} must be a string, got {type(value).__name__}"
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    # Strip whitespace and check for empty string
    sanitized = value.strip()
    if not sanitized:
        error_msg = f"{param_name} cannot be empty"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return sanitized


def _validate_integer_input(value: Any, param_name: str) -> int:
    """Validate integer input with strict type checking.
    
    Helper function to ensure input is exactly an integer type.
    
    Args:
        value: The value to validate.
        param_name: Name of the parameter for error messages.
    
    Returns:
        The validated integer value.
    
    Raises:
        TypeError: If value is not exactly an integer type.
    """
    if type(value) is not int:
        error_msg = f"{param_name} must be an integer, got {type(value).__name__}"
        logger.error(error_msg)
        raise TypeError(error_msg)
    
    return value


def greet(name: str) -> str:
    """Return a personalized greeting message.
    
    This function creates a welcome message for the given name. It includes
    input validation to ensure the name is a valid non-empty string.
    
    Args:
        name: The name of the person to greet. Must be a non-empty string.
            Leading and trailing whitespace will be stripped.
    
    Returns:
        A formatted greeting message string.
    
    Raises:
        TypeError: If name is not a string.
        ValueError: If name is empty or contains only whitespace.
    
    Examples:
        >>> greet("Alice")
        'Hello, Alice! Welcome to the Python uv template.'
        
        >>> greet("  Bob  ")
        'Hello, Bob! Welcome to the Python uv template.'
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
    to ensure both arguments are integers (not floats or other types).
    
    Args:
        a: The first integer to add.
        b: The second integer to add.
    
    Returns:
        The sum of a and b as an integer.
    
    Raises:
        TypeError: If either a or b is not an integer.
    
    Examples:
        >>> add_numbers(2, 3)
        5
        
        >>> add_numbers(-5, 10)
        5
        
        >>> add_numbers(0, 0)
        0
    
    Note:
        Python 3 has unlimited integer precision, so overflow is not a concern.
    """
    try:
        validated_a = _validate_integer_input(a, "First argument")
        validated_b = _validate_integer_input(b, "Second argument")
        return validated_a + validated_b
    except TypeError:
        # Log and re-raise with more specific message
        error_msg = "Both arguments must be integers"
        logger.error(f"Type validation failed: {error_msg}")
        raise TypeError(error_msg)


def safe_greet(name: str, default: str = "Guest") -> str:
    """Safely greet a user with fallback to default.
    
    This function provides a safe wrapper around greet() with error recovery.
    
    Args:
        name: The name to greet.
        default: Default name to use if validation fails.
    
    Returns:
        A greeting message string.
    
    Examples:
        >>> safe_greet("Alice")
        'Hello, Alice! Welcome to the Python uv template.'
        
        >>> safe_greet("")
        'Hello, Guest! Welcome to the Python uv template.'
    """
    try:
        return greet(name)
    except (TypeError, ValueError) as e:
        logger.warning(f"Invalid input for greeting, using default: {e}")
        return greet(default)


if __name__ == "__main__":
    # Example usage with error handling
    try:
        print(greet("Developer"))
        print(f"2 + 3 = {add_numbers(2, 3)}")
        
        # Demonstrate safe_greet
        print(safe_greet(""))  # Will use default "Guest"
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"Error: {e}")