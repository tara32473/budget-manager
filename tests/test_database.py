"""
Unit tests for the database manager.
"""

import os
import tempfile
import unittest
from datetime import datetime, timedelta
from decimal import Decimal

from budget_manager.database import DatabaseManager
from budget_manager.models import Budget, Category, Transaction, TransactionType


class TestDatabaseManager(unittest.TestCase):
    """Test cases for DatabaseManager."""

    def setUp(self):
        """Set up test database."""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db = DatabaseManager(self.temp_db.name)

        # Create test category
        self.test_category = Category(name="Test Category", description="Test description")
        self.category_id = self.db.create_category(self.test_category)

    def tearDown(self):
        """Clean up test database."""
        os.unlink(self.temp_db.name)

    def test_create_and_get_category(self):
        """Test creating and retrieving a category."""
        # Create category
        category = Category(name="Food", description="Food expenses")
        category_id = self.db.create_category(category)

        # Retrieve category
        retrieved = self.db.get_category(category_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Food")
        self.assertEqual(retrieved.description, "Food expenses")

    def test_get_all_categories(self):
        """Test retrieving all categories."""
        # Should have at least the test category
        categories = self.db.get_all_categories()
        self.assertGreaterEqual(len(categories), 1)

        # Create another category
        category2 = Category(name="Transport", description="Transport expenses")
        self.db.create_category(category2)

        categories = self.db.get_all_categories()
        self.assertGreaterEqual(len(categories), 2)

    def test_update_category(self):
        """Test updating a category."""
        # Get the test category
        category = self.db.get_category(self.category_id)
        category.name = "Updated Category"
        category.description = "Updated description"

        # Update
        result = self.db.update_category(category)
        self.assertTrue(result)

        # Verify update
        updated = self.db.get_category(self.category_id)
        self.assertEqual(updated.name, "Updated Category")
        self.assertEqual(updated.description, "Updated description")

    def test_delete_category(self):
        """Test deleting a category."""
        # Create a category to delete
        category = Category(name="To Delete")
        category_id = self.db.create_category(category)

        # Delete it
        result = self.db.delete_category(category_id)
        self.assertTrue(result)

        # Verify deletion
        deleted = self.db.get_category(category_id)
        self.assertIsNone(deleted)

    def test_create_and_get_transaction(self):
        """Test creating and retrieving a transaction."""
        # Create transaction
        transaction = Transaction(
            amount=Decimal("50.00"),
            description="Test transaction",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
        )
        transaction_id = self.db.create_transaction(transaction)

        # Retrieve transaction
        retrieved = self.db.get_transaction(transaction_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.amount, Decimal("50.00"))
        self.assertEqual(retrieved.description, "Test transaction")
        self.assertEqual(retrieved.category_id, self.category_id)
        self.assertEqual(retrieved.transaction_type, TransactionType.EXPENSE)

    def test_get_transactions_with_filters(self):
        """Test retrieving transactions with various filters."""
        # Create test transactions
        t1 = Transaction(
            amount=Decimal("25.00"),
            description="Transaction 1",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
            date=datetime.now() - timedelta(days=1),
        )
        t2 = Transaction(
            amount=Decimal("100.00"),
            description="Transaction 2",
            category_id=self.category_id,
            transaction_type=TransactionType.INCOME,
            date=datetime.now(),
        )

        self.db.create_transaction(t1)
        self.db.create_transaction(t2)

        # Test filter by category
        transactions = self.db.get_transactions(category_id=self.category_id)
        self.assertGreaterEqual(len(transactions), 2)

        # Test filter by type
        expense_transactions = self.db.get_transactions(transaction_type=TransactionType.EXPENSE)
        income_transactions = self.db.get_transactions(transaction_type=TransactionType.INCOME)

        self.assertGreater(len(expense_transactions), 0)
        self.assertGreater(len(income_transactions), 0)

        # Test date filtering
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_transactions = self.db.get_transactions(start_date=today)
        self.assertGreater(len(today_transactions), 0)

    def test_update_transaction(self):
        """Test updating a transaction."""
        # Create transaction
        transaction = Transaction(
            amount=Decimal("30.00"),
            description="Original description",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
        )
        transaction_id = self.db.create_transaction(transaction)

        # Update transaction
        transaction.amount = Decimal("35.00")
        transaction.description = "Updated description"
        result = self.db.update_transaction(transaction)
        self.assertTrue(result)

        # Verify update
        updated = self.db.get_transaction(transaction_id)
        self.assertEqual(updated.amount, Decimal("35.00"))
        self.assertEqual(updated.description, "Updated description")

    def test_delete_transaction(self):
        """Test deleting a transaction."""
        # Create transaction
        transaction = Transaction(
            amount=Decimal("20.00"),
            description="To delete",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
        )
        transaction_id = self.db.create_transaction(transaction)

        # Delete it
        result = self.db.delete_transaction(transaction_id)
        self.assertTrue(result)

        # Verify deletion
        deleted = self.db.get_transaction(transaction_id)
        self.assertIsNone(deleted)

    def test_create_and_get_budget(self):
        """Test creating and retrieving a budget."""
        # Create budget
        budget = Budget(category_id=self.category_id, amount=Decimal("200.00"), period="monthly")
        budget_id = self.db.create_budget(budget)

        # Retrieve budget
        retrieved = self.db.get_budget(budget_id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.category_id, self.category_id)
        self.assertEqual(retrieved.amount, Decimal("200.00"))
        self.assertEqual(retrieved.period, "monthly")

    def test_get_budgets_with_filters(self):
        """Test retrieving budgets with filters."""
        # Create budgets
        budget1 = Budget(
            category_id=self.category_id, amount=Decimal("100.00"), period="monthly", is_active=True
        )
        budget2 = Budget(
            category_id=self.category_id, amount=Decimal("50.00"), period="weekly", is_active=False
        )

        self.db.create_budget(budget1)
        self.db.create_budget(budget2)

        # Test filter by category
        budgets = self.db.get_budgets(category_id=self.category_id)
        self.assertGreaterEqual(len(budgets), 1)

        # Test filter by active status
        active_budgets = self.db.get_budgets(is_active=True)
        inactive_budgets = self.db.get_budgets(is_active=False)

        self.assertGreater(len(active_budgets), 0)
        self.assertGreater(len(inactive_budgets), 0)

    def test_budget_summary(self):
        """Test budget summary calculation."""
        # Create budget starting 10 days ago to ensure transactions are within period
        budget_start = datetime.now() - timedelta(days=10)
        budget = Budget(
            category_id=self.category_id,
            amount=Decimal("100.00"),
            period="monthly",
            start_date=budget_start,
        )
        budget_id = self.db.create_budget(budget)
        budget = self.db.get_budget(budget_id)

        # Create some transactions within the budget period
        t1 = Transaction(
            amount=Decimal("30.00"),
            description="Expense 1",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
            date=budget_start + timedelta(days=3),
        )
        t2 = Transaction(
            amount=Decimal("20.00"),
            description="Expense 2",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
            date=budget_start + timedelta(days=5),
        )

        self.db.create_transaction(t1)
        self.db.create_transaction(t2)

        # Get budget summary
        summary = self.db.get_budget_summary(budget)

        self.assertEqual(summary.spent_amount, Decimal("50.00"))
        self.assertEqual(summary.remaining_amount, Decimal("50.00"))
        self.assertEqual(summary.percentage_used, 50.0)
        self.assertFalse(summary.is_over_budget)
        self.assertEqual(summary.transaction_count, 2)

    def test_spending_by_category(self):
        """Test spending by category analysis."""
        # Create another category
        category2 = Category(name="Transport")
        category2_id = self.db.create_category(category2)

        # Create transactions in different categories
        t1 = Transaction(
            amount=Decimal("50.00"),
            description="Food expense",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
        )
        t2 = Transaction(
            amount=Decimal("30.00"),
            description="Transport expense",
            category_id=category2_id,
            transaction_type=TransactionType.EXPENSE,
        )

        self.db.create_transaction(t1)
        self.db.create_transaction(t2)

        # Get spending by category
        spending = self.db.get_spending_by_category()

        self.assertIn("Test Category", spending)
        self.assertIn("Transport", spending)
        self.assertEqual(spending["Test Category"], Decimal("50.00"))
        self.assertEqual(spending["Transport"], Decimal("30.00"))

    def test_income_vs_expenses(self):
        """Test income vs expenses analysis."""
        # Create income and expense transactions
        income = Transaction(
            amount=Decimal("1000.00"),
            description="Salary",
            category_id=self.category_id,
            transaction_type=TransactionType.INCOME,
        )
        expense = Transaction(
            amount=Decimal("300.00"),
            description="Groceries",
            category_id=self.category_id,
            transaction_type=TransactionType.EXPENSE,
        )

        self.db.create_transaction(income)
        self.db.create_transaction(expense)

        # Get income vs expenses
        result = self.db.get_income_vs_expenses()

        self.assertGreaterEqual(result["income"], Decimal("1000.00"))
        self.assertGreaterEqual(result["expense"], Decimal("300.00"))
        self.assertGreaterEqual(result["net"], Decimal("700.00"))


if __name__ == "__main__":
    unittest.main()
