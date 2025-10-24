"""
Report generation module for the budget manager application.

This module provides various financial reports and analytics including:
- Monthly/yearly summaries
- Budget performance analysis
- Spending trends by category
- Income vs expense analysis
"""

import json
import csv
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List, Optional, Any
from calendar import monthrange

from .database import DatabaseManager
from .models import TransactionType


class ReportGenerator:
    """Generates various financial reports and analytics."""
    
    def __init__(self, db: DatabaseManager):
        """Initialize with database manager."""
        self.db = db
    
    def monthly_report(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Generate a comprehensive monthly report."""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        # Calculate date range for the month
        start_date = datetime(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = datetime(year, month, last_day, 23, 59, 59)
        
        print(f"\n📊 Monthly Report for {start_date.strftime('%B %Y')}")
        print("=" * 60)
        
        # Income vs Expenses
        income_expense = self.db.get_income_vs_expenses(start_date, end_date)
        print(f"\n💰 Financial Summary:")
        print(f"  Income:     ${income_expense['income']:>10.2f}")
        print(f"  Expenses:   ${income_expense['expense']:>10.2f}")
        print(f"  Net:        ${income_expense['net']:>10.2f}")
        
        if income_expense['net'] >= 0:
            print("  Status:     ✅ Positive cash flow")
        else:
            print("  Status:     ⚠️  Negative cash flow")
        
        # Spending by category
        spending_by_category = self.db.get_spending_by_category(start_date, end_date)
        if spending_by_category:
            print(f"\n📈 Spending by Category:")
            total_spending = sum(spending_by_category.values())
            for category, amount in sorted(spending_by_category.items(), 
                                         key=lambda x: x[1], reverse=True):
                if amount > 0:
                    percentage = (amount / total_spending * 100) if total_spending > 0 else 0
                    print(f"  {category:<20} ${amount:>8.2f} ({percentage:>5.1f}%)")
        
        # Budget performance
        self._show_budget_performance(start_date, end_date)
        
        # Transaction count
        transactions = self.db.get_transactions(start_date=start_date, end_date=end_date)
        income_count = len([t for t in transactions if t.transaction_type == TransactionType.INCOME])
        expense_count = len([t for t in transactions if t.transaction_type == TransactionType.EXPENSE])
        
        print(f"\n📝 Transaction Summary:")
        print(f"  Total transactions: {len(transactions)}")
        print(f"  Income entries:     {income_count}")
        print(f"  Expense entries:    {expense_count}")
        
        # Daily average
        days_in_month = (end_date - start_date).days + 1
        if income_expense['expense'] > 0:
            daily_avg = income_expense['expense'] / days_in_month
            print(f"  Daily avg spending: ${daily_avg:.2f}")
        
        return {
            'period': f"{start_date.strftime('%B %Y')}",
            'income_expense': income_expense,
            'spending_by_category': spending_by_category,
            'transaction_count': len(transactions),
            'daily_average': daily_avg if income_expense['expense'] > 0 else 0
        }
    
    def yearly_report(self, year: int = None) -> Dict[str, Any]:
        """Generate a comprehensive yearly report."""
        if year is None:
            year = datetime.now().year
        
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)
        
        print(f"\n📊 Yearly Report for {year}")
        print("=" * 60)
        
        # Overall financial summary
        income_expense = self.db.get_income_vs_expenses(start_date, end_date)
        print(f"\n💰 Annual Financial Summary:")
        print(f"  Total Income:   ${income_expense['income']:>12.2f}")
        print(f"  Total Expenses: ${income_expense['expense']:>12.2f}")
        print(f"  Net Income:     ${income_expense['net']:>12.2f}")
        
        if income_expense['net'] >= 0:
            print("  Status:         ✅ Profitable year")
        else:
            print("  Status:         ⚠️  Loss for the year")
        
        # Monthly breakdown
        print(f"\n📅 Monthly Breakdown:")
        print(f"{'Month':<12} {'Income':<12} {'Expenses':<12} {'Net':<12}")
        print("-" * 50)
        
        monthly_data = []
        for month in range(1, 13):
            month_start = datetime(year, month, 1)
            _, last_day = monthrange(year, month)
            month_end = datetime(year, month, last_day, 23, 59, 59)
            
            month_summary = self.db.get_income_vs_expenses(month_start, month_end)
            month_name = month_start.strftime('%b')
            
            print(f"{month_name:<12} "
                  f"${month_summary['income']:<11.2f} "
                  f"${month_summary['expense']:<11.2f} "
                  f"${month_summary['net']:<11.2f}")
            
            monthly_data.append({
                'month': month_name,
                'income': float(month_summary['income']),
                'expenses': float(month_summary['expense']),
                'net': float(month_summary['net'])
            })
        
        # Category analysis
        spending_by_category = self.db.get_spending_by_category(start_date, end_date)
        if spending_by_category:
            print(f"\n📈 Top Spending Categories:")
            total_spending = sum(spending_by_category.values())
            top_categories = sorted(spending_by_category.items(), 
                                  key=lambda x: x[1], reverse=True)[:10]
            
            for category, amount in top_categories:
                if amount > 0:
                    percentage = (amount / total_spending * 100) if total_spending > 0 else 0
                    print(f"  {category:<25} ${amount:>10.2f} ({percentage:>5.1f}%)")
        
        # Calculate averages
        monthly_avg_income = income_expense['income'] / 12
        monthly_avg_expense = income_expense['expense'] / 12
        
        print(f"\n📊 Averages:")
        print(f"  Monthly avg income:  ${monthly_avg_income:>10.2f}")
        print(f"  Monthly avg expense: ${monthly_avg_expense:>10.2f}")
        
        return {
            'year': year,
            'income_expense': income_expense,
            'monthly_data': monthly_data,
            'spending_by_category': spending_by_category,
            'monthly_averages': {
                'income': float(monthly_avg_income),
                'expense': float(monthly_avg_expense)
            }
        }
    
    def summary_report(self) -> Dict[str, Any]:
        """Generate a quick summary report of current financial status."""
        print(f"\n📊 Financial Summary")
        print("=" * 40)
        
        # Current month
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        
        month_summary = self.db.get_income_vs_expenses(start_of_month, now)
        print(f"\n💰 This Month ({now.strftime('%B')}):")
        print(f"  Income:   ${month_summary['income']:>10.2f}")
        print(f"  Expenses: ${month_summary['expense']:>10.2f}")
        print(f"  Net:      ${month_summary['net']:>10.2f}")
        
        # Current year
        start_of_year = datetime(now.year, 1, 1)
        year_summary = self.db.get_income_vs_expenses(start_of_year, now)
        print(f"\n💰 This Year ({now.year}):")
        print(f"  Income:   ${year_summary['income']:>10.2f}")
        print(f"  Expenses: ${year_summary['expense']:>10.2f}")
        print(f"  Net:      ${year_summary['net']:>10.2f}")
        
        # Budget status
        budgets = self.db.get_budgets(is_active=True)
        if budgets:
            print(f"\n💳 Budget Status:")
            over_budget_count = 0
            for budget in budgets:
                summary = self.db.get_budget_summary(budget)
                if summary.is_over_budget:
                    over_budget_count += 1
            
            print(f"  Active budgets: {len(budgets)}")
            print(f"  Over budget:    {over_budget_count}")
            if over_budget_count > 0:
                print("  Status:         ⚠️  Some budgets exceeded")
            else:
                print("  Status:         ✅ All budgets on track")
        
        # Recent transactions
        recent_transactions = self.db.get_transactions(limit=5)
        if recent_transactions:
            print(f"\n📝 Recent Transactions:")
            categories = {c.id: c.name for c in self.db.get_all_categories()}
            for trans in recent_transactions:
                category_name = categories.get(trans.category_id, "N/A") if trans.category_id else "N/A"
                print(f"  {trans.date.strftime('%m/%d')} "
                      f"{trans.transaction_type.value[:3].upper()} "
                      f"${trans.amount:>8.2f} "
                      f"{category_name:<15} "
                      f"{trans.description[:25]}")
        
        return {
            'current_month': month_summary,
            'current_year': year_summary,
            'budget_count': len(budgets) if budgets else 0,
            'over_budget_count': over_budget_count if budgets else 0
        }
    
    def custom_report(self, start_date: datetime = None, end_date: datetime = None, 
                     category_name: str = None) -> Dict[str, Any]:
        """Generate a custom report for a specific date range and/or category."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=30)
        if end_date is None:
            end_date = datetime.now()
        
        print(f"\n📊 Custom Report")
        print(f"Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        if category_name:
            print(f"Category: {category_name}")
        print("=" * 60)
        
        category_id = None
        if category_name:
            categories = [c for c in self.db.get_all_categories() if c.name == category_name]
            if not categories:
                print(f"Category '{category_name}' not found.")
                return {}
            category_id = categories[0].id
        
        # Financial summary
        if category_id:
            # Get transactions for specific category
            transactions = self.db.get_transactions(
                category_id=category_id,
                start_date=start_date,
                end_date=end_date
            )
            
            total_income = sum(t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
            total_expense = sum(t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)
            net = total_income - total_expense
            
            print(f"\n💰 Financial Summary for {category_name}:")
            print(f"  Income:   ${total_income:>10.2f}")
            print(f"  Expenses: ${total_expense:>10.2f}")
            print(f"  Net:      ${net:>10.2f}")
            
        else:
            # Overall summary
            income_expense = self.db.get_income_vs_expenses(start_date, end_date)
            print(f"\n💰 Overall Financial Summary:")
            print(f"  Income:   ${income_expense['income']:>10.2f}")
            print(f"  Expenses: ${income_expense['expense']:>10.2f}")
            print(f"  Net:      ${income_expense['net']:>10.2f}")
            
            # Category breakdown
            spending_by_category = self.db.get_spending_by_category(start_date, end_date)
            if spending_by_category:
                print(f"\n📈 Spending by Category:")
                total_spending = sum(spending_by_category.values())
                for category, amount in sorted(spending_by_category.items(), 
                                             key=lambda x: x[1], reverse=True):
                    if amount > 0:
                        percentage = (amount / total_spending * 100) if total_spending > 0 else 0
                        print(f"  {category:<20} ${amount:>8.2f} ({percentage:>5.1f}%)")
        
        # Transaction details
        all_transactions = self.db.get_transactions(
            category_id=category_id,
            start_date=start_date,
            end_date=end_date
        )
        
        print(f"\n📝 Transaction Summary:")
        print(f"  Total transactions: {len(all_transactions)}")
        
        income_transactions = [t for t in all_transactions if t.transaction_type == TransactionType.INCOME]
        expense_transactions = [t for t in all_transactions if t.transaction_type == TransactionType.EXPENSE]
        
        print(f"  Income entries:     {len(income_transactions)}")
        print(f"  Expense entries:    {len(expense_transactions)}")
        
        # Daily/weekly averages
        days = (end_date - start_date).days + 1
        if days > 0 and expense_transactions:
            total_expenses = sum(t.amount for t in expense_transactions)
            daily_avg = total_expenses / days
            weekly_avg = daily_avg * 7
            print(f"  Daily avg spending: ${daily_avg:.2f}")
            print(f"  Weekly avg spending: ${weekly_avg:.2f}")
        
        return {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'category': category_name,
            'transaction_count': len(all_transactions),
            'summary': income_expense if not category_id else {
                'income': float(total_income),
                'expense': float(total_expense),
                'net': float(net)
            }
        }
    
    def _show_budget_performance(self, start_date: datetime, end_date: datetime):
        """Show budget performance for the given period."""
        budgets = self.db.get_budgets(is_active=True)
        if not budgets:
            return
        
        print(f"\n💳 Budget Performance:")
        
        # Filter budgets that are active during the period
        relevant_budgets = []
        for budget in budgets:
            if (budget.start_date <= end_date and 
                (budget.end_date is None or budget.end_date >= start_date)):
                relevant_budgets.append(budget)
        
        if not relevant_budgets:
            print("  No active budgets for this period.")
            return
        
        categories = {c.id: c.name for c in self.db.get_all_categories()}
        
        print(f"  {'Category':<15} {'Budget':<10} {'Spent':<10} {'Remaining':<12} {'Status':<12}")
        print("  " + "-" * 65)
        
        for budget in relevant_budgets:
            summary = self.db.get_budget_summary(budget)
            category_name = categories.get(budget.category_id, "Unknown")
            if len(category_name) > 12:
                category_name = category_name[:9] + "..."
            
            if summary.is_over_budget:
                status = "⚠️ Over"
            elif summary.percentage_used > 80:
                status = "⚡ Warning"
            else:
                status = "✅ Good"
            
            print(f"  {category_name:<15} "
                  f"${budget.amount:<9.2f} "
                  f"${summary.spent_amount:<9.2f} "
                  f"${summary.remaining_amount:<11.2f} "
                  f"{status:<12}")
    
    def export_to_csv(self, data: Dict[str, Any], filename: str):
        """Export report data to CSV format."""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if 'monthly_data' in data:
                    # Yearly report format
                    writer = csv.DictWriter(csvfile, fieldnames=['month', 'income', 'expenses', 'net'])
                    writer.writeheader()
                    writer.writerows(data['monthly_data'])
                else:
                    # Simple format for other reports
                    writer = csv.writer(csvfile)
                    writer.writerow(['Report Type', 'Generated On', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    
                    for key, value in data.items():
                        if isinstance(value, dict):
                            writer.writerow([key, ''])
                            for subkey, subvalue in value.items():
                                writer.writerow(['  ' + subkey, subvalue])
                        else:
                            writer.writerow([key, value])
            
            print(f"✓ Report exported to {filename}")
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
    
    def export_to_json(self, data: Dict[str, Any], filename: str):
        """Export report data to JSON format."""
        try:
            # Convert Decimal objects to float for JSON serialization
            def decimal_to_float(obj):
                if isinstance(obj, Decimal):
                    return float(obj)
                elif isinstance(obj, dict):
                    return {k: decimal_to_float(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [decimal_to_float(item) for item in obj]
                return obj
            
            json_data = decimal_to_float(data)
            json_data['generated_on'] = datetime.now().isoformat()
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(json_data, jsonfile, indent=2, ensure_ascii=False)
            
            print(f"✓ Report exported to {filename}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")