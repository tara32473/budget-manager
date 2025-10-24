# Usage Guide

Comprehensive guide to using Budget Manager for personal finance management.

## 🎯 Quick Start

Get up and running with Budget Manager in 5 minutes:

```bash
# 1. Set up basic categories
budget add-category "Food" "Groceries and dining"
budget add-category "Transport" "Gas and public transit"
budget add-category "Housing" "Rent and utilities"

# 2. Set monthly budgets
budget set-budget "Food" 500.00
budget set-budget "Transport" 300.00
budget set-budget "Housing" 2000.00

# 3. Add some transactions
budget add-transaction income 3000.00 "Salary" "Monthly paycheck"
budget add-transaction expense 400.00 "Food" "Weekly groceries"
budget add-transaction expense 50.00 "Transport" "Gas fill-up"

# 4. Check your status
budget report monthly
budget budget-status
```

## 📊 Core Workflows

### Daily Financial Tracking

**Morning Routine:**
```bash
# Check yesterday's transactions
budget list-transactions --limit 10

# Review budget status
budget budget-status --warnings-only
```

**Adding Expenses:**
```bash
# Restaurant meal
budget add-transaction expense 35.50 "Food" "Lunch at Subway"

# Transportation
budget add-transaction expense 2.75 "Transport" "Bus fare to work"

# Quick entry for recurring expenses
budget add-transaction expense 85.00 "Utilities" "Electric bill"
```

**Recording Income:**
```bash
# Salary
budget add-transaction income 2500.00 "Salary" "Bi-weekly paycheck"

# Side income
budget add-transaction income 150.00 "Freelance" "Web design project"

# Other income
budget add-transaction income 25.00 "Investment" "Dividend payment"
```

### Weekly Review Process

```bash
# 1. Review the week's spending
budget list-transactions --limit 50

# 2. Check budget status
budget budget-status

# 3. Generate weekly summary (custom date range)
budget report custom --start-date $(date -d '7 days ago' +%Y-%m-%d) --end-date $(date +%Y-%m-%d)

# 4. Export for spreadsheet analysis
budget export-transactions weekly_$(date +%Y%m%d).csv --start-date $(date -d '7 days ago' +%Y-%m-%d)
```

### Monthly Financial Housekeeping

```bash
# 1. Generate comprehensive monthly report
budget report monthly

# 2. Review all categories and budgets
budget list-categories
budget budget-status

# 3. Export monthly data
budget export-transactions monthly_$(date +%Y_%m).csv --month $(date +%Y-%m)

# 4. Plan next month's budgets
budget set-budget "Food" 550.00 --month $(date -d 'next month' +%Y-%m)
```

## 💰 Transaction Management

### Adding Transactions

**Basic Syntax:**
```bash
budget add-transaction <type> <amount> <category> <description>
```

**Examples:**
```bash
# Expenses with different categories
budget add-transaction expense 45.99 "Food" "Dinner at Italian restaurant"
budget add-transaction expense 125.00 "Clothing" "New work shirts"
budget add-transaction expense 75.50 "Healthcare" "Doctor copay"
budget add-transaction expense 15.00 "Entertainment" "Movie ticket"

# Income sources
budget add-transaction income 3200.00 "Salary" "Monthly salary - October"
budget add-transaction income 75.00 "Side Job" "Pet sitting weekend"
budget add-transaction income 120.00 "Refund" "Insurance reimbursement"
```

**Advanced Options:**
```bash
# Specify custom date (for past transactions)
budget add-transaction expense 200.00 "Utilities" "Gas bill" --date 2025-10-15

# Add with specific time
budget add-transaction expense 25.00 "Transport" "Uber ride" --datetime "2025-10-20 14:30"
```

### Viewing Transactions

**List Recent Transactions:**
```bash
# Last 20 transactions
budget list-transactions --limit 20

# All transactions this month
budget list-transactions --month $(date +%Y-%m)

# Specific category
budget list-transactions --category "Food"

# Date range
budget list-transactions --start-date 2025-10-01 --end-date 2025-10-15
```

**Formatted Output:**
```bash
# Table format (default)
budget list-transactions --format table

# CSV format
budget list-transactions --format csv

# JSON format for scripting
budget list-transactions --format json
```

### Editing Transactions

**Update Transaction Details:**
```bash
# Find transaction ID first
budget list-transactions --limit 5

# Update amount
budget update-transaction abc123def --amount 47.50

# Update description
budget update-transaction abc123def --description "Corrected restaurant bill"

# Update category
budget update-transaction abc123def --category "Entertainment"

# Multiple updates at once
budget update-transaction abc123def --amount 50.00 --description "Fixed amount and description"
```

