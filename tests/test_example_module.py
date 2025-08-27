"""Unit tests for the example module."""

import pytest
import sys
from src.example import greet, add_numbers, safe_greet, _validate_string_input, _validate_integer_input


class TestGreetFunction:
    """Test suite for the greet function."""
    
    def test_greet_with_valid_name(self):
        """Test greet with a valid name."""
        result = greet("Alice")
        assert result == "Hello, Alice! Welcome to the Python uv template."
    
    def test_greet_with_empty_string(self):
        """Test greet with empty string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet("")
    
    def test_greet_with_whitespace_only(self):
        """Test greet with whitespace-only string raises ValueError."""
        with pytest.raises(ValueError, match="Name cannot be empty"):
            greet("   ")
    
    def test_greet_with_none(self):
        """Test greet with None raises TypeError."""
        with pytest.raises(TypeError, match="Name must be a string"):
            greet(None)
    
    def test_greet_with_number(self):
        """Test greet with number raises TypeError."""
        with pytest.raises(TypeError, match="Name must be a string"):
            greet(123)
    
    def test_greet_with_special_characters(self):
        """Test greet with name containing special characters."""
        result = greet("O'Neil")
        assert result == "Hello, O'Neil! Welcome to the Python uv template."
    
    def test_greet_with_unicode(self):
        """Test greet with Unicode characters."""
        result = greet("José")
        assert result == "Hello, José! Welcome to the Python uv template."
    
    def test_greet_strips_whitespace(self):
        """Test greet strips leading and trailing whitespace."""
        result = greet("  Bob  ")
        assert result == "Hello, Bob! Welcome to the Python uv template."


class TestAddNumbersFunction:
    """Test suite for the add_numbers function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add_numbers(2, 3) == 5
        assert add_numbers(10, 20) == 30
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers."""
        assert add_numbers(-5, -3) == -8
        assert add_numbers(-10, 5) == -5
    
    def test_add_zero(self):
        """Test adding with zero."""
        assert add_numbers(0, 5) == 5
        assert add_numbers(5, 0) == 5
        assert add_numbers(0, 0) == 0
    
    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add_numbers(1000000, 2000000) == 3000000
    
    def test_add_with_string_raises_error(self):
        """Test that strings raise TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers("5", 3)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, "3")
    
    def test_add_with_float_raises_error(self):
        """Test that floats raise TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5.5, 3)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, 3.5)
    
    def test_add_with_none_raises_error(self):
        """Test that None raises TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(None, 5)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, None)
    
    def test_add_with_boolean_raises_error(self):
        """Test that booleans raise TypeError (since bool is subclass of int)."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(True, 5)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, False)
    
    def test_add_with_list_raises_error(self):
        """Test that lists raise TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers([1, 2], 5)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, [3, 4])
    
    def test_add_with_dict_raises_error(self):
        """Test that dictionaries raise TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers({"a": 1}, 5)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, {"b": 2})
    
    def test_add_with_tuple_raises_error(self):
        """Test that tuples raise TypeError."""
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers((1, 2), 5)
        
        with pytest.raises(TypeError, match="Both arguments must be integers"):
            add_numbers(5, (3, 4))
    
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