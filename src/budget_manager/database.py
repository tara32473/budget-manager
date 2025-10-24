"""
Database operations for the budget manager application.

This module handles all database interactions using SQLite for data persistence.
Provides methods for CRUD operations on transactions, categories, and budgets.
"""

import sqlite3
import os
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import Transaction, Category, Budget, TransactionType, BudgetSummary


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager with optional custom path."""
        if db_path is None:
            # Default to data directory in project root
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(project_root, "data", "budget_manager.db")
        
        self.db_path = db_path
        self._ensure_db_directory()
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        try:
            yield conn
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    color TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    amount DECIMAL(10,2) NOT NULL,
                    description TEXT NOT NULL,
                    category_id TEXT,
                    transaction_type TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')
            
            # Budgets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id TEXT PRIMARY KEY,
                    category_id TEXT NOT NULL,
                    amount DECIMAL(10,2) NOT NULL,
                    period TEXT NOT NULL DEFAULT 'monthly',
                    start_date TIMESTAMP NOT NULL,
                    end_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                )
            ''')
            
            # Create indices for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(transaction_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_budgets_category ON budgets(category_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_budgets_dates ON budgets(start_date, end_date)')
            
            conn.commit()
    
    # Category operations
    def create_category(self, category: Category) -> str:
        """Create a new category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO categories (id, name, description, color, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (category.id, category.name, category.description, 
                  category.color, category.created_at))
            conn.commit()
            return category.id
    
    def get_category(self, category_id: str) -> Optional[Category]:
        """Get a category by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
            row = cursor.fetchone()
            if row:
                return Category(
                    id=row['id'],
                    name=row['name'],
                    description=row['description'],
                    color=row['color'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categories ORDER BY name')
            rows = cursor.fetchall()
            return [Category(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                color=row['color'],
                created_at=datetime.fromisoformat(row['created_at'])
            ) for row in rows]
    
    def update_category(self, category: Category) -> bool:
        """Update an existing category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE categories 
                SET name = ?, description = ?, color = ?
                WHERE id = ?
            ''', (category.name, category.description, category.color, category.id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_category(self, category_id: str) -> bool:
        """Delete a category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    # Transaction operations
    def create_transaction(self, transaction: Transaction) -> str:
        """Create a new transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (id, amount, description, category_id, 
                                        transaction_type, date, created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (transaction.id, float(transaction.amount), transaction.description,
                  transaction.category_id, transaction.transaction_type.value,
                  transaction.date, transaction.created_at, transaction.notes))
            conn.commit()
            return transaction.id
    
    def get_transaction(self, transaction_id: str) -> Optional[Transaction]:
        """Get a transaction by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM transactions WHERE id = ?', (transaction_id,))
            row = cursor.fetchone()
            if row:
                return Transaction(
                    id=row['id'],
                    amount=Decimal(str(row['amount'])),
                    description=row['description'],
                    category_id=row['category_id'],
                    transaction_type=TransactionType(row['transaction_type']),
                    date=datetime.fromisoformat(row['date']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    notes=row['notes']
                )
            return None
    
    def get_transactions(self, category_id: str = None, transaction_type: TransactionType = None,
                        start_date: datetime = None, end_date: datetime = None,
                        limit: int = None) -> List[Transaction]:
        """Get transactions with optional filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM transactions WHERE 1=1'
            params = []
            
            if category_id:
                query += ' AND category_id = ?'
                params.append(category_id)
            
            if transaction_type:
                query += ' AND transaction_type = ?'
                params.append(transaction_type.value)
            
            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)
            
            query += ' ORDER BY date DESC'
            
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [Transaction(
                id=row['id'],
                amount=Decimal(str(row['amount'])),
                description=row['description'],
                category_id=row['category_id'],
                transaction_type=TransactionType(row['transaction_type']),
                date=datetime.fromisoformat(row['date']),
                created_at=datetime.fromisoformat(row['created_at']),
                notes=row['notes']
            ) for row in rows]
    
    def update_transaction(self, transaction: Transaction) -> bool:
        """Update an existing transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE transactions 
                SET amount = ?, description = ?, category_id = ?, 
                    transaction_type = ?, date = ?, notes = ?
                WHERE id = ?
            ''', (float(transaction.amount), transaction.description,
                  transaction.category_id, transaction.transaction_type.value,
                  transaction.date, transaction.notes, transaction.id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete a transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    # Budget operations
    def create_budget(self, budget: Budget) -> str:
        """Create a new budget."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO budgets (id, category_id, amount, period, 
                                   start_date, end_date, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (budget.id, budget.category_id, float(budget.amount),
                  budget.period, budget.start_date, budget.end_date,
                  budget.created_at, budget.is_active))
            conn.commit()
            return budget.id
    
    def get_budget(self, budget_id: str) -> Optional[Budget]:
        """Get a budget by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM budgets WHERE id = ?', (budget_id,))
            row = cursor.fetchone()
            if row:
                return Budget(
                    id=row['id'],
                    category_id=row['category_id'],
                    amount=Decimal(str(row['amount'])),
                    period=row['period'],
                    start_date=datetime.fromisoformat(row['start_date']),
                    end_date=datetime.fromisoformat(row['end_date']) if row['end_date'] else None,
                    created_at=datetime.fromisoformat(row['created_at']),
                    is_active=bool(row['is_active'])
                )
            return None
    
    def get_budgets(self, category_id: str = None, is_active: bool = True) -> List[Budget]:
        """Get budgets with optional filters."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = 'SELECT * FROM budgets WHERE 1=1'
            params = []
            
            if category_id:
                query += ' AND category_id = ?'
                params.append(category_id)
            
            if is_active is not None:
                query += ' AND is_active = ?'
                params.append(is_active)
            
            query += ' ORDER BY created_at DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [Budget(
                id=row['id'],
                category_id=row['category_id'],
                amount=Decimal(str(row['amount'])),
                period=row['period'],
                start_date=datetime.fromisoformat(row['start_date']),
                end_date=datetime.fromisoformat(row['end_date']) if row['end_date'] else None,
                created_at=datetime.fromisoformat(row['created_at']),
                is_active=bool(row['is_active'])
            ) for row in rows]
    
    def update_budget(self, budget: Budget) -> bool:
        """Update an existing budget."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE budgets 
                SET category_id = ?, amount = ?, period = ?, 
                    start_date = ?, end_date = ?, is_active = ?
                WHERE id = ?
            ''', (budget.category_id, float(budget.amount), budget.period,
                  budget.start_date, budget.end_date, budget.is_active, budget.id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_budget(self, budget_id: str) -> bool:
        """Delete a budget."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    # Analytics and reporting methods
    def get_budget_summary(self, budget: Budget) -> BudgetSummary:
        """Get a summary of budget performance."""
        # Get transactions for the budget period
        transactions = self.get_transactions(
            category_id=budget.category_id,
            transaction_type=TransactionType.EXPENSE,
            start_date=budget.start_date,
            end_date=budget.end_date
        )
        
        spent_amount = sum(t.amount for t in transactions)
        
        return BudgetSummary(
            budget=budget,
            spent_amount=spent_amount,
            transaction_count=len(transactions)
        )
    
    def get_spending_by_category(self, start_date: datetime = None, 
                               end_date: datetime = None) -> Dict[str, Decimal]:
        """Get spending totals by category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT c.name, COALESCE(SUM(t.amount), 0) as total
                FROM categories c
                LEFT JOIN transactions t ON c.id = t.category_id 
                    AND t.transaction_type = 'expense'
            '''
            params = []
            
            if start_date or end_date:
                if start_date:
                    query += ' AND t.date >= ?'
                    params.append(start_date)
                if end_date:
                    query += ' AND t.date <= ?'
                    params.append(end_date)
            
            query += ' GROUP BY c.id, c.name ORDER BY total DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return {row['name']: Decimal(str(row['total'])) for row in rows}
    
    def get_income_vs_expenses(self, start_date: datetime = None, 
                             end_date: datetime = None) -> Dict[str, Decimal]:
        """Get total income vs expenses."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT transaction_type, COALESCE(SUM(amount), 0) as total
                FROM transactions
                WHERE 1=1
            '''
            params = []
            
            if start_date:
                query += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                query += ' AND date <= ?'
                params.append(end_date)
            
            query += ' GROUP BY transaction_type'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            result = {'income': Decimal('0'), 'expense': Decimal('0')}
            for row in rows:
                result[row['transaction_type']] = Decimal(str(row['total']))
            
            result['net'] = result['income'] - result['expense']
            return result