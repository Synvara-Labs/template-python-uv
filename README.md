# Python uv Template 🐍

A modern Python project template using [uv](https://github.com/astral-sh/uv) for ultra-fast package management.

## ✨ Features

### 🚀 Package Management
- **Lightning Fast**: uv provides 10-100x faster package resolution than pip
- **Built-in Python**: Automatic Python version management
- **Lock Files**: Reproducible builds with `uv.lock`
- **Virtual Environments**: Automatic `.venv` creation and management

### 🔒 Security & Quality
- **CodeQL Analysis**: Automated security vulnerability scanning
- **Dependency Review**: Checks for vulnerable or malicious dependencies  
- **Input Validation**: Example module with comprehensive validation
- **XSS Prevention**: HTML escaping demonstrations for web contexts

### 🧪 Testing & CI/CD
- **52+ Tests**: Comprehensive test suite with parameterized testing
- **GitHub Actions**: Automated CI pipeline with multiple checks
- **Code Quality**: Pre-configured for ruff, black, and mypy
- **PR Automation**: Auto-labeling and release drafting

### 📦 Example Module
Includes a production-ready example module demonstrating:
- Type hints and validation
- Google-style docstrings
- Error handling with helpful messages
- Security best practices
- CLI interface

## 🚀 Quick Start

### Prerequisites
Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup
1. **Clone and install dependencies:**
   ```bash
   git clone <your-repo>
   cd <your-repo>
   uv sync --all-extras --dev
   ```

2. **Run tests:**
   ```bash
   uv run pytest
   ```

3. **Try the example module:**
   ```bash
   # Run interactive demo
   uv run python src/example.py
   
   # Use CLI interface
   uv run python src/cli.py greet "Your Name"
   uv run python src/cli.py add 10 20
   ```

## 📋 GitHub Workflows

| Workflow | Purpose | Trigger |
|----------|---------|---------|
| **CI** | Run tests and quality checks | Push, PR |
| **CodeQL** | Security vulnerability scanning | Push, PR, Schedule |
| **Dependency Review** | Check for vulnerable dependencies | PR |
| **PR Labeler** | Auto-label PRs based on files changed | PR |
| **Release Drafter** | Generate release notes automatically | Push to main |

## 🛠️ Development

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_example_module.py -v
```

### Code Quality
```bash
# Linting with ruff
uv run ruff check .

# Formatting with black
uv run black .

# Type checking with mypy
uv run mypy .
```

### Project Structure
```
.
├── .github/
│   ├── workflows/       # CI/CD workflows
│   └── labeler.yml      # PR labeling config
├── src/
│   ├── __init__.py
│   ├── example.py       # Example module with best practices
│   ├── cli.py           # CLI interface
│   └── README.md        # Module documentation
├── tests/
│   └── test_example_module.py  # Comprehensive test suite
├── pyproject.toml       # Project configuration
└── uv.lock             # Locked dependencies
```

## 🔧 Configuration

### Required GitHub Settings
1. **Enable GitHub Actions** (Settings → Actions)
2. **Enable Dependabot** (Settings → Security & analysis)
3. **Set up branch protection** for `main`:
   - Require PR reviews
   - Require status checks to pass
   - Require branches to be up to date

### Optional Enhancements
- [ ] Add CODEOWNERS file for automatic PR reviewers
- [ ] Configure GitHub Pages for documentation
- [ ] Set up PyPI publishing workflow
- [ ] Add Docker support

## 📚 Example Module Documentation

The template includes a fully-featured example module demonstrating:

### Input Validation
```python
from src.example import greet, add_numbers

# Type-safe functions with validation
greeting = greet("Alice")  # ✓ Valid
greeting = greet("")       # ✗ Raises ValueError
result = add_numbers(5, 3) # ✓ Valid  
result = add_numbers(5.5, 3) # ✗ Raises TypeError with helpful message
```

### Security Features
```python
from src.example import greet_for_web

# Automatic HTML escaping for web contexts
safe_output = greet_for_web("<script>alert('XSS')</script>")
# Output: "Hello, &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;..."
```

### Error Recovery
```python
from src.example import safe_greet

# Graceful fallback on errors
message = safe_greet(None)  # Returns "Hello, Guest!" instead of raising
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`uv run pytest`)
5. Commit with conventional commits (`git commit -m 'feat: Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This template is open source and available under the MIT License.

## 🙏 Acknowledgments

- [uv](https://github.com/astral-sh/uv) - Ultra-fast Python package manager
- [pytest](https://pytest.org) - Testing framework
- [ruff](https://github.com/astral-sh/ruff) - Fast Python linter
- GitHub Actions for CI/CD automation

---

Built with ❤️ using modern Python tooling