**Delete Transactions:**
```bash
# Delete by ID
budget delete-transaction abc123def

# Confirm deletion
budget delete-transaction abc123def --confirm
```

## 🏷️ Category Management

### Creating Categories

**Simple Categories:**
```bash
budget add-category "Groceries"
budget add-category "Gas"
budget add-category "Rent"
```

**Categories with Descriptions:**
```bash
budget add-category "Healthcare" "Medical expenses, prescriptions, insurance"
budget add-category "Professional" "Work-related expenses, training, conferences"
budget add-category "Home Maintenance" "Repairs, improvements, lawn care"
budget add-category "Subscriptions" "Streaming services, magazines, software"
```

### Category Organization Strategies

**By Necessity Level:**
```bash
# Essential expenses
budget add-category "Housing-Essential" "Rent, utilities, insurance"
budget add-category "Food-Essential" "Groceries, basic dining"
budget add-category "Transport-Essential" "Gas, public transit, car maintenance"

# Discretionary spending
budget add-category "Entertainment-Discretionary" "Movies, concerts, hobbies"
budget add-category "Dining-Discretionary" "Restaurants, takeout, coffee"
budget add-category "Shopping-Discretionary" "Clothing, electronics, gifts"
```

**By Frequency:**
```bash
# Fixed monthly expenses
budget add-category "Fixed-Housing" "Rent, mortgage, insurance"
budget add-category "Fixed-Utilities" "Electric, gas, water, internet"
budget add-category "Fixed-Subscriptions" "Netflix, Spotify, gym membership"

# Variable expenses
budget add-category "Variable-Food" "Groceries, dining out"
budget add-category "Variable-Transport" "Gas, parking, maintenance"
budget add-category "Variable-Personal" "Clothing, personal care, misc"
```

### Managing Categories

**View All Categories:**
```bash
# Simple list
budget list-categories

# Detailed view with statistics
budget list-categories --detailed

# Categories with recent activity
budget list-categories --active-only
```

**Update Categories:**
```bash
# Rename category
budget update-category "Food" --new-name "Food & Dining"

# Update description
budget update-category "Transport" --description "All transportation: gas, public transit, rideshare, parking"

# Merge categories (move all transactions to new category)
budget merge-categories "Dining" "Food" --target "Food & Dining"
```

## 💳 Budget Management

### Setting Budgets

**Monthly Budgets:**
```bash
# Current month (automatic)
budget set-budget "Food" 600.00
budget set-budget "Transport" 250.00
budget set-budget "Entertainment" 150.00

# Specific month
budget set-budget "Food" 650.00 --month 2025-11
budget set-budget "Housing" 2200.00 --month 2025-11
```

**Budget Planning Strategies:**

**50/30/20 Rule Implementation:**
```bash
# Assuming $4000 monthly income
# 50% Needs ($2000)
budget set-budget "Housing" 1200.00
budget set-budget "Food" 400.00
budget set-budget "Utilities" 200.00
budget set-budget "Transport" 200.00

# 30% Wants ($1200) 
budget set-budget "Entertainment" 300.00
budget set-budget "Dining Out" 200.00
budget set-budget "Shopping" 400.00
budget set-budget "Hobbies" 300.00

# 20% Savings & Debt ($800)
budget set-budget "Emergency Fund" 400.00
budget set-budget "Investments" 400.00
```

**Zero-Based Budgeting:**
```bash
# Allocate every dollar of income
# Income: $3500/month
budget set-budget "Housing" 1400.00      # 40%
budget set-budget "Food" 350.00          # 10%
budget set-budget "Transport" 280.00     # 8%
budget set-budget "Utilities" 175.00     # 5%
budget set-budget "Insurance" 210.00     # 6%
budget set-budget "Entertainment" 175.00  # 5%
budget set-budget "Personal Care" 105.00  # 3%
budget set-budget "Emergency Fund" 350.00 # 10%
budget set-budget "Investments" 245.00    # 7%
budget set-budget "Miscellaneous" 210.00  # 6%
```

### Monitoring Budgets

**Daily Budget Checks:**
```bash
# Quick status overview
budget budget-status

# Show only categories over budget
budget budget-status --warnings-only

# Detailed breakdown
budget budget-status --detailed
```

**Budget Alerts and Notifications:**
```bash
# Check if approaching budget limits (80% spent)
budget budget-status --threshold 0.8

# Get spending velocity (daily average)
budget budget-status --velocity

# Projected month-end status
budget budget-status --projection
```

### Budget Adjustments

**Mid-Month Adjustments:**
```bash
# Increase budget if needed
budget set-budget "Food" 700.00  # Increase from 600

# Reallocate between categories
budget transfer-budget "Entertainment" "Food" 50.00

# Set temporary budget increase
budget set-budget "Healthcare" 300.00 --temporary
```

