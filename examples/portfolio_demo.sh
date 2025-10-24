#!/bin/bash
# Professional Portfolio Demo Script
# This script creates a realistic financial scenario for demonstration purposes
#
# Author: tara32473
# GitHub: https://github.com/tara32473/budget-manager

echo "🎯 Budget Manager - Professional Portfolio Demo"
echo "=============================================="
echo "This demo creates a realistic 6-month financial scenario"
echo "showing comprehensive personal finance management capabilities."
echo

# Clean slate - remove existing database for demo
rm -f data/budget_manager.db

echo "📋 Setting up comprehensive category system..."
./budget add-category "Salary" "Primary employment income"
./budget add-category "Freelance" "Side project income"
./budget add-category "Investments" "Stock dividends and returns"
./budget add-category "Housing" "Rent, utilities, maintenance"
./budget add-category "Transportation" "Car payments, gas, insurance"
./budget add-category "Food" "Groceries and dining"
./budget add-category "Healthcare" "Medical expenses and insurance"
./budget add-category "Entertainment" "Movies, subscriptions, hobbies"
./budget add-category "Education" "Courses, books, training"
./budget add-category "Savings" "Emergency fund contributions"
./budget add-category "Insurance" "Life, health, auto insurance"
./budget add-category "Utilities" "Electricity, water, internet"
echo "✅ Categories created successfully"
echo

echo "💳 Setting up realistic monthly budgets..."
./budget set-budget Housing 2200.00 monthly
./budget set-budget Transportation 600.00 monthly
./budget set-budget Food 800.00 monthly
./budget set-budget Healthcare 300.00 monthly
./budget set-budget Entertainment 400.00 monthly
./budget set-budget Education 200.00 monthly
./budget set-budget Utilities 250.00 monthly
./budget set-budget Insurance 350.00 monthly
echo "✅ Budgets configured successfully"
echo

echo "💰 Adding 6 months of realistic income data..."

# Monthly salary (consistent)
for month in {1..6}; do
    case $month in
        1) date="2024-05-01" ;;
        2) date="2024-06-01" ;;
        3) date="2024-07-01" ;;
        4) date="2024-08-01" ;;
        5) date="2024-09-01" ;;
        6) date="2024-10-01" ;;
    esac
    ./budget add-transaction -a 6500.00 -d "Software Engineer Salary" -c Salary income --date $date
done

# Freelance income (variable)
./budget add-transaction -a 1200.00 -d "Website development project" -c Freelance income --date 2024-05-15
./budget add-transaction -a 800.00 -d "Code review consultation" -c Freelance income --date 2024-06-20
./budget add-transaction -a 1500.00 -d "Mobile app development" -c Freelance income --date 2024-08-10
./budget add-transaction -a 600.00 -d "Technical writing" -c Freelance income --date 2024-09-25

# Investment returns
./budget add-transaction -a 125.50 -d "Stock dividends - AAPL" -c Investments income --date 2024-06-15
./budget add-transaction -a 89.25 -d "ETF distributions" -c Investments income --date 2024-07-20
./budget add-transaction -a 156.75 -d "Stock dividends - MSFT" -c Investments income --date 2024-09-15

echo "✅ Income transactions added"
echo

echo "🏠 Adding housing and utilities expenses..."
for month in {1..6}; do
    case $month in
        1) date="2024-05-01"; rent_date="2024-05-01"; util_date="2024-05-15" ;;
        2) date="2024-06-01"; rent_date="2024-06-01"; util_date="2024-06-15" ;;
        3) date="2024-07-01"; rent_date="2024-07-01"; util_date="2024-07-15" ;;
        4) date="2024-08-01"; rent_date="2024-08-01"; util_date="2024-08-15" ;;
        5) date="2024-09-01"; rent_date="2024-09-01"; util_date="2024-09-15" ;;
        6) date="2024-10-01"; rent_date="2024-10-01"; util_date="2024-10-15" ;;
    esac
    ./budget add-transaction -a 2200.00 -d "Monthly rent payment" -c Housing expense --date $rent_date
    
    # Utilities vary by season
    if [ $month -le 2 ] || [ $month -ge 5 ]; then
        util_amount="275.50"  # Higher in winter/summer
    else
        util_amount="195.25"  # Lower in spring/fall
    fi
    ./budget add-transaction -a $util_amount -d "Electric & gas bill" -c Utilities expense --date $util_date
done

echo "✅ Housing expenses added"
echo

echo "🚗 Adding transportation expenses..."
# Car payment
for month in {1..6}; do
    case $month in
        1) date="2024-05-05" ;;
        2) date="2024-06-05" ;;
        3) date="2024-07-05" ;;
        4) date="2024-08-05" ;;
        5) date="2024-09-05" ;;
        6) date="2024-10-05" ;;
    esac
    ./budget add-transaction -a 385.50 -d "Car loan payment" -c Transportation expense --date $date
done

# Gas purchases (variable)
./budget add-transaction -a 65.25 -d "Shell gas station" -c Transportation expense --date 2024-05-08
./budget add-transaction -a 58.90 -d "Chevron gas station" -c Transportation expense --date 2024-05-18
./budget add-transaction -a 72.15 -d "Road trip gas" -c Transportation expense --date 2024-06-12
./budget add-transaction -a 61.30 -d "BP gas station" -c Transportation expense --date 2024-06-25
./budget add-transaction -a 69.80 -d "Exxon gas station" -c Transportation expense --date 2024-07-08
./budget add-transaction -a 125.45 -d "Auto insurance premium" -c Transportation expense --date 2024-07-15

echo "✅ Transportation expenses added"
echo

