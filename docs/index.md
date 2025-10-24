# Budget Manager Documentation

Welcome to the comprehensive documentation for Budget Manager - a professional personal finance CLI application.

**Author**: tara32473  
**GitHub**: https://github.com/tara32473/budget-manager

## 📚 Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](installation.md) - Complete setup instructions
3. [Usage Guide](usage.md) - Comprehensive user manual  
4. [API Reference](api.md) - Developer documentation
5. [Examples](#examples)
6. [Contributing](#contributing)

## 🚀 Getting Started

Budget Manager is a command-line application for tracking personal finances, managing budgets, and generating financial reports. Built with Python and SQLite, it provides a robust foundation for financial data management.

### Key Features

- **Transaction Management**: Add, edit, and categorize income/expense transactions
- **Budget Tracking**: Set monthly budgets and monitor spending against limits
- **Comprehensive Reporting**: Generate detailed financial summaries and analytics
- **Data Persistence**: SQLite database for reliable data storage
- **Professional CLI**: Clean, intuitive command-line interface
- **Type Safety**: Full type hints for better code reliability

## 💻 Installation

### Requirements
- Python 3.8 or higher
- SQLite (included with Python)

### Quick Install
```bash
# Clone the repository
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager

# Install the package
pip install -e .

# Verify installation
budget --help
```

### Development Installation
```bash
# Install with development dependencies
pip install -e .
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Docker Installation
```bash
# Build the image
docker build -t budget-manager .

# Run the application
docker run -it --rm budget-manager --help
```

## 📖 Usage Guide

### Basic Commands

#### Managing Categories
```bash
# Add a new category
budget add-category "Food" "Groceries and dining"

# List all categories
budget list-categories

# Remove a category
budget remove-category "Food"
```

#### Recording Transactions
```bash
# Add an expense
budget add-transaction expense 50.00 "Food" "Lunch at restaurant"

# Add income
budget add-transaction income 3000.00 "Salary" "Monthly paycheck"

# List transactions
budget list-transactions

# List transactions for specific month
budget list-transactions --month 2025-10
```

#### Budget Management
```bash
# Set a monthly budget
budget set-budget "Food" 500.00

# View budget status
budget budget-status

# Check overspending
budget budget-status --warnings-only
```

#### Financial Reports
```bash
# Monthly summary
budget report monthly

# Yearly overview
budget report yearly

# Custom date range
budget report --start-date 2025-01-01 --end-date 2025-03-31
```

### Advanced Features

#### Data Export
```bash
# Export transactions to CSV
budget export-transactions transactions.csv

# Export with date filter
budget export-transactions --start-date 2025-01-01 data.csv
```

#### Database Management
```bash
# Database statistics
budget stats

# Backup database
cp data/budget_manager.db backups/budget_$(date +%Y%m%d).db
```

## 🔧 API Reference

### Core Models

#### Transaction
```python
@dataclass
class Transaction:
    id: str
    date: datetime
    type: TransactionType  # income or expense
    amount: Decimal
    category_id: str
    description: str
    created_at: datetime
```

#### Category
```python
@dataclass
class Category:
    id: str
    name: str
    description: str
    created_at: datetime
```

#### Budget
```python
@dataclass
class Budget:
    id: str
    category_id: str
    amount: Decimal
    month: str  # YYYY-MM format
    created_at: datetime
```

### Database Operations

#### DatabaseManager Methods
- `create_tables()`: Initialize database schema
- `add_transaction()`: Insert new transaction
- `get_transactions()`: Retrieve transactions with filters
- `add_category()`: Create new category
- `set_budget()`: Configure monthly budget
- `get_budget_status()`: Check budget utilization

### CLI Interface

All commands are available through the `budget` command:

```bash
budget [command] [options] [arguments]
```

Use `budget --help` or `budget [command] --help` for detailed usage information.

## 📊 Examples

### Quick Demo
Run the quick demonstration:
```bash
./examples/quick_demo.sh
```

### Portfolio Demo
Comprehensive 6-month financial scenario:
```bash
./examples/portfolio_demo.sh
```

### Performance Testing
Test with large datasets:
```bash
./examples/performance_demo.sh
```

### Real-World Scenarios

#### Monthly Budget Setup
```bash
# Set up typical monthly budgets
budget add-category "Housing" "Rent and utilities"
budget add-category "Food" "Groceries and dining"
budget add-category "Transport" "Gas and maintenance"
budget add-category "Entertainment" "Movies and hobbies"

budget set-budget "Housing" 2000.00
budget set-budget "Food" 600.00
budget set-budget "Transport" 300.00
budget set-budget "Entertainment" 200.00
```

#### Expense Tracking
```bash
# Record regular expenses
budget add-transaction expense 2000.00 "Housing" "Monthly rent"
budget add-transaction expense 85.00 "Food" "Weekly groceries"
budget add-transaction expense 45.00 "Transport" "Gas fill-up"
budget add-transaction expense 25.00 "Entertainment" "Movie tickets"

# Check budget status
budget budget-status
```

#### Monthly Review
```bash
# Generate comprehensive monthly report
budget report monthly

# Check for overspending
budget budget-status --warnings-only

# Export data for spreadsheet analysis
budget export-transactions monthly_data.csv --month $(date +%Y-%m)
```

## 🏗️ Architecture

### Project Structure
```
budget-manager/
├── src/budget_manager/     # Core application
│   ├── models.py          # Data models and types
│   ├── database.py        # SQLite operations
│   ├── cli.py            # Command-line interface
│   └── reports.py        # Report generation
├── tests/                # Test suite
├── examples/            # Demo scripts
├── .github/            # CI/CD workflows
└── docs/              # Documentation
```

### Design Principles

1. **Separation of Concerns**: Clear boundaries between data, business logic, and presentation
2. **Type Safety**: Comprehensive type hints throughout the codebase
3. **Testability**: High test coverage with unit and integration tests
4. **User Experience**: Clean, intuitive CLI with helpful error messages
5. **Data Integrity**: Proper validation and constraint handling

### Technology Stack

- **Language**: Python 3.8+
- **Database**: SQLite with optimized queries
- **CLI Framework**: argparse with custom enhancements
- **Testing**: pytest with comprehensive coverage
- **Code Quality**: Black, Flake8, isort, mypy
- **CI/CD**: GitHub Actions with multi-version testing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Development setup
- Code standards
- Testing requirements
- Pull request process

### Quick Contributing Steps
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run quality checks: `make lint test`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [GitHub Pages](https://tara32473.github.io/budget-manager/)
- **Issues**: [GitHub Issues](https://github.com/tara32473/budget-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tara32473/budget-manager/discussions)

---

Built with ❤️ using Python • [View on GitHub](https://github.com/tara32473/budget-manager)