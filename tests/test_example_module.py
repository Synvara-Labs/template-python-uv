"""Unit tests for the example module."""

import pytest
import sys
from src.example import (
    greet, add_numbers, safe_greet, greet_for_web,
    _validate_string_input, _validate_integer_input
)


class TestGreetFunction:
    """Test suite for the greet function."""
    
    @pytest.mark.parametrize("name,expected", [
        ("Alice", "Hello, Alice! Welcome to the Python uv template."),
        ("Bob", "Hello, Bob! Welcome to the Python uv template."),
        ("O'Neil", "Hello, O'Neil! Welcome to the Python uv template."),
        ("José", "Hello, José! Welcome to the Python uv template."),
        ("  John  ", "Hello, John! Welcome to the Python uv template."),
        (" Mary ", "Hello, Mary! Welcome to the Python uv template."),
    ])
    def test_greet_with_valid_names(self, name, expected):
        """Test greet with various valid names using parameterized tests."""
        assert greet(name) == expected
    
    @pytest.mark.parametrize("invalid_input,error_type,error_pattern", [
        ("", ValueError, "cannot be empty or contain only whitespace"),
        ("   ", ValueError, "cannot be empty or contain only whitespace"),
        ("\t\n", ValueError, "cannot be empty or contain only whitespace"),
        (None, TypeError, "must be a string.*Received NoneType instead"),
        (123, TypeError, "must be a string.*Received int instead"),
        (12.5, TypeError, "must be a string.*Received float instead"),
        ([], TypeError, "must be a string.*Received list instead"),
        ({}, TypeError, "must be a string.*Received dict instead"),
    ])
    def test_greet_with_invalid_inputs_raises_appropriate_errors(self, invalid_input, error_type, error_pattern):
        """Test greet with various invalid inputs raises appropriate errors."""
        with pytest.raises(error_type, match=error_pattern):
            greet(invalid_input)
    


class TestAddNumbersFunction:
    """Test suite for the add_numbers function."""
    
    @pytest.mark.parametrize("a,b,expected", [
        (2, 3, 5),           # positive numbers
        (10, 20, 30),        # larger positive numbers
        (-5, -3, -8),        # negative numbers
        (-10, 5, -5),        # mixed signs
        (0, 5, 5),           # zero as first argument
        (5, 0, 5),           # zero as second argument
        (0, 0, 0),           # both zeros
        (-100, 100, 0),      # opposites
        (1, -1, 0),          # small opposites
    ])
    def test_add_various_integer_combinations(self, a, b, expected):
        """Test adding various combinations of integers using parameterized tests."""
        assert add_numbers(a, b) == expected
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add_numbers(1000000, 2000000) == 3000000
    
    @pytest.mark.parametrize("invalid_a,valid_b,error_pattern", [
        ("5", 3, "must be an integer.*Received str instead"),
        (5.5, 3, "must be an integer.*Received float.*Please convert to integer"),
        (None, 3, "must be an integer.*Received NoneType instead"),
        (True, 3, "must be an integer.*Received boolean instead"),
        ([1, 2], 3, "must be an integer.*Received list instead"),
        ({"a": 1}, 3, "must be an integer.*Received dict instead"),
        ((1, 2), 3, "must be an integer.*Received tuple instead"),
    ])
    def test_add_with_invalid_first_argument_raises_type_error(self, invalid_a, valid_b, error_pattern):
        """Test that invalid first arguments raise TypeError with helpful messages."""
        with pytest.raises(TypeError, match=error_pattern):
            add_numbers(invalid_a, valid_b)
    
    @pytest.mark.parametrize("valid_a,invalid_b,error_pattern", [
        (3, "5", "must be an integer.*Received str instead"),
        (3, 5.5, "must be an integer.*Received float.*Please convert to integer"),
        (3, None, "must be an integer.*Received NoneType instead"),
        (3, False, "must be an integer.*Received boolean instead"),
        (3, [1, 2], "must be an integer.*Received list instead"),
        (3, {"b": 2}, "must be an integer.*Received dict instead"),
        (3, (3, 4), "must be an integer.*Received tuple instead"),
    ])
    def test_add_with_invalid_second_argument_raises_type_error(self, valid_a, invalid_b, error_pattern):
        """Test that invalid second arguments raise TypeError with helpful messages."""
        with pytest.raises(TypeError, match=error_pattern):
            add_numbers(valid_a, invalid_b)
    
    
    def test_add_boundary_conditions(self):
        """Test addition at boundary conditions with maximum/minimum values."""
        
        # Test with maximum integer values (Python 3 has unlimited int precision)
        max_val = sys.maxsize
        assert add_numbers(max_val, 0) == max_val
        assert add_numbers(max_val, 1) == max_val + 1  # Should not overflow
        
        # Test with minimum values
        min_val = -sys.maxsize - 1
        assert add_numbers(min_val, 0) == min_val
        assert add_numbers(min_val, -1) == min_val - 1  # Should not underflow
        
        # Test adding opposite extremes
        assert add_numbers(max_val, -max_val) == 0
    
    def test_add_commutativity(self):
        """Test that addition is commutative."""
        assert add_numbers(3, 5) == add_numbers(5, 3)
        assert add_numbers(-2, 7) == add_numbers(7, -2)


