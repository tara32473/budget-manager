"""
Core data models for the budget manager application.

This module defines the main data structures used throughout the application:
- Transaction: Individual financial transactions (income/expense)
- Category: Spending/income categories for organization
- Budget: Budget limits for different categories
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid


class TransactionType(Enum):
    """Enumeration for transaction types."""
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Category:
    """Represents a spending or income category."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: Optional[str] = None
    color: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Category name is required")


@dataclass
class Transaction:
    """Represents a financial transaction (income or expense)."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    amount: Decimal = Decimal('0.00')
    description: str = ""
    category_id: Optional[str] = None
    transaction_type: TransactionType = TransactionType.EXPENSE
    date: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None
    
    def __post_init__(self):
        if not self.description:
            raise ValueError("Transaction description is required")
        if self.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        # Ensure amount is a Decimal with 2 decimal places
        self.amount = Decimal(str(self.amount)).quantize(Decimal('0.01'))


@dataclass
class Budget:
    """Represents a budget limit for a category."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    category_id: str = ""
    amount: Decimal = Decimal('0.00')
    period: str = "monthly"  # monthly, weekly, yearly
    start_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True
    
    def __post_init__(self):
        if not self.category_id:
            raise ValueError("Budget category_id is required")
        if self.amount <= 0:
            raise ValueError("Budget amount must be positive")
        # Ensure amount is a Decimal with 2 decimal places
        self.amount = Decimal(str(self.amount)).quantize(Decimal('0.01'))
        
        # Set default end_date based on period if not provided
        if not self.end_date:
            if self.period == "monthly":
                # Set to end of the month
                if self.start_date.month == 12:
                    self.end_date = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)
                else:
                    self.end_date = self.start_date.replace(month=self.start_date.month + 1, day=1)
            elif self.period == "weekly":
                # Set to 7 days from start
                from datetime import timedelta
                self.end_date = self.start_date + timedelta(days=7)
            elif self.period == "yearly":
                # Set to end of the year
                self.end_date = self.start_date.replace(year=self.start_date.year + 1, month=1, day=1)


@dataclass
class BudgetSummary:
    """Summary of budget performance."""
    budget: Budget
    spent_amount: Decimal = Decimal('0.00')
    remaining_amount: Decimal = Decimal('0.00')
    percentage_used: float = 0.0
    is_over_budget: bool = False
    transaction_count: int = 0
    
    def __post_init__(self):
        self.remaining_amount = self.budget.amount - self.spent_amount
        if self.budget.amount > 0:
            self.percentage_used = float(self.spent_amount / self.budget.amount * 100)
        self.is_over_budget = self.spent_amount > self.budget.amount