"""
Command-line interface for the budget manager application.

This module provides a comprehensive CLI for managing personal finances,
including transactions, categories, budgets, and generating reports.
"""

import argparse
import sys
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from typing import Optional

from .database import DatabaseManager
from .models import Transaction, Category, Budget, TransactionType
from .reports import ReportGenerator


class BudgetManagerCLI:
    """Main CLI class for the budget manager application."""
    
    def __init__(self, db_path: str = None):
        """Initialize CLI with database manager."""
        self.db = DatabaseManager(db_path)
        self.report_generator = ReportGenerator(self.db)
    
    def run(self):
        """Main entry point for the CLI."""
        parser = self.create_parser()
        args = parser.parse_args()
        
        if hasattr(args, 'func'):
            try:
                args.func(args)
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)
        else:
            parser.print_help()
    
    def create_parser(self):
        """Create the argument parser with all subcommands."""
        parser = argparse.ArgumentParser(
            description="Budget Manager - Personal Finance Tracking Tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  budget add-category Food "Restaurant and grocery expenses"
  budget add-transaction -a 50.00 -d "Grocery shopping" -c Food expense
  budget set-budget Food 500.00 monthly
  budget list-transactions --last-month
  budget report monthly
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Category commands
        self._add_category_commands(subparsers)
        
        # Transaction commands
        self._add_transaction_commands(subparsers)
        
        # Budget commands
        self._add_budget_commands(subparsers)
        
        # Report commands
        self._add_report_commands(subparsers)
        
        return parser
    
    def _add_category_commands(self, subparsers):
        """Add category-related commands."""
        # Add category
        add_cat = subparsers.add_parser('add-category', help='Add a new category')
        add_cat.add_argument('name', help='Category name')
        add_cat.add_argument('description', nargs='?', help='Category description')
        add_cat.add_argument('--color', help='Category color (hex code)')
        add_cat.set_defaults(func=self.add_category)
        
        # List categories
        list_cat = subparsers.add_parser('list-categories', help='List all categories')
        list_cat.set_defaults(func=self.list_categories)
        
        # Update category
        update_cat = subparsers.add_parser('update-category', help='Update a category')
        update_cat.add_argument('name', help='Current category name')
        update_cat.add_argument('--new-name', help='New category name')
        update_cat.add_argument('--description', help='New description')
        update_cat.add_argument('--color', help='New color (hex code)')
        update_cat.set_defaults(func=self.update_category)
        
        # Delete category
        del_cat = subparsers.add_parser('delete-category', help='Delete a category')
        del_cat.add_argument('name', help='Category name to delete')
        del_cat.add_argument('--force', action='store_true', help='Force deletion without confirmation')
        del_cat.set_defaults(func=self.delete_category)
    
    def _add_transaction_commands(self, subparsers):
        """Add transaction-related commands."""
        # Add transaction
        add_trans = subparsers.add_parser('add-transaction', help='Add a new transaction')
        add_trans.add_argument('-a', '--amount', required=True, type=str, help='Transaction amount')
        add_trans.add_argument('-d', '--description', required=True, help='Transaction description')
        add_trans.add_argument('-c', '--category', help='Category name')
        add_trans.add_argument('type', choices=['income', 'expense'], help='Transaction type')
        add_trans.add_argument('--date', help='Transaction date (YYYY-MM-DD)')
        add_trans.add_argument('--notes', help='Additional notes')
        add_trans.set_defaults(func=self.add_transaction)
        
        # List transactions
        list_trans = subparsers.add_parser('list-transactions', help='List transactions')
        list_trans.add_argument('--category', help='Filter by category name')
        list_trans.add_argument('--type', choices=['income', 'expense'], help='Filter by type')
        list_trans.add_argument('--limit', type=int, default=20, help='Limit number of results')
        list_trans.add_argument('--last-week', action='store_true', help='Show last week only')
        list_trans.add_argument('--last-month', action='store_true', help='Show last month only')
        list_trans.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
        list_trans.add_argument('--end-date', help='End date (YYYY-MM-DD)')
        list_trans.set_defaults(func=self.list_transactions)
        
        # Update transaction
        update_trans = subparsers.add_parser('update-transaction', help='Update a transaction')
        update_trans.add_argument('transaction_id', help='Transaction ID')
        update_trans.add_argument('--amount', type=str, help='New amount')
        update_trans.add_argument('--description', help='New description')
        update_trans.add_argument('--category', help='New category name')
        update_trans.add_argument('--type', choices=['income', 'expense'], help='New type')
        update_trans.add_argument('--date', help='New date (YYYY-MM-DD)')
        update_trans.add_argument('--notes', help='New notes')
        update_trans.set_defaults(func=self.update_transaction)
        
        # Delete transaction
        del_trans = subparsers.add_parser('delete-transaction', help='Delete a transaction')
        del_trans.add_argument('transaction_id', help='Transaction ID to delete')
        del_trans.add_argument('--force', action='store_true', help='Force deletion without confirmation')
        del_trans.set_defaults(func=self.delete_transaction)
    
    def _add_budget_commands(self, subparsers):
        """Add budget-related commands."""
        # Set budget
        set_budget = subparsers.add_parser('set-budget', help='Set a budget for a category')
        set_budget.add_argument('category', help='Category name')
        set_budget.add_argument('amount', type=str, help='Budget amount')
        set_budget.add_argument('period', choices=['weekly', 'monthly', 'yearly'], 
                               default='monthly', nargs='?', help='Budget period')
        set_budget.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
        set_budget.set_defaults(func=self.set_budget)
        
        # List budgets
        list_budgets = subparsers.add_parser('list-budgets', help='List all budgets')
        list_budgets.add_argument('--category', help='Filter by category name')
        list_budgets.add_argument('--include-inactive', action='store_true', help='Include inactive budgets')
        list_budgets.set_defaults(func=self.list_budgets)
        
        # Budget status
        budget_status = subparsers.add_parser('budget-status', help='Show budget status')
        budget_status.add_argument('--category', help='Specific category')
        budget_status.set_defaults(func=self.budget_status)
        
        # Delete budget
        del_budget = subparsers.add_parser('delete-budget', help='Delete a budget')
        del_budget.add_argument('budget_id', help='Budget ID to delete')
        del_budget.add_argument('--force', action='store_true', help='Force deletion without confirmation')
        del_budget.set_defaults(func=self.delete_budget)
    
    def _add_report_commands(self, subparsers):
        """Add report-related commands."""
        # Generate report
        report = subparsers.add_parser('report', help='Generate financial reports')
        report.add_argument('type', choices=['monthly', 'yearly', 'custom', 'summary'], 
                           help='Report type')
        report.add_argument('--start-date', help='Start date for custom report (YYYY-MM-DD)')
        report.add_argument('--end-date', help='End date for custom report (YYYY-MM-DD)')
        report.add_argument('--category', help='Filter by category')
        report.add_argument('--export', choices=['csv', 'json'], help='Export format')
        report.add_argument('--output', help='Output file path')
        report.set_defaults(func=self.generate_report)
    
    # Category command implementations
    def add_category(self, args):
        """Add a new category."""
        try:
            category = Category(
                name=args.name,
                description=args.description,
                color=args.color
            )
            category_id = self.db.create_category(category)
            print(f"✓ Category '{args.name}' created successfully (ID: {category_id})")
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_categories(self, args):
        """List all categories."""
        categories = self.db.get_all_categories()
        if not categories:
            print("No categories found.")
            return
        
        print(f"{'Name':<20} {'Description':<40} {'Created':<20}")
        print("-" * 80)
        for cat in categories:
            desc = cat.description or ""
            if len(desc) > 37:
                desc = desc[:34] + "..."
            print(f"{cat.name:<20} {desc:<40} {cat.created_at.strftime('%Y-%m-%d %H:%M'):<20}")
    
    def update_category(self, args):
        """Update an existing category."""
        categories = [c for c in self.db.get_all_categories() if c.name == args.name]
        if not categories:
            print(f"Category '{args.name}' not found.")
            return
        
        category = categories[0]
        if args.new_name:
            category.name = args.new_name
        if args.description is not None:
            category.description = args.description
        if args.color:
            category.color = args.color
        
        if self.db.update_category(category):
            print(f"✓ Category updated successfully.")
        else:
            print("Failed to update category.")
    
    def delete_category(self, args):
        """Delete a category."""
        categories = [c for c in self.db.get_all_categories() if c.name == args.name]
        if not categories:
            print(f"Category '{args.name}' not found.")
            return
        
        category = categories[0]
        
        if not args.force:
            confirm = input(f"Are you sure you want to delete '{args.name}'? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
        
        if self.db.delete_category(category.id):
            print(f"✓ Category '{args.name}' deleted successfully.")
        else:
            print("Failed to delete category.")
    
    # Transaction command implementations
    def add_transaction(self, args):
        """Add a new transaction."""
        try:
            amount = Decimal(args.amount)
        except InvalidOperation:
            print(f"Error: Invalid amount '{args.amount}'")
            return
        
        category_id = None
        if args.category:
            categories = [c for c in self.db.get_all_categories() if c.name == args.category]
            if not categories:
                print(f"Category '{args.category}' not found.")
                return
            category_id = categories[0].id
        
        transaction_date = datetime.now()
        if args.date:
            try:
                transaction_date = datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.")
                return
        
        try:
            transaction = Transaction(
                amount=amount,
                description=args.description,
                category_id=category_id,
                transaction_type=TransactionType(args.type),
                date=transaction_date,
                notes=args.notes
            )
            transaction_id = self.db.create_transaction(transaction)
            print(f"✓ Transaction added successfully (ID: {transaction_id[:8]}...)")
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_transactions(self, args):
        """List transactions with filters."""
        category_id = None
        if args.category:
            categories = [c for c in self.db.get_all_categories() if c.name == args.category]
            if not categories:
                print(f"Category '{args.category}' not found.")
                return
            category_id = categories[0].id
        
        transaction_type = None
        if args.type:
            transaction_type = TransactionType(args.type)
        
        start_date = None
        end_date = None
        
        if args.last_week:
            start_date = datetime.now() - timedelta(days=7)
        elif args.last_month:
            start_date = datetime.now() - timedelta(days=30)
        else:
            if args.start_date:
                try:
                    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
                except ValueError:
                    print(f"Error: Invalid start date format '{args.start_date}'. Use YYYY-MM-DD.")
                    return
            if args.end_date:
                try:
                    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
                except ValueError:
                    print(f"Error: Invalid end date format '{args.end_date}'. Use YYYY-MM-DD.")
                    return
        
        transactions = self.db.get_transactions(
            category_id=category_id,
            transaction_type=transaction_type,
            start_date=start_date,
            end_date=end_date,
            limit=args.limit
        )
        
        if not transactions:
            print("No transactions found.")
            return
        
        # Get category names for display
        categories = {c.id: c.name for c in self.db.get_all_categories()}
        
        print(f"{'Date':<12} {'Type':<8} {'Amount':<12} {'Category':<15} {'Description':<30} {'ID':<10}")
        print("-" * 95)
        
        for trans in transactions:
            category_name = categories.get(trans.category_id, "N/A") if trans.category_id else "N/A"
            if len(category_name) > 12:
                category_name = category_name[:9] + "..."
            
            description = trans.description
            if len(description) > 27:
                description = description[:24] + "..."
            
            amount_str = f"${trans.amount:.2f}"
            trans_id = trans.id[:8] + "..."
            
            print(f"{trans.date.strftime('%Y-%m-%d'):<12} "
                  f"{trans.transaction_type.value:<8} "
                  f"{amount_str:<12} "
                  f"{category_name:<15} "
                  f"{description:<30} "
                  f"{trans_id:<10}")
    
    def update_transaction(self, args):
        """Update an existing transaction."""
        transaction = self.db.get_transaction(args.transaction_id)
        if not transaction:
            print(f"Transaction with ID '{args.transaction_id}' not found.")
            return
        
        if args.amount:
            try:
                transaction.amount = Decimal(args.amount)
            except InvalidOperation:
                print(f"Error: Invalid amount '{args.amount}'")
                return
        
        if args.description:
            transaction.description = args.description
        
        if args.category:
            categories = [c for c in self.db.get_all_categories() if c.name == args.category]
            if not categories:
                print(f"Category '{args.category}' not found.")
                return
            transaction.category_id = categories[0].id
        
        if args.type:
            transaction.transaction_type = TransactionType(args.type)
        
        if args.date:
            try:
                transaction.date = datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.")
                return
        
        if args.notes is not None:
            transaction.notes = args.notes
        
        if self.db.update_transaction(transaction):
            print("✓ Transaction updated successfully.")
        else:
            print("Failed to update transaction.")
    
    def delete_transaction(self, args):
        """Delete a transaction."""
        transaction = self.db.get_transaction(args.transaction_id)
        if not transaction:
            print(f"Transaction with ID '{args.transaction_id}' not found.")
            return
        
        if not args.force:
            print(f"Transaction: {transaction.description} - ${transaction.amount}")
            confirm = input("Are you sure you want to delete this transaction? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
        
        if self.db.delete_transaction(args.transaction_id):
            print("✓ Transaction deleted successfully.")
        else:
            print("Failed to delete transaction.")
    
    # Budget command implementations
    def set_budget(self, args):
        """Set a budget for a category."""
        categories = [c for c in self.db.get_all_categories() if c.name == args.category]
        if not categories:
            print(f"Category '{args.category}' not found.")
            return
        
        try:
            amount = Decimal(args.amount)
        except InvalidOperation:
            print(f"Error: Invalid amount '{args.amount}'")
            return
        
        start_date = datetime.now()
        if args.start_date:
            try:
                start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.start_date}'. Use YYYY-MM-DD.")
                return
        
        try:
            budget = Budget(
                category_id=categories[0].id,
                amount=amount,
                period=args.period,
                start_date=start_date
            )
            budget_id = self.db.create_budget(budget)
            print(f"✓ Budget set for '{args.category}': ${amount} ({args.period})")
            print(f"Budget ID: {budget_id}")
        except ValueError as e:
            print(f"Error: {e}")
    
    def list_budgets(self, args):
        """List all budgets."""
        category_id = None
        if args.category:
            categories = [c for c in self.db.get_all_categories() if c.name == args.category]
            if not categories:
                print(f"Category '{args.category}' not found.")
                return
            category_id = categories[0].id
        
        budgets = self.db.get_budgets(
            category_id=category_id,
            is_active=None if args.include_inactive else True
        )
        
        if not budgets:
            print("No budgets found.")
            return
        
        # Get category names
        categories = {c.id: c.name for c in self.db.get_all_categories()}
        
        print(f"{'Category':<15} {'Amount':<12} {'Period':<10} {'Start Date':<12} {'Status':<8} {'ID':<10}")
        print("-" * 75)
        
        for budget in budgets:
            category_name = categories.get(budget.category_id, "Unknown")
            if len(category_name) > 12:
                category_name = category_name[:9] + "..."
            
            status = "Active" if budget.is_active else "Inactive"
            budget_id = budget.id[:8] + "..."
            
            print(f"{category_name:<15} "
                  f"${budget.amount:<11.2f} "
                  f"{budget.period:<10} "
                  f"{budget.start_date.strftime('%Y-%m-%d'):<12} "
                  f"{status:<8} "
                  f"{budget_id:<10}")
    
    def budget_status(self, args):
        """Show budget status with spending analysis."""
        category_id = None
        if args.category:
            categories = [c for c in self.db.get_all_categories() if c.name == args.category]
            if not categories:
                print(f"Category '{args.category}' not found.")
                return
            category_id = categories[0].id
        
        budgets = self.db.get_budgets(category_id=category_id, is_active=True)
        if not budgets:
            print("No active budgets found.")
            return
        
        # Get category names
        categories = {c.id: c.name for c in self.db.get_all_categories()}
        
        print(f"{'Category':<15} {'Budget':<12} {'Spent':<12} {'Remaining':<12} {'%Used':<8} {'Status':<12}")
        print("-" * 85)
        
        for budget in budgets:
            summary = self.db.get_budget_summary(budget)
            category_name = categories.get(budget.category_id, "Unknown")
            if len(category_name) > 12:
                category_name = category_name[:9] + "..."
            
            status = "Over Budget!" if summary.is_over_budget else "On Track"
            if summary.percentage_used > 80 and not summary.is_over_budget:
                status = "Warning"
            
            print(f"{category_name:<15} "
                  f"${budget.amount:<11.2f} "
                  f"${summary.spent_amount:<11.2f} "
                  f"${summary.remaining_amount:<11.2f} "
                  f"{summary.percentage_used:<7.1f}% "
                  f"{status:<12}")
    
    def delete_budget(self, args):
        """Delete a budget."""
        budget = self.db.get_budget(args.budget_id)
        if not budget:
            print(f"Budget with ID '{args.budget_id}' not found.")
            return
        
        if not args.force:
            categories = {c.id: c.name for c in self.db.get_all_categories()}
            category_name = categories.get(budget.category_id, "Unknown")
            print(f"Budget: {category_name} - ${budget.amount} ({budget.period})")
            confirm = input("Are you sure you want to delete this budget? (y/N): ")
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                return
        
        if self.db.delete_budget(args.budget_id):
            print("✓ Budget deleted successfully.")
        else:
            print("Failed to delete budget.")
    
    def generate_report(self, args):
        """Generate financial reports."""
        try:
            if args.type == 'monthly':
                self.report_generator.monthly_report()
            elif args.type == 'yearly':
                self.report_generator.yearly_report()
            elif args.type == 'summary':
                self.report_generator.summary_report()
            elif args.type == 'custom':
                start_date = None
                end_date = None
                
                if args.start_date:
                    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
                if args.end_date:
                    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
                
                self.report_generator.custom_report(start_date, end_date, args.category)
        except Exception as e:
            print(f"Error generating report: {e}")


def main():
    """Main entry point for the CLI application."""
    cli = BudgetManagerCLI()
    cli.run()


if __name__ == '__main__':
    main()