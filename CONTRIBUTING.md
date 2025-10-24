# Contributing to Budget Manager

Thank you for your interest in contributing to Budget Manager! This document provides guidelines and instructions for contributing.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/budget-manager.git
   cd budget-manager
   ```

3. **Set up development environment**
   ```bash
   # Install in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -r requirements.txt
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Run tests**
   ```bash
   pytest
   ```

## 🛠️ Development Workflow

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for public APIs
- Maintain test coverage above 90%

### Testing
- Write tests for new features
- Run the full test suite: `pytest`
- Check coverage: `pytest --cov=budget_manager`

### Code Quality Tools
We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/
```

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `refactor:` for code refactoring

Example: `feat: add export to CSV functionality`

## 📋 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**
   ```bash
   make test
   make lint
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear title and description
   - Reference any related issues
   - Ensure all CI checks pass

## 🐛 Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment information (OS, Python version)
- Error messages or screenshots

## 💡 Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Provide clear use cases
- Explain the expected behavior
- Consider implementation complexity

## 🏗️ Project Structure

```
budget-manager/
├── src/budget_manager/          # Main application code
│   ├── models.py               # Data models
│   ├── database.py             # Database operations
│   ├── cli.py                  # Command-line interface
│   └── reports.py              # Report generation
├── tests/                      # Test suite
├── examples/                   # Demo scripts
├── .github/                    # GitHub workflows
└── docs/                       # Documentation
```

## 🔧 Available Make Commands

```bash
make test          # Run tests
make coverage      # Run tests with coverage
make lint          # Run all linters
make format        # Format code
make clean         # Clean build artifacts
make install       # Install in development mode
make docker-build  # Build Docker image
make demo          # Run demonstration
```

## 📞 Getting Help

- Check the [README](README.md) for basic usage
- Browse [existing issues](https://github.com/tara32473/budget-manager/issues)
- Run examples in the `examples/` directory
- Join discussions in issue comments

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Budget Manager! 🎉