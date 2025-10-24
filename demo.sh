#!/bin/bash
# Budget Manager Demo Script
# This script demonstrates the full functionality of the budget manager

echo "🎯 Budget Manager Demo - Personal Finance Tracking"
echo "=================================================="
echo

echo "📋 Step 1: Setting up categories"
./budget add-category Food "Groceries and dining expenses"
./budget add-category Transport "Car, gas, public transport"
./budget add-category Entertainment "Movies, games, subscriptions"
./budget add-category Utilities "Electricity, water, internet"
echo

echo "📊 Step 2: Viewing all categories"
./budget list-categories
echo

echo "💰 Step 3: Setting monthly budgets"
./budget set-budget Food 400.00 monthly
./budget set-budget Transport 200.00 monthly
./budget set-budget Entertainment 100.00 monthly
./budget set-budget Utilities 150.00 monthly
echo

echo "💵 Step 4: Adding income"
./budget add-transaction -a 3000.00 -d "Monthly salary" income
./budget add-transaction -a 500.00 -d "Freelance work" income
echo

echo "🛒 Step 5: Adding expenses"
./budget add-transaction -a 85.50 -d "Grocery shopping" -c Food expense
./budget add-transaction -a 45.00 -d "Gas station" -c Transport expense
./budget add-transaction -a 12.99 -d "Netflix subscription" -c Entertainment expense
./budget add-transaction -a 75.25 -d "Electricity bill" -c Utilities expense
./budget add-transaction -a 35.00 -d "Restaurant dinner" -c Food expense
echo

echo "📈 Step 6: Checking budget status"
./budget budget-status
echo

echo "📋 Step 7: Viewing recent transactions"
./budget list-transactions --limit 10
echo

echo "📊 Step 8: Generating comprehensive monthly report"
./budget report monthly
echo

echo "✅ Demo completed! Your budget manager is ready to use."
echo "Run './budget --help' to see all available commands."