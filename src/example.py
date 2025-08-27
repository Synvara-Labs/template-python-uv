"""Example module to demonstrate the template functionality."""


def greet(name: str) -> str:
    """
    Return a greeting message.
    
    Args:
        name: The name to greet
        
    Returns:
        A greeting message string
    """
    return f"Hello, {name}! Welcome to the Python uv template."


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


if __name__ == "__main__":
    print(greet("Developer"))
    print(f"2 + 3 = {add_numbers(2, 3)}")