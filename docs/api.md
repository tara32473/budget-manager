# API Reference

Complete API documentation for Budget Manager components.

## Core Models

### Transaction

```python
@dataclass
class Transaction:
    id: str                    # Unique identifier (UUID)
    date: datetime            # Transaction date
    type: TransactionType     # "income" or "expense"
    amount: Decimal          # Transaction amount (precision preserved)
    category_id: str         # Reference to category
    description: str         # User description
    created_at: datetime     # Record creation timestamp
```

**Methods:**
- `to_dict()` - Convert to dictionary representation
- `from_dict(data: Dict)` - Create from dictionary (class method)

### Category

```python
@dataclass
class Category:
    id: str              # Unique identifier (UUID)
    name: str           # Category name (e.g., "Food", "Transport")
    description: str    # Detailed description
    created_at: datetime # Record creation timestamp
```

**Methods:**
- `to_dict()` - Convert to dictionary representation
- `from_dict(data: Dict)` - Create from dictionary (class method)

### Budget

```python
@dataclass
class Budget:
    id: str              # Unique identifier (UUID)
    category_id: str     # Reference to category
    amount: Decimal     # Budget amount for the month
    month: str          # Month in YYYY-MM format
    created_at: datetime # Record creation timestamp
```

**Methods:**
- `to_dict()` - Convert to dictionary representation
- `from_dict(data: Dict)` - Create from dictionary (class method)

## Database Manager

### DatabaseManager Class

Primary interface for all database operations.

```python
class DatabaseManager:
    def __init__(self, db_path: str = "data/budget_manager.db")
```

#### Core Methods

**Transaction Operations:**
```python
def add_transaction(self, transaction_type: str, amount: Decimal, 
                   category_id: str, description: str, 
                   date: Optional[datetime] = None) -> str

def get_transactions(self, limit: Optional[int] = None, 
                    category_id: Optional[str] = None,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Transaction]

def update_transaction(self, transaction_id: str, **kwargs) -> bool

def delete_transaction(self, transaction_id: str) -> bool
```

**Category Operations:**
```python
def add_category(self, name: str, description: str = "") -> str

def get_categories(self) -> List[Category]

def get_category_by_name(self, name: str) -> Optional[Category]

def update_category(self, category_id: str, **kwargs) -> bool

def delete_category(self, category_id: str) -> bool
```

**Budget Operations:**
```python
def set_budget(self, category_id: str, amount: Decimal, 
               month: Optional[str] = None) -> str

def get_budgets(self, month: Optional[str] = None) -> List[Budget]

def get_budget_status(self, month: Optional[str] = None) -> Dict[str, Any]
```

**Utility Methods:**
```python
def get_monthly_summary(self, month: str) -> Dict[str, Any]

def get_yearly_summary(self, year: int) -> Dict[str, Any]

def export_transactions(self, filepath: str, **filters) -> None

def get_database_stats() -> Dict[str, int]
```

## CLI Interface

### Command Structure

All CLI commands follow the pattern:
```bash
budget [global-options] <command> [command-options] [arguments]
```

### Global Options
- `--db-path PATH` - Specify database location
- `--verbose` - Enable verbose output
- `--help` - Show help information

### Commands Reference

#### Transaction Management
```bash
# Add transactions
budget add-transaction <type> <amount> <category> <description>
budget add-transaction income 3000.00 "Salary" "Monthly paycheck"
budget add-transaction expense 45.50 "Food" "Lunch restaurant"

# List transactions  
budget list-transactions [--limit N] [--category NAME] [--month YYYY-MM]

# Update transaction
budget update-transaction <id> [--amount AMOUNT] [--description DESC]

# Delete transaction
budget delete-transaction <id>
```

#### Category Management
```bash
# Add category
budget add-category <name> [description]
budget add-category "Entertainment" "Movies, games, hobbies"

# List categories
budget list-categories

# Update category
budget update-category <name> [--new-name NAME] [--description DESC]

# Remove category
budget remove-category <name>
```

#### Budget Management
```bash
# Set budget
budget set-budget <category> <amount> [--month YYYY-MM]
budget set-budget "Food" 500.00 --month 2025-10

# Check budget status
budget budget-status [--month YYYY-MM] [--warnings-only]
```

#### Reporting
```bash
# Generate reports
budget report <type> [options]
budget report monthly [--month YYYY-MM]
budget report yearly [--year YYYY]
budget report custom --start-date YYYY-MM-DD --end-date YYYY-MM-DD

# Export data
budget export-transactions <filepath> [filters]
```

#### Utility Commands
```bash
# Database statistics
budget stats

# Initialize fresh database
budget init-db [--force]
```

## Report Generator

### ReportGenerator Class

Handles all financial reporting and analytics.

```python
class ReportGenerator:
    def __init__(self, db_manager: DatabaseManager)
```

#### Methods

```python
def generate_monthly_report(self, month: str) -> str
def generate_yearly_report(self, year: int) -> str  
def generate_custom_report(self, start_date: datetime, 
                          end_date: datetime) -> str
def generate_budget_status_report(self, month: str) -> str
def generate_category_breakdown(self, month: str) -> Dict[str, Decimal]
```

## Error Handling

### Custom Exceptions

```python
class BudgetManagerError(Exception):
    """Base exception for Budget Manager"""

class DatabaseError(BudgetManagerError):
    """Database operation errors"""

class ValidationError(BudgetManagerError):
    """Data validation errors"""

class CategoryError(BudgetManagerError):
    """Category-related errors"""
```

### Error Codes

- `BM001`: Database connection error
- `BM002`: Invalid transaction data
- `BM003`: Category not found
- `BM004`: Budget already exists
- `BM005`: Invalid date format

## Data Validation

### Input Validation Rules

**Amounts:**
- Must be positive Decimal values
- Maximum 2 decimal places
- Range: 0.01 to 999,999,999.99

**Dates:**
- ISO format: YYYY-MM-DD
- Must not be future dates for transactions
- Month format: YYYY-MM

**Text Fields:**
- Category names: 1-50 characters, alphanumeric + spaces
- Descriptions: 1-200 characters
- No HTML or special characters

**IDs:**
- UUID format validation
- Existence checks for foreign keys

## Database Schema

### Tables

**transactions:**
```sql
CREATE TABLE transactions (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    amount TEXT NOT NULL,  -- Stored as string for Decimal precision
    category_id TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
```

**categories:**
```sql
CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

**budgets:**
```sql
CREATE TABLE budgets (
    id TEXT PRIMARY KEY,
    category_id TEXT NOT NULL,
    amount TEXT NOT NULL,
    month TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(category_id, month),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
```

### Indices

- `idx_transactions_date` - On transactions.date for report performance
- `idx_transactions_category` - On transactions.category_id for filtering
- `idx_budgets_month` - On budgets.month for monthly queries

---

[← Back to Documentation Home](index.md)