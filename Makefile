# Makefile for Budget Manager
# Professional development workflow automation

.PHONY: help install install-dev test test-cov lint format type-check security clean build docs

help: ## Show this help message
	@echo "Budget Manager - Development Commands"
	@echo "======================================"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[dev]"
	pre-commit install

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=src/budget_manager --cov-report=html --cov-report=term

lint: ## Run linting checks
	flake8 src/ tests/
	black --check src/ tests/
	isort --check-only src/ tests/

format: ## Format code
	black src/ tests/
	isort src/ tests/

type-check: ## Run type checking
	mypy src/budget_manager/

security: ## Run security checks
	bandit -r src/ -ll
	safety check

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build package
	python -m build

docs: ## Generate documentation
	@echo "Documentation available in README.md"
	@echo "API documentation can be generated with: pdoc src/budget_manager/"

all: clean install-dev lint type-check test-cov ## Run all checks

demo: ## Run the demo
	./demo.sh

# Development workflow
dev-setup: install-dev ## Complete development setup
	@echo "Development environment ready!"
	@echo "Run 'make test' to verify installation"

check: lint type-check test ## Run all code checks

release-check: check build ## Prepare for release
	twine check dist/*
	@echo "Release ready! Remember to:"
	@echo "1. Update version in pyproject.toml"
	@echo "2. Update CHANGELOG.md"
	@echo "3. Create git tag: git tag v1.0.0"
	@echo "4. Push tag: git push origin v1.0.0"