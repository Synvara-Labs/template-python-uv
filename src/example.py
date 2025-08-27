"""Example module to demonstrate the template functionality."""


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
    # Type validation
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    
    # Strip whitespace and check for empty string
    name = name.strip()
    if not name:
        raise ValueError("Name cannot be empty")
    
    return f"Hello, {name}! Welcome to the Python uv template."


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
    """
    # Type validation - strict integer check (excludes floats and bools)
    if type(a) is not int:
        raise TypeError("Both arguments must be integers")
    if type(b) is not int:
        raise TypeError("Both arguments must be integers")
    
    return a + b


if __name__ == "__main__":
    print(greet("Developer"))
    print(f"2 + 3 = {add_numbers(2, 3)}")