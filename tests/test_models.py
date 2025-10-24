"""
Unit tests for the budget manager models.
"""

import unittest
from datetime import datetime
from decimal import Decimal

from budget_manager.models import Category, Transaction, Budget, TransactionType, BudgetSummary


class TestCategory(unittest.TestCase):
    """Test cases for Category model."""
    
    def test_create_category(self):
        """Test creating a valid category."""
        category = Category(name="Food", description="Food and dining expenses")
        self.assertEqual(category.name, "Food")
        self.assertEqual(category.description, "Food and dining expenses")
        self.assertIsNotNone(category.id)
        self.assertIsInstance(category.created_at, datetime)
    
    def test_category_requires_name(self):
        """Test that category requires a name."""
        with self.assertRaises(ValueError):
            Category(name="")
    
    def test_category_optional_fields(self):
        """Test that optional fields work correctly."""
        category = Category(name="Transport", color="#FF0000")
        self.assertEqual(category.name, "Transport")
        self.assertEqual(category.color, "#FF0000")
        self.assertIsNone(category.description)


class TestTransaction(unittest.TestCase):
    """Test cases for Transaction model."""
    
    def test_create_transaction(self):
        """Test creating a valid transaction."""
        transaction = Transaction(
            amount=Decimal('25.50'),
            description="Lunch at restaurant",
            transaction_type=TransactionType.EXPENSE
        )
        self.assertEqual(transaction.amount, Decimal('25.50'))
        self.assertEqual(transaction.description, "Lunch at restaurant")
        self.assertEqual(transaction.transaction_type, TransactionType.EXPENSE)
        self.assertIsNotNone(transaction.id)
        self.assertIsInstance(transaction.date, datetime)
    
    def test_transaction_requires_description(self):
        """Test that transaction requires a description."""
        with self.assertRaises(ValueError):
            Transaction(amount=Decimal('10.00'), description="")
    
    def test_transaction_requires_positive_amount(self):
        """Test that transaction amount must be positive."""
        with self.assertRaises(ValueError):
            Transaction(amount=Decimal('0'), description="Test")
        
        with self.assertRaises(ValueError):
            Transaction(amount=Decimal('-10.00'), description="Test")
    
    def test_amount_precision(self):
        """Test that amount is correctly formatted to 2 decimal places."""
        transaction = Transaction(amount=Decimal('10.1'), description="Test")
        self.assertEqual(transaction.amount, Decimal('10.10'))
        
        transaction2 = Transaction(amount=Decimal('10.999'), description="Test")
        self.assertEqual(transaction2.amount, Decimal('11.00'))


class TestBudget(unittest.TestCase):
    """Test cases for Budget model."""
    
    def test_create_budget(self):
        """Test creating a valid budget."""
        budget = Budget(
            category_id="test-category-id",
            amount=Decimal('500.00'),
            period="monthly"
        )
        self.assertEqual(budget.category_id, "test-category-id")
        self.assertEqual(budget.amount, Decimal('500.00'))
        self.assertEqual(budget.period, "monthly")
        self.assertTrue(budget.is_active)
        self.assertIsNotNone(budget.end_date)
    
    def test_budget_requires_category_id(self):
        """Test that budget requires a category_id."""
        with self.assertRaises(ValueError):
            Budget(category_id="", amount=Decimal('100.00'))
    
    def test_budget_requires_positive_amount(self):
        """Test that budget amount must be positive."""
        with self.assertRaises(ValueError):
            Budget(category_id="test", amount=Decimal('0'))
        
        with self.assertRaises(ValueError):
            Budget(category_id="test", amount=Decimal('-100.00'))
    
    def test_budget_end_date_calculation(self):
        """Test that end_date is calculated correctly based on period."""
        start_date = datetime(2024, 1, 15)
        
        # Monthly budget
        monthly_budget = Budget(
            category_id="test",
            amount=Decimal('100.00'),
            period="monthly",
            start_date=start_date
        )
        expected_end = datetime(2024, 2, 1)
        self.assertEqual(monthly_budget.end_date, expected_end)
        
        # Weekly budget
        weekly_budget = Budget(
            category_id="test",
            amount=Decimal('100.00'),
            period="weekly",
            start_date=start_date
        )
        expected_end = datetime(2024, 1, 22)
        self.assertEqual(weekly_budget.end_date, expected_end)
        
        # Yearly budget
        yearly_budget = Budget(
            category_id="test",
            amount=Decimal('1000.00'),
            period="yearly",
            start_date=start_date
        )
        expected_end = datetime(2025, 1, 1)
        self.assertEqual(yearly_budget.end_date, expected_end)


class TestBudgetSummary(unittest.TestCase):
    """Test cases for BudgetSummary model."""
    
    def test_budget_summary_calculations(self):
        """Test that budget summary calculations are correct."""
        budget = Budget(
            category_id="test",
            amount=Decimal('100.00'),
            period="monthly"
        )
        
        summary = BudgetSummary(
            budget=budget,
            spent_amount=Decimal('75.00'),
            transaction_count=5
        )
        
        self.assertEqual(summary.remaining_amount, Decimal('25.00'))
        self.assertEqual(summary.percentage_used, 75.0)
        self.assertFalse(summary.is_over_budget)
        self.assertEqual(summary.transaction_count, 5)
    
    def test_over_budget_detection(self):
        """Test that over budget condition is detected correctly."""
        budget = Budget(
            category_id="test",
            amount=Decimal('100.00'),
            period="monthly"
        )
        
        summary = BudgetSummary(
            budget=budget,
            spent_amount=Decimal('125.00')
        )
        
        self.assertEqual(summary.remaining_amount, Decimal('-25.00'))
        self.assertEqual(summary.percentage_used, 125.0)
        self.assertTrue(summary.is_over_budget)


if __name__ == '__main__':
    unittest.main()