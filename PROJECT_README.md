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

## Project Structure

```
MockData/
├── main.py                 # Main orchestration script
├── config.py              # Configuration and environment variables
├── schema_reflector.py    # SQLAlchemy schema reflection
├── data_generator.py      # Mock data generation engine
├── data_validator.py      # Data quality validation
├── data_exporter.py       # JSON/CSV export functionality
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment configuration
├── Sql_code.txt          # MySQL schema definition
├── SETUP.md              # Setup instructions
└── exports/              # Generated export files (created at runtime)
```

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

## Example Output

```
================================================================================
  MySQL Mock Data Generation and Validation System
================================================================================

Configuration:
  Database: citi_db
  Host: localhost:3306
  Random Seed: 42
  Customers: 500
  Employees: 500
  Branches: 500
  Accounts: 500

Step 1: Connecting to database and reflecting schema...
  ✓ Found 11 tables: customers, account_type, branches, ...
  ✓ Determined insertion order: account_type -> customers -> ...

Step 2: Generating mock data...
  - Truncating existing data...
  - Generating and inserting data...
  ✓ Data generation completed in 12.34 seconds

Step 3: Validating data quality...
  ✓ Validation completed: 45 passed, 0 failed

Step 4: Generating validation report...
  ✓ Validation report saved to: validation_report.md

Step 5: Exporting data to JSON and CSV...
  ✓ Exported 11 tables to ./exports/
    - customers: customers.json, customers.csv
    - accounts: accounts.json, accounts.csv
    ...

Step 6: Summary...
  Total records generated: 15,234
    - customers: 500 records
    - accounts: 500 records
    - banking_transactions: 6,250 records
    ...

================================================================================
  ✓ All operations completed successfully!
================================================================================
```

## Technical Details

### Data Generation Strategy

1. **Topological Sorting** - Tables are inserted in dependency order to satisfy foreign key constraints
2. **Realistic Faker Data** - Uses Faker library with appropriate providers for each field type
3. **Business Rule Enforcement** - Post-generation validation and adjustment to ensure all business rules are met
4. **Relationship Management** - Maintains referential integrity across all table relationships

### Validation Approach

- **Pre-commit Validation** - Business rules enforced during generation
- **Post-commit Validation** - Comprehensive checks across all 8 categories
- **Detailed Reporting** - Clear identification of any issues with specific counts and details

### Performance Considerations

- Batch inserts for efficiency
- Connection pooling via SQLAlchemy
- Optimized queries for validation checks
- Typical runtime: 10-30 seconds for 500 records per main table

## Requirements

- Python 3.8+
- MySQL 5.7+
- SQLAlchemy 2.0+
- PyMySQL 1.1+
- Faker 20.1+
- python-dotenv 1.0+

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
