# Example Module Documentation

This module demonstrates best practices for Python development with comprehensive validation, testing, and security measures.

## Features

- **Type Validation**: Strict type checking with helpful error messages
- **Input Sanitization**: Protection against injection attacks
- **XSS Prevention**: HTML escaping for web contexts
- **Error Recovery**: Safe wrapper functions with fallback behavior
- **Comprehensive Testing**: 52+ parameterized tests
- **Production Ready**: Logging, error handling, and documentation

## Usage

### Basic Usage

```python
from src.example import greet, add_numbers

# Greet a user
message = greet("Alice")
print(message)  # "Hello, Alice! Welcome to the Python uv template."

# Add numbers
result = add_numbers(5, 3)
print(result)  # 8
```

### Web-Safe Usage

```python
from src.example import greet_for_web

# Automatically escapes HTML to prevent XSS
safe_message = greet_for_web("<script>alert('XSS')</script>")
# Output: "Hello, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;! Welcome..."
```

### Error Recovery

```python
from src.example import safe_greet

# Falls back to default on invalid input
message = safe_greet(None)  # Uses "Guest" as default
print(message)  # "Hello, Guest! Welcome to the Python uv template."
```

## Running Tests

```bash
# Run all tests
uv run pytest tests/test_example_module.py -v

# Run with coverage
uv run pytest tests/test_example_module.py --cov=src

# Run doctests
uv run python src/example.py
```

## Security Considerations

1. **Input Validation**: All inputs are validated before processing
2. **XSS Prevention**: Use `greet_for_web()` for HTML contexts
3. **Error Messages**: Designed to be helpful without exposing internals
4. **Logging**: Errors logged for monitoring without exposing sensitive data

## Error Handling

The module provides clear error messages with helpful hints:

```python
>>> add_numbers(2.5, 3)
TypeError: First argument must be an integer. Received float instead. (value: 2.5). Please convert to integer if needed.

>>> greet("")
ValueError: Name cannot be empty or contain only whitespace.
```

## Contributing

When contributing to this module:
1. Maintain comprehensive type hints
2. Follow Google-style docstrings
3. Add tests for new functionality
4. Ensure security considerations are addressed
5. Update this documentation as needed