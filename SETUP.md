# Setup Guide

This guide will help you set up the MySQL Mock Data Generation and Validation System.

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package installer)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/ganne-sriram/MockData.git
cd MockData
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

First, create the database and tables using the provided SQL schema:

```bash
mysql -u root -p < Sql_code.txt
```

This will:
- Create the `citi_db` database
- Create all required tables with proper constraints
- Set up foreign key relationships

### 4. Configure Environment Variables

Copy the example environment file and edit it with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=citi_db

# Data Generation Configuration
RANDOM_SEED=42
NUM_CUSTOMERS=500
NUM_EMPLOYEES=500
NUM_BRANCHES=500
NUM_ACCOUNTS=500
```

### 5. Verify Connection

You can verify your database connection by running:

```bash
python -c "from config import Config; print(Config.get_database_url())"
```

## Running the System

Once setup is complete, run the main script:

```bash
python main.py
```

This will:
1. Connect to the database and reflect the schema
2. Generate mock data for all tables
3. Validate data quality across 8 categories
4. Export data to JSON and CSV formats
5. Generate a validation report

## Output Files

After running, you'll find:

- `validation_report.md` - Comprehensive validation report
- `exports/*.json` - JSON files for each table
- `exports/*.csv` - CSV files for each table

## Troubleshooting

### Connection Issues

If you encounter connection errors:

1. Verify MySQL is running: `mysql -u root -p`
2. Check credentials in `.env` file
3. Ensure the database exists: `SHOW DATABASES;`
4. Verify user permissions: `SHOW GRANTS FOR 'your_user'@'localhost';`

### Import Errors

If you get Python import errors:

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check Python version: `python --version` (should be 3.8+)
3. Verify you're in the correct directory

### Data Generation Issues

If data generation fails:

1. Check that all tables exist: `SHOW TABLES;`
2. Verify foreign key constraints are properly set up
3. Review error messages in the console output

## Configuration Options

You can customize data generation by modifying `.env`:

- `RANDOM_SEED` - Controls reproducibility (same seed = same data)
- `NUM_CUSTOMERS` - Number of customer records to generate
- `NUM_EMPLOYEES` - Number of employee records to generate
- `NUM_BRANCHES` - Number of branch records to generate
- `NUM_ACCOUNTS` - Number of account records to generate

Dependent tables (transactions, credit cards, loans) are generated based on logical relationships with main tables.
