# Email Validation Guide

## Overview

The `validators` module provides robust email validation functionality that follows RFC 5322 standards while maintaining security and performance. This guide covers common use cases, best practices, and implementation examples.

## Quick Start

```python
from src.validators import validate_email_format

# Basic validation
if validate_email_format("user@example.com"):
    print("Valid email!")
else:
    print("Invalid email format")
```

## Features

### Core Capabilities
- ✅ RFC 5322 compliant validation
- ✅ Security-conscious error handling
- ✅ Performance optimized (<1ms per validation)
- ✅ Batch validation support
- ✅ Comprehensive edge case handling
- ✅ Safe for untrusted input

### What It Validates
- Proper email structure (local@domain.tld)
- Valid characters in local and domain parts
- Length constraints (max 254 total, max 64 local)
- No consecutive dots
- Valid TLD (2+ characters)
- Proper @ symbol usage

### What It Doesn't Do
- ❌ Check if email actually exists
- ❌ Verify deliverability
- ❌ DNS/MX record validation
- ❌ SMTP verification

## Usage Examples

### Basic Validation

```python
from src.validators import validate_email_format

# Simple validation
email = "john.doe@company.com"
is_valid = validate_email_format(email)
print(f"{email} is {'valid' if is_valid else 'invalid'}")

# Handle user input
user_email = input("Enter your email: ").strip()
try:
    if validate_email_format(user_email):
        print("Thank you! Email accepted.")
    else:
        print("Please enter a valid email address.")
except TypeError:
    print("Invalid input type.")
```

### Form Validation

```python
def process_registration_form(form_data):
    """Example form processing with email validation."""
    email = form_data.get("email", "")
    
    # Validate email format
    if not validate_email_format(email):
        return {
            "success": False,
            "error": "Please provide a valid email address"
        }
    
    # Proceed with registration
    return {
        "success": True,
        "message": "Registration successful"
    }
```

### Batch Processing

```python
from src.validators import validate_email_batch

# Validate multiple emails at once
email_list = [
    "valid@example.com",
    "another.valid@test.org",
    "not-an-email",
    "user@domain.co.uk",
    ""  # Empty string
]

results = validate_email_batch(email_list)

# Filter valid emails
valid_emails = [email for email, is_valid in results.items() if is_valid]
invalid_emails = [email for email, is_valid in results.items() if not is_valid]

print(f"Valid emails: {valid_emails}")
print(f"Invalid emails: {invalid_emails}")
```

### Data Cleaning

```python
import pandas as pd
from src.validators import validate_email_format

def clean_email_dataset(df):
    """Clean and validate emails in a pandas DataFrame."""
    # Add validation column
    df['email_valid'] = df['email'].apply(
        lambda x: validate_email_format(x) if isinstance(x, str) else False
    )
    
    # Get statistics
    valid_count = df['email_valid'].sum()
    total_count = len(df)
    
    print(f"Valid emails: {valid_count}/{total_count} "
          f"({valid_count/total_count*100:.1f}%)")
    
    # Option 1: Filter out invalid emails
    df_clean = df[df['email_valid']].copy()
    
    # Option 2: Mark but keep invalid emails
    df['email_status'] = df['email_valid'].map({
        True: 'valid',
        False: 'invalid'
    })
    
    return df
```

### API Endpoint Validation

```python
from flask import Flask, request, jsonify
from src.validators import validate_email_format

app = Flask(__name__)

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    """API endpoint with email validation."""
    data = request.get_json()
    email = data.get('email', '')
    
    # Validate email
    try:
        if not validate_email_format(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
    except TypeError:
        return jsonify({
            'success': False,
            'error': 'Email must be a string'
        }), 400
    
    # Process subscription
    # ... subscription logic here ...
    
    return jsonify({
        'success': True,
        'message': f'Successfully subscribed {email}'
    })
```

### Custom Validation Rules

```python
from src.validators import validate_email_format

def validate_corporate_email(email, allowed_domains=None):
    """
    Validate email with additional corporate rules.
    
    Args:
        email: Email address to validate
        allowed_domains: List of allowed domains (e.g., ['company.com'])
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # First check basic format
    if not validate_email_format(email):
        return False, "Invalid email format"
    
    # Additional corporate rules
    if allowed_domains:
        domain = email.split('@')[1].lower()
        if domain not in allowed_domains:
            return False, f"Email must be from domains: {', '.join(allowed_domains)}"
    
    # Check for disposable email providers
    disposable_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com']
    domain = email.split('@')[1].lower()
    if domain in disposable_domains:
        return False, "Disposable email addresses are not allowed"
    
    return True, "Valid corporate email"

# Usage
result, message = validate_corporate_email(
    "john@company.com",
    allowed_domains=['company.com', 'subsidiary.com']
)
print(message)
```

### Testing and Validation

```python
import pytest
from src.validators import validate_email_format

def test_email_validation():
    """Example test cases for email validation."""
    # Valid emails
    valid_emails = [
        "user@example.com",
        "first.last@domain.org",
        "user+tag@company.co.uk",
        "test123@sub.domain.com"
    ]
    
    for email in valid_emails:
        assert validate_email_format(email) is True, f"Failed: {email}"
    
    # Invalid emails
    invalid_emails = [
        "",  # Empty
        "not-an-email",  # No @
        "@example.com",  # No local part
        "user@",  # No domain
        "user@domain",  # No TLD
        "user..name@example.com",  # Consecutive dots
    ]
    
    for email in invalid_emails:
        assert validate_email_format(email) is False, f"Should fail: {email}"

# Run tests
if __name__ == "__main__":
    test_email_validation()
    print("All tests passed!")
```

## Common Patterns

### Safe User Input Handling

```python
def get_valid_email_from_user():
    """Safely get a valid email from user input."""
    max_attempts = 3
    
    for attempt in range(max_attempts):
        user_input = input("Please enter your email: ").strip()
        
        try:
            if validate_email_format(user_input):
                return user_input
            else:
                print("Invalid email format. Please try again.")
        except TypeError:
            print("Invalid input. Please enter a text string.")
    
    raise ValueError("Maximum attempts exceeded")
```

### Logging Invalid Emails

```python
import logging
from src.validators import validate_email_format

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_email_with_logging(email):
    """Process email with validation logging."""
    try:
        if validate_email_format(email):
            logger.info(f"Valid email processed: {email[:3]}***")  # Partial log for privacy
            return True
        else:
            logger.warning(f"Invalid email format rejected: {email[:3]}***")
            return False
    except TypeError as e:
        logger.error(f"Type error in email validation: {e}")
        return False
```

## Best Practices

### Do's ✅
- Always validate user input before processing
- Use try-except for type safety with untrusted input
- Strip whitespace from user input
- Log validation failures for monitoring (without full email)
- Provide clear user feedback

### Don'ts ❌
- Don't assume validation means email exists
- Don't log full email addresses (privacy concern)
- Don't expose detailed error messages to end users
- Don't skip validation for "trusted" sources
- Don't use email validation for authentication

## Migration from Deprecated Functions

If you're using the deprecated `is_valid_email` function:

```python
# Old code (deprecated)
from src.validators import is_valid_email
result = is_valid_email("test@example.com")

# New code (recommended)
from src.validators import validate_email_format
result = validate_email_format("test@example.com")
```

## Performance Considerations

- Single validation: <1ms typical
- Batch of 1000: <1 second
- No regex backtracking issues
- Safe for user-facing applications

## Security Notes

1. **Input Sanitization**: The validator safely handles malicious input
2. **Error Messages**: Generic errors don't expose system details
3. **No Code Execution**: Email strings are never evaluated
4. **DoS Protection**: No regex patterns that cause exponential backtracking

## Limitations

- Doesn't verify email deliverability
- No support for quoted local parts (rare but RFC-valid)
- No support for IP address domains
- No internationalized domain name (IDN) support in non-Punycode form

## Future Enhancements

Planned features for future versions:
- DNS MX record validation
- SMTP verification option
- Parallel batch processing
- Internationalized email support
- Disposable email detection

## Support

For issues, questions, or contributions, please refer to the project repository.