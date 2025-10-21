# MySQL Mock Data Generation and Validation System

A comprehensive Python-based system that dynamically connects to MySQL databases, reflects their schema automatically, and generates synthetic but realistic mock data while enforcing referential integrity, business rules, and data quality validations.

## Features

### 🔄 Automatic Schema Reflection
- Dynamically detects all tables, columns, primary keys, and foreign keys
- No hardcoding of table definitions required
- Automatically determines safe insertion order based on dependencies

### 🎲 Intelligent Data Generation
- Uses Faker library for realistic names, addresses, and transaction data
- Configurable record counts for main tables
- Dependent tables populated based on logical relationships
- Respects column length constraints and data types
- Enforces foreign key safe insertion order

### ✅ Comprehensive Data Validation (8 Categories)

1. **Foreign Key Integrity** - No orphan rows; all references exist
2. **Column Completeness** - No nulls in required fields; strings within varchar limits
3. **Business Logic Validation**
   - Customers aged ≥ 18
   - Account balance ≥ minimum restriction
   - Loan repaid ≤ taken; realistic interest and duration
   - Credit scores 300–850
   - Credit card expiry dates in future
   - Transaction amounts 1–2,500
4. **Temporal Consistency**
   - No future dates in transactions
   - Account opened before transactions
   - Employee end date ≥ start date
5. **Uniqueness Constraints**
   - Unique primary keys
   - Unique emails
   - Unique credit card numbers
6. **Realistic Distribution**
   - Variety in account types, states, transaction types
   - No uniform values
7. **Data Cleanliness**
   - No leading/trailing spaces
   - Valid zipcodes
8. **Reproducibility**
   - Controlled by random seed from .env
   - Same seed produces identical data

### 📤 Multi-Format Export
- JSON export for each table
- CSV export for each table
- Organized in `./exports/` directory

### 📊 Validation Reporting
- Comprehensive `validation_report.md` with pass/fail results
- Detailed breakdown by validation category
- Clear identification of any data quality issues

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
mysql -u root -p < Sql_code.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Run the System

```bash
python main.py
```

## Database Schema

The system works with the following banking database schema:

- **customers** - Customer information
- **account_type** - Types of accounts with minimum balance requirements
- **branches** - Bank branch locations
- **employees** - Employee records with supervisor relationships
- **accounts** - Bank accounts linked to branches and account types
- **account_customers** - Many-to-many relationship between accounts and customers
- **banking_transactions** - Banking transaction history
- **credit_cards** - Credit card information
- **cc_transactions** - Credit card transaction history
- **loan** - Loan records
- **branch_employees** - Employee-branch assignments with date ranges

## Configuration

Edit `.env` to customize:

```env
# Database Connection
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=citi_db

# Data Generation
RANDOM_SEED=42              # For reproducibility
NUM_CUSTOMERS=500           # Number of customers
NUM_EMPLOYEES=500           # Number of employees
NUM_BRANCHES=500            # Number of branches
NUM_ACCOUNTS=500            # Number of accounts
```

## Output

After running, you'll find:

1. **validation_report.md** - Detailed validation results
2. **exports/*.json** - JSON files for each table
3. **exports/*.csv** - CSV files for each table

## Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [PROJECT_README.md](PROJECT_README.md) - Complete project documentation

## Requirements

- Python 3.8+
- MySQL 5.7+
- SQLAlchemy 2.0+
- PyMySQL 1.1+
- Faker 20.1+
- python-dotenv 1.0+

## Testing

Run the test suite to verify the system:

```bash
python test_system.py
```

## Legacy Scripts

The repository also contains legacy SQLite-based scripts:
- `database_setup.py` - Original SQLite database setup
- `data_extraction.py` - Original SQLite data extraction

These are kept for reference but the new MySQL system is recommended.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Faker](https://faker.readthedocs.io/en/master/)
