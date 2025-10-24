# Installation Guide

Complete installation instructions for Budget Manager across different environments.

## 📋 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Storage**: ~50MB for application and data
- **Dependencies**: SQLite (included with Python)

## 🚀 Quick Installation

### Method 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager

# Install the package
pip install -e .

# Verify installation
budget --version
budget --help
```

### Method 2: Download and Install

```bash
# Download the latest release
curl -L https://github.com/tara32473/budget-manager/archive/main.zip -o budget-manager.zip
unzip budget-manager.zip
cd budget-manager-main

# Install
pip install -e .
```

## 🛠️ Development Installation

For contributors and developers who want the full development environment:

```bash
# Clone the repository
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager

# Install in development mode with all dependencies
pip install -e .
pip install -r requirements.txt

# Install pre-commit hooks for code quality
pip install pre-commit
pre-commit install

# Verify development setup
pytest                    # Run tests
make lint                # Run code quality checks
make coverage            # Check test coverage
```

## 🐳 Docker Installation

### Quick Docker Run

```bash
# Pull and run the latest image
docker pull ghcr.io/tara32473/budget-manager:latest
docker run -it --rm ghcr.io/tara32473/budget-manager:latest --help

# Run with persistent data
docker run -it --rm -v $(pwd)/data:/app/data \
    ghcr.io/tara32473/budget-manager:latest list-transactions
```

### Build from Source

```bash
# Clone and build
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager

# Build the Docker image
docker build -t budget-manager .

# Run the container
docker run -it --rm budget-manager --help
```

### Docker Compose

For persistent data and easy management:

```bash
# Start the service
docker-compose up -d

# Use the application
docker-compose exec budget-manager budget --help

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

## 📦 Platform-Specific Installation

### Ubuntu/Debian

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip if not present
sudo apt install python3 python3-pip git -y

# Install Budget Manager
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager
pip3 install -e .

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### CentOS/RHEL/Fedora

```bash
# Install Python and Git
sudo dnf install python3 python3-pip git -y

# Install Budget Manager
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager
pip3 install --user -e .

# Update PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### macOS

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python git

# Install Budget Manager
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager
pip3 install -e .
```

### Windows

**Option 1: Using Git Bash or WSL (Recommended)**
```bash
# In Git Bash or WSL terminal
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager
pip install -e .
```

**Option 2: Command Prompt**
```cmd
# Install Git and Python from their official websites first
git clone https://github.com/tara32473/budget-manager.git
cd budget-manager
pip install -e .
```

## 🏗️ Virtual Environment Setup

### Using venv (Python 3.3+)

```bash
# Create virtual environment
python3 -m venv budget-env

# Activate environment
source budget-env/bin/activate  # Linux/macOS
# budget-env\Scripts\activate   # Windows

# Install Budget Manager
pip install -e .

# Deactivate when done
deactivate
```

### Using conda

```bash
# Create environment
conda create -n budget-manager python=3.9 -y
conda activate budget-manager

# Install Budget Manager
pip install -e .

# Deactivate when done
conda deactivate
```

## ⚙️ Configuration

### Environment Variables

```bash
# Optional: Set custom database location
export BUDGET_DB_PATH="/path/to/your/budget.db"

# Optional: Set default date format
export BUDGET_DATE_FORMAT="%Y-%m-%d"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export BUDGET_DB_PATH="$HOME/Documents/budget.db"' >> ~/.bashrc
```

### Initial Setup

```bash
# Initialize database (automatic on first run)
budget init-db

# Set up basic categories
budget add-category "Food" "Groceries and dining"
budget add-category "Transport" "Gas, public transit, car maintenance"
budget add-category "Housing" "Rent, utilities, maintenance"
budget add-category "Entertainment" "Movies, games, hobbies"

# Set monthly budgets
budget set-budget "Food" 500.00
budget set-budget "Transport" 200.00
budget set-budget "Housing" 1500.00
budget set-budget "Entertainment" 150.00

# Verify setup
budget list-categories
budget budget-status
```

## 🔧 Troubleshooting

### Common Issues

**1. Command not found: budget**
```bash
# Check if installed correctly
pip list | grep budget-manager

# Verify Python scripts directory is in PATH
python -m site --user-base
export PATH="$(python -m site --user-base)/bin:$PATH"
```

**2. Permission denied errors**
```bash
# Install without sudo (user installation)
pip install --user -e .

# Or fix permissions
sudo chown -R $USER:$USER ~/.local/
```

**3. Import errors**
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall with verbose output
pip install -v -e .
```

**4. Database errors**
```bash
# Reset database
rm -f data/budget_manager.db
budget init-db

# Check permissions
ls -la data/
chmod 755 data/
chmod 644 data/budget_manager.db
```

### Getting Help

**Check installation:**
```bash
budget --version
budget --help
python -c "import budget_manager; print('Installation successful')"
```

**Run diagnostics:**
```bash
# Check all components
pytest tests/test_installation.py -v

# Verify CLI functionality  
budget stats
```

**Debug mode:**
```bash
# Run with verbose output
budget --verbose list-transactions

# Check logs
tail -f ~/.budget-manager/logs/app.log
```

## ⬆️ Upgrading

### From Git

```bash
cd budget-manager
git pull origin main
pip install -e .
```

### Backup Before Upgrading

```bash
# Backup your data
cp data/budget_manager.db backups/budget_$(date +%Y%m%d).db

# Backup configuration
cp -r ~/.budget-manager/ backups/config_$(date +%Y%m%d)/
```

## 🗑️ Uninstallation

```bash
# Uninstall the package
pip uninstall budget-manager

# Remove data (optional - be careful!)
rm -rf data/budget_manager.db
rm -rf ~/.budget-manager/

# Remove from PATH if added manually
# Edit ~/.bashrc and remove the export PATH line
```

---

[← Back to Documentation Home](index.md) | [Next: Usage Guide →](usage.md)