## 📈 Financial Reporting

### Standard Reports

**Monthly Reports:**
```bash
# Current month
budget report monthly

# Specific month
budget report monthly --month 2025-09

# Compare to previous month
budget report monthly --compare
```

**Yearly Reports:**
```bash
# Current year
budget report yearly

# Specific year
budget report yearly --year 2024

# Year-over-year comparison
budget report yearly --compare
```

**Custom Date Range Reports:**
```bash
# Quarter report
budget report custom --start-date 2025-07-01 --end-date 2025-09-30

# Last 30 days
budget report custom --start-date $(date -d '30 days ago' +%Y-%m-%d) --end-date $(date +%Y-%m-%d)

# Year-to-date
budget report custom --start-date 2025-01-01 --end-date $(date +%Y-%m-%d)
```

### Advanced Analytics

**Spending Trends:**
```bash
# Monthly spending by category
budget analyze trends --by-category --period monthly

# Weekly spending patterns
budget analyze trends --by-week --last-months 3

# Daily spending averages
budget analyze trends --by-day --category "Food"
```

**Budget Performance:**
```bash
# Budget adherence over time
budget analyze budget-performance --months 6

# Category budget accuracy
budget analyze budget-accuracy --detailed

# Overspending patterns
budget analyze overspending --frequency
```

### Data Export

**Export Formats:**
```bash
# CSV for Excel/Google Sheets
budget export-transactions data.csv

# JSON for programming/analysis
budget export-transactions data.json --format json

# PDF report
budget export-report monthly_report.pdf --month 2025-10
```

**Filtered Exports:**
```bash
# Specific category
budget export-transactions food_expenses.csv --category "Food"

# Date range
budget export-transactions q3_2025.csv --start-date 2025-07-01 --end-date 2025-09-30

# Expense type only
budget export-transactions expenses_only.csv --type expense

# Large amounts only
budget export-transactions large_transactions.csv --min-amount 100.00
```

## 🔧 Advanced Features

### Automation and Scripting

**Recurring Transactions:**
```bash
# Set up monthly recurring
budget add-recurring expense 2000.00 "Housing" "Monthly rent" --frequency monthly --day 1

# Weekly groceries
budget add-recurring expense 150.00 "Food" "Weekly groceries" --frequency weekly --day monday

# Bi-weekly salary
budget add-recurring income 2500.00 "Salary" "Paycheck" --frequency biweekly --day friday
```

**Batch Operations:**
```bash
# Import from CSV
budget import-transactions transactions.csv

# Bulk category updates
budget bulk-update-category "Dining" "Food & Dining" --confirm

# Batch transaction editing
budget bulk-edit --category "Food" --add-tag "groceries" --date-range "2025-10-01,2025-10-31"
```

### Data Management

**Database Maintenance:**
```bash
# Database statistics
budget stats

# Clean up old data
budget cleanup --older-than 2-years --confirm

# Optimize database
budget optimize-db

# Backup database
budget backup --output backup_$(date +%Y%m%d).db
```

**Data Integrity:**
```bash
# Verify data consistency
budget verify-data

# Fix common issues
budget repair-data --auto-fix

# Audit trail
budget audit-log --last-days 30
```

## 🎯 Tips and Best Practices

### Effective Categorization

1. **Keep categories broad initially**: Start with 5-10 main categories
2. **Split high-volume categories**: If "Food" becomes too large, split into "Groceries" and "Dining Out"
3. **Use consistent naming**: "Food & Dining", "Transport & Travel", "Health & Fitness"
4. **Consider your goals**: Categories should align with your budgeting priorities

### Budget Setting Guidelines

1. **Start conservative**: Better to exceed a low budget than constantly overspend
2. **Review monthly**: Adjust based on actual spending patterns
3. **Plan for seasonality**: Higher utility costs in summer/winter
4. **Include buffer**: Add 5-10% buffer for unexpected expenses

### Transaction Entry Best Practices

1. **Enter transactions immediately**: Don't wait until end of day
2. **Use descriptive names**: "Gas - Shell Station Main St" vs "Gas"
3. **Be consistent**: Use same description format for recurring items
4. **Review weekly**: Catch and correct any entry errors

### Reporting Workflow

1. **Weekly quick check**: `budget budget-status`
2. **Monthly detailed review**: `budget report monthly`
3. **Quarterly planning**: `budget report custom` for 3-month periods
4. **Yearly assessment**: `budget report yearly --compare`

---

[← Back to Installation](installation.md) | [Next: API Reference →](api.md)