echo "🍽️ Adding food and dining expenses..."
# Grocery shopping (weekly)
groceries=(145.67 128.90 156.23 142.15 138.45 151.78 139.90 147.25 133.60 158.90 144.35 152.80)
dates=("2024-05-04" "2024-05-11" "2024-05-18" "2024-05-25" "2024-06-01" "2024-06-08" 
       "2024-06-15" "2024-06-22" "2024-06-29" "2024-07-06" "2024-07-13" "2024-07-20")

for i in ${!groceries[@]}; do
    ./budget add-transaction -a ${groceries[$i]} -d "Weekly grocery shopping" -c Food expense --date ${dates[$i]}
done

# Dining out
./budget add-transaction -a 45.67 -d "Italian restaurant - date night" -c Food expense --date 2024-05-10
./budget add-transaction -a 28.90 -d "Chipotle lunch" -c Food expense --date 2024-05-14
./budget add-transaction -a 85.50 -d "Team dinner celebration" -c Food expense --date 2024-06-08
./budget add-transaction -a 32.15 -d "Thai takeout" -c Food expense --date 2024-06-20
./budget add-transaction -a 67.80 -d "Weekend brunch" -c Food expense --date 2024-07-15

echo "✅ Food expenses added"
echo

echo "🏥 Adding healthcare expenses..."
./budget add-transaction -a 285.00 -d "Health insurance premium" -c Healthcare expense --date 2024-05-01
./budget add-transaction -a 125.00 -d "Dental cleaning" -c Healthcare expense --date 2024-05-20
./budget add-transaction -a 285.00 -d "Health insurance premium" -c Healthcare expense --date 2024-06-01
./budget add-transaction -a 45.00 -d "Prescription medication" -c Healthcare expense --date 2024-06-15
./budget add-transaction -a 285.00 -d "Health insurance premium" -c Healthcare expense --date 2024-07-01
./budget add-transaction -a 200.00 -d "Annual physical exam" -c Healthcare expense --date 2024-07-25

echo "✅ Healthcare expenses added"
echo

echo "🎬 Adding entertainment and lifestyle expenses..."
./budget add-transaction -a 15.99 -d "Netflix subscription" -c Entertainment expense --date 2024-05-03
./budget add-transaction -a 12.99 -d "Spotify Premium" -c Entertainment expense --date 2024-05-05
./budget add-transaction -a 45.00 -d "Movie tickets and popcorn" -c Entertainment expense --date 2024-05-12
./budget add-transaction -a 89.99 -d "PlayStation game" -c Entertainment expense --date 2024-05-25
./budget add-transaction -a 25.00 -d "Concert tickets" -c Entertainment expense --date 2024-06-18
./budget add-transaction -a 156.78 -d "Weekend camping gear" -c Entertainment expense --date 2024-07-04

echo "✅ Entertainment expenses added"
echo

echo "📚 Adding education and professional development..."
./budget add-transaction -a 49.99 -d "Udemy Python course" -c Education expense --date 2024-05-15
./budget add-transaction -a 29.99 -d "Technical books" -c Education expense --date 2024-06-10
./budget add-transaction -a 199.00 -d "AWS certification exam" -c Education expense --date 2024-07-20
./budget add-transaction -a 79.99 -d "Online React masterclass" -c Education expense --date 2024-08-15

echo "✅ Education expenses added"
echo

echo "💾 Adding savings and investments..."
for month in {1..6}; do
    case $month in
        1) date="2024-05-31" ;;
        2) date="2024-06-30" ;;
        3) date="2024-07-31" ;;
        4) date="2024-08-31" ;;
        5) date="2024-09-30" ;;
        6) date="2024-10-31" ;;
    esac
    ./budget add-transaction -a 1000.00 -d "Emergency fund contribution" -c Savings expense --date $date
done

echo "✅ Savings transactions added"
echo

echo "📊 Generating comprehensive demonstration reports..."
echo
echo "========================================="
echo "📈 FINANCIAL OVERVIEW"
echo "========================================="
./budget report summary

echo
echo "========================================="
echo "📅 DETAILED MONTHLY ANALYSIS"
echo "========================================="
./budget report monthly

echo
echo "========================================="
echo "💳 CURRENT BUDGET STATUS"
echo "========================================="
./budget budget-status

echo
echo "========================================="
echo "📋 RECENT TRANSACTION HISTORY"
echo "========================================="
./budget list-transactions --limit 15

echo
echo "========================================="
echo "🎯 CATEGORY-SPECIFIC ANALYSIS"
echo "========================================="
echo "Food spending analysis:"
./budget list-transactions --category Food --limit 10

echo
echo "========================================="
echo "💰 CUSTOM REPORT - LAST 3 MONTHS"
echo "========================================="
./budget report custom --start-date 2024-08-01 --end-date 2024-10-31

echo
echo "✅ Professional Portfolio Demo Complete!"
echo
echo "🌟 This demonstration showcases:"
echo "   • Comprehensive financial tracking over 6 months"
echo "   • Realistic income from multiple sources"
echo "   • Detailed expense categorization"
echo "   • Budget monitoring and analysis"
echo "   • Professional reporting capabilities"
echo "   • Data-driven financial insights"
echo
echo "💼 Perfect for demonstrating to employers:"
echo "   • Clean, professional codebase"
echo "   • Real-world problem solving"
echo "   • Data management and analysis"
echo "   • User experience design"
echo "   • Software engineering best practices"
echo
echo "🚀 Try exploring the data with various commands:"
echo "   ./budget --help"
echo "   ./budget list-categories"
echo "   ./budget report yearly"
echo "   ./budget list-transactions --last-month"