#!/bin/bash
# Quick Start Demo - Perfect for Live Interviews
# This script demonstrates the Budget Manager in under 2 minutes
#
# Author: tara32473
# GitHub: https://github.com/tara32473/budget-manager

echo "🚀 Budget Manager - Quick Interview Demo"
echo "========================================"
echo "Showcasing professional personal finance management"
echo

# Clean start for consistent demo
rm -f data/budget_manager.db

echo "⚡ Step 1: Setting up core categories (5 seconds)"
./budget add-category "Salary" "Primary employment income" > /dev/null
./budget add-category "Housing" "Rent and utilities" > /dev/null
./budget add-category "Food" "Groceries and dining" > /dev/null
./budget add-category "Transport" "Car and commuting" > /dev/null
echo "✅ 4 categories created"

echo
echo "💳 Step 2: Setting realistic budgets (3 seconds)"
./budget set-budget Housing 2000.00 monthly > /dev/null
./budget set-budget Food 600.00 monthly > /dev/null
./budget set-budget Transport 400.00 monthly > /dev/null
echo "✅ Monthly budgets configured"

echo
echo "💰 Step 3: Adding sample transactions (5 seconds)"
./budget add-transaction -a 5000.00 -d "Software Engineer Salary" -c Salary income > /dev/null
./budget add-transaction -a 2000.00 -d "Monthly rent payment" -c Housing expense > /dev/null
./budget add-transaction -a 150.00 -d "Weekly groceries" -c Food expense > /dev/null
./budget add-transaction -a 65.00 -d "Gas station fill-up" -c Transport expense > /dev/null
./budget add-transaction -a 45.00 -d "Restaurant dinner" -c Food expense > /dev/null
echo "✅ 5 sample transactions added"

echo
echo "📊 Live Financial Dashboard:"
echo "============================"

echo
echo "💳 Current Budget Status:"
./budget budget-status

echo
echo "📋 Recent Transactions:"
./budget list-transactions --limit 5

echo
echo "📈 Financial Summary:"
./budget report summary

echo
echo "🎯 Demo Complete! Key Features Shown:"
echo "• ✅ Category-based transaction management"
echo "• ✅ Budget setting and real-time monitoring"
echo "• ✅ Comprehensive financial reporting"
echo "• ✅ Clean, professional CLI interface"
echo "• ✅ Data persistence and integrity"
echo
echo "💼 Perfect for demonstrating:"
echo "• Software engineering best practices"
echo "• Database design and operations"
echo "• User experience design"
echo "• Real-world problem solving"
echo "• Professional code organization"

echo
echo "🔍 Try exploring more:"
echo "  ./budget --help                    # See all available commands"
echo "  ./budget report monthly           # Generate detailed reports"
echo "  ./budget add-category Tech 'Equipment'  # Add custom categories"
echo "  ./examples/portfolio_demo.sh      # Run comprehensive 6-month demo"