"""
Integration tests for the CLI interface.
"""

import unittest
import tempfile
import os
import sys
from io import StringIO
from unittest.mock import patch

# Add src directory to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from budget_manager.cli import BudgetManagerCLI
from budget_manager.database import DatabaseManager


class TestBudgetManagerCLI(unittest.TestCase):
    """Test cases for the CLI interface."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        
        # Initialize CLI with test database
        self.cli = BudgetManagerCLI(self.temp_db.name)
        
        # Capture stdout for testing output
        self.held, sys.stdout = sys.stdout, StringIO()
    
    def tearDown(self):
        """Clean up test environment."""
        sys.stdout = self.held
        os.unlink(self.temp_db.name)
    
    def get_output(self):
        """Get captured stdout output."""
        return sys.stdout.getvalue()
    
    def test_add_category_command(self):
        """Test adding a category via CLI."""
        # Mock command line arguments
        test_args = ['add-category', 'Food', 'Food and dining expenses']
        
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.add_category(args)
        
        output = self.get_output()
        self.assertIn("Category 'Food' created successfully", output)
        
        # Verify category was created in database
        categories = self.cli.db.get_all_categories()
        food_categories = [c for c in categories if c.name == 'Food']
        self.assertEqual(len(food_categories), 1)
        self.assertEqual(food_categories[0].description, 'Food and dining expenses')
    
    def test_list_categories_command(self):
        """Test listing categories via CLI."""
        # Add some test categories
        test_args1 = ['add-category', 'Food', 'Food expenses']
        test_args2 = ['add-category', 'Transport', 'Transport expenses']
        
        with patch('sys.argv', ['budget'] + test_args1):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args1)
            self.cli.add_category(args)
        
        with patch('sys.argv', ['budget'] + test_args2):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args2)
            self.cli.add_category(args)
        
        # Clear previous output
        sys.stdout = StringIO()
        
        # List categories
        test_args = ['list-categories']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.list_categories(args)
        
        output = self.get_output()
        self.assertIn('Food', output)
        self.assertIn('Transport', output)
    
    def test_add_transaction_command(self):
        """Test adding a transaction via CLI."""
        # First add a category
        test_args_cat = ['add-category', 'Food', 'Food expenses']
        with patch('sys.argv', ['budget'] + test_args_cat):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_cat)
            self.cli.add_category(args)
        
        # Clear output
        sys.stdout = StringIO()
        
        # Add transaction
        test_args = ['add-transaction', '-a', '25.50', '-d', 'Lunch', '-c', 'Food', 'expense']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.add_transaction(args)
        
        output = self.get_output()
        self.assertIn("Transaction added successfully", output)
        
        # Verify transaction was created
        transactions = self.cli.db.get_transactions(limit=1)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].description, 'Lunch')
        self.assertEqual(str(transactions[0].amount), '25.50')
    
    def test_set_budget_command(self):
        """Test setting a budget via CLI."""
        # First add a category
        test_args_cat = ['add-category', 'Food', 'Food expenses']
        with patch('sys.argv', ['budget'] + test_args_cat):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_cat)
            self.cli.add_category(args)
        
        # Clear output
        sys.stdout = StringIO()
        
        # Set budget
        test_args = ['set-budget', 'Food', '500.00', 'monthly']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.set_budget(args)
        
        output = self.get_output()
        self.assertIn("Budget set for 'Food': $500.00 (monthly)", output)
        
        # Verify budget was created
        budgets = self.cli.db.get_budgets()
        self.assertEqual(len(budgets), 1)
        self.assertEqual(str(budgets[0].amount), '500.00')
        self.assertEqual(budgets[0].period, 'monthly')
    
    def test_list_transactions_command(self):
        """Test listing transactions via CLI."""
        # Add category and transactions
        test_args_cat = ['add-category', 'Food', 'Food expenses']
        with patch('sys.argv', ['budget'] + test_args_cat):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_cat)
            self.cli.add_category(args)
        
        # Add some transactions
        test_args_t1 = ['add-transaction', '-a', '25.00', '-d', 'Breakfast', '-c', 'Food', 'expense']
        test_args_t2 = ['add-transaction', '-a', '50.00', '-d', 'Dinner', '-c', 'Food', 'expense']
        
        with patch('sys.argv', ['budget'] + test_args_t1):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_t1)
            self.cli.add_transaction(args)
        
        with patch('sys.argv', ['budget'] + test_args_t2):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_t2)
            self.cli.add_transaction(args)
        
        # Clear output
        sys.stdout = StringIO()
        
        # List transactions
        test_args = ['list-transactions', '--limit', '10']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.list_transactions(args)
        
        output = self.get_output()
        self.assertIn('Breakfast', output)
        self.assertIn('Dinner', output)
        self.assertIn('$25.00', output)
        self.assertIn('$50.00', output)
    
    def test_error_handling_invalid_category(self):
        """Test error handling for invalid category names."""
        # Try to add transaction with non-existent category
        test_args = ['add-transaction', '-a', '25.00', '-d', 'Test', '-c', 'NonExistent', 'expense']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.add_transaction(args)
        
        output = self.get_output()
        self.assertIn("Category 'NonExistent' not found", output)
    
    def test_error_handling_invalid_amount(self):
        """Test error handling for invalid amount formats."""
        # Add category first
        test_args_cat = ['add-category', 'Food', 'Food expenses']
        with patch('sys.argv', ['budget'] + test_args_cat):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args_cat)
            self.cli.add_category(args)
        
        # Clear output
        sys.stdout = StringIO()
        
        # Try to add transaction with invalid amount
        test_args = ['add-transaction', '-a', 'invalid', '-d', 'Test', '-c', 'Food', 'expense']
        with patch('sys.argv', ['budget'] + test_args):
            parser = self.cli.create_parser()
            args = parser.parse_args(test_args)
            self.cli.add_transaction(args)
        
        output = self.get_output()
        self.assertIn("Invalid amount 'invalid'", output)


if __name__ == '__main__':
    unittest.main()