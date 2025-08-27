"""Unit tests for the example module."""

import pytest
from src.example import greet, add_numbers


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
    
    def test_add_commutativity(self):
        """Test that addition is commutative."""
        assert add_numbers(3, 5) == add_numbers(5, 3)
        assert add_numbers(-2, 7) == add_numbers(7, -2)