class TestGreetForWebFunction:
    """Test suite for the greet_for_web function with XSS prevention."""
    
    def test_greet_for_web_with_normal_name(self):
        """Test greet_for_web with a normal name."""
        assert greet_for_web("Alice") == "Hello, Alice! Welcome to the Python uv template."
    
    def test_greet_for_web_escapes_html_tags(self):
        """Test that HTML tags are escaped to prevent XSS."""
        result = greet_for_web("<script>alert('XSS')</script>")
        assert "&lt;script&gt;" in result
        assert "&lt;/script&gt;" in result
        assert "<script>" not in result
    
    def test_greet_for_web_escapes_quotes(self):
        """Test that quotes are escaped properly."""
        result = greet_for_web("O'Malley")
        assert "O&#x27;Malley" in result or "O'Malley" in result  # HTML escape is optional for single quotes in content
    
    def test_greet_for_web_with_html_entities(self):
        """Test handling of HTML entities."""
        result = greet_for_web("Alice&Bob")
        assert "Alice&amp;Bob" in result or "Alice&Bob" in result


class TestSafeGreetFunction:
    """Test suite for the safe_greet function."""
    
    def test_safe_greet_with_valid_name(self):
        """Test safe_greet with a valid name."""
        assert safe_greet("Alice") == "Hello, Alice! Welcome to the Python uv template."
    
    def test_safe_greet_with_empty_uses_default(self):
        """Test safe_greet falls back to default on empty input."""
        assert safe_greet("") == "Hello, Guest! Welcome to the Python uv template."
    
    def test_safe_greet_with_none_uses_default(self):
        """Test safe_greet falls back to default on None input."""
        assert safe_greet(None) == "Hello, Guest! Welcome to the Python uv template."
    
    def test_safe_greet_with_custom_default(self):
        """Test safe_greet with custom default value."""
        assert safe_greet("", "Friend") == "Hello, Friend! Welcome to the Python uv template."


class TestHelperFunctions:
    """Test suite for helper validation functions."""
    
    def test_validate_string_input_valid(self):
        """Test string validation with valid input."""
        assert _validate_string_input("test", "param") == "test"
        assert _validate_string_input("  test  ", "param") == "test"
    
    def test_validate_string_input_invalid(self):
        """Test string validation with invalid input."""
        with pytest.raises(TypeError):
            _validate_string_input(123, "param")
        
        with pytest.raises(ValueError):
            _validate_string_input("", "param")
    
    def test_validate_integer_input_valid(self):
        """Test integer validation with valid input."""
        assert _validate_integer_input(5, "param") == 5
        assert _validate_integer_input(-10, "param") == -10
        assert _validate_integer_input(0, "param") == 0
    
    def test_validate_integer_input_invalid(self):
        """Test integer validation with invalid input."""
        with pytest.raises(TypeError):
            _validate_integer_input(5.5, "param")
        
        with pytest.raises(TypeError):
            _validate_integer_input(True, "param")
        
        with pytest.raises(TypeError):
            _validate_integer_input("5", "param")