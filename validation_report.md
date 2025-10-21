# Data Quality Validation Report
**Total Validations:** 132
**Passed:** 127
**Failed:** 5

---

## Foreign Key Integrity

- **✅ PASS** - FK: account_customers.Account_id
  - account_customers.Account_id -> accounts.Account_id: 0 orphan rows
- **✅ PASS** - FK: account_customers.Customer_id
  - account_customers.Customer_id -> customers.Customer_id: 0 orphan rows
- **✅ PASS** - FK: accounts.Account_Type
  - accounts.Account_Type -> account_type.Account_Type: 0 orphan rows
- **✅ PASS** - FK: accounts.Branch_id
  - accounts.Branch_id -> branches.Branch_id: 0 orphan rows
- **✅ PASS** - FK: banking_transactions.Customer_id
  - banking_transactions.Customer_id -> customers.Customer_id: 0 orphan rows
- **✅ PASS** - FK: branch_employees.Branch_id
  - branch_employees.Branch_id -> branches.Branch_id: 0 orphan rows
- **✅ PASS** - FK: branch_employees.Employee_id
  - branch_employees.Employee_id -> employees.Employee_id: 0 orphan rows
- **✅ PASS** - FK: cc_transactions.CC_Number
  - cc_transactions.CC_Number -> credit_cards.CC_number: 0 orphan rows
- **✅ PASS** - FK: credit_cards.Customer_id
  - credit_cards.Customer_id -> customers.Customer_id: 0 orphan rows
- **✅ PASS** - FK: employees.Supervisor_id
  - employees.Supervisor_id -> employees.Employee_id: 0 orphan rows
- **✅ PASS** - FK: loan.Customer_id
  - loan.Customer_id -> customers.Customer_id: 0 orphan rows

## Column Completeness

- **✅ PASS** - NOT NULL: account_customers.Account_id
  - account_customers.Account_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: account_customers.Customer_id
  - account_customers.Customer_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: account_type.Account_Type
  - account_type.Account_Type: 0 null values in NOT NULL column
- **✅ PASS** - Length: account_type.Account_Type
  - account_type.Account_Type: max length 12/20
- **✅ PASS** - NOT NULL: account_type.Minimum_Balance_Restriction
  - account_type.Minimum_Balance_Restriction: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: accounts.Account_id
  - accounts.Account_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: accounts.Account_Balance
  - accounts.Account_Balance: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: accounts.Branch_id
  - accounts.Branch_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: accounts.Date_Opened
  - accounts.Date_Opened: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: accounts.Account_Type
  - accounts.Account_Type: 0 null values in NOT NULL column
- **✅ PASS** - Length: accounts.Account_Type
  - accounts.Account_Type: max length 12/20
- **✅ PASS** - NOT NULL: banking_transactions.Transaction_id
  - banking_transactions.Transaction_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: banking_transactions.Transaction_Type
  - banking_transactions.Transaction_Type: 0 null values in NOT NULL column
- **✅ PASS** - Length: banking_transactions.Transaction_Type
  - banking_transactions.Transaction_Type: max length 10/45
- **✅ PASS** - Length: banking_transactions.Description
  - banking_transactions.Description: max length 45/45
- **✅ PASS** - NOT NULL: banking_transactions.Amount
  - banking_transactions.Amount: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: banking_transactions.Transaction_Date
  - banking_transactions.Transaction_Date: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: banking_transactions.Customer_id
  - banking_transactions.Customer_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branch_employees.Branch_id
  - branch_employees.Branch_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branch_employees.Employee_id
  - branch_employees.Employee_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branch_employees.Start_Date
  - branch_employees.Start_Date: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branches.Branch_id
  - branches.Branch_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branches.Branch_Name
  - branches.Branch_Name: 0 null values in NOT NULL column
- **✅ PASS** - Length: branches.Branch_Name
  - branches.Branch_Name: max length 30/45
- **✅ PASS** - NOT NULL: branches.Street_Address
  - branches.Street_Address: 0 null values in NOT NULL column
- **✅ PASS** - Length: branches.Street_Address
  - branches.Street_Address: max length 36/50
- **✅ PASS** - NOT NULL: branches.City
  - branches.City: 0 null values in NOT NULL column
- **✅ PASS** - Length: branches.City
  - branches.City: max length 23/25
- **✅ PASS** - NOT NULL: branches.State
  - branches.State: 0 null values in NOT NULL column
- **✅ PASS** - Length: branches.State
  - branches.State: max length 2/2
- **✅ PASS** - NOT NULL: branches.Zipcode
  - branches.Zipcode: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: branches.Phone_Number
  - branches.Phone_Number: 0 null values in NOT NULL column
- **✅ PASS** - Length: branches.Phone_Number
  - branches.Phone_Number: max length 12/12
- **✅ PASS** - NOT NULL: cc_transactions.Transaction_id
  - cc_transactions.Transaction_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: cc_transactions.CC_Number
  - cc_transactions.CC_Number: 0 null values in NOT NULL column
- **✅ PASS** - Length: cc_transactions.CC_Number
  - cc_transactions.CC_Number: max length 16/20
- **✅ PASS** - NOT NULL: cc_transactions.Transaction_Date
  - cc_transactions.Transaction_Date: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: cc_transactions.Amount
  - cc_transactions.Amount: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: cc_transactions.Merchant_Details
  - cc_transactions.Merchant_Details: 0 null values in NOT NULL column
- **✅ PASS** - Length: cc_transactions.Merchant_Details
  - cc_transactions.Merchant_Details: max length 33/45
- **✅ PASS** - NOT NULL: credit_cards.CC_number
  - credit_cards.CC_number: 0 null values in NOT NULL column
- **✅ PASS** - Length: credit_cards.CC_number
  - credit_cards.CC_number: max length 16/20
- **✅ PASS** - NOT NULL: credit_cards.Maximum_Limit
  - credit_cards.Maximum_Limit: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: credit_cards.Expiry_Date
  - credit_cards.Expiry_Date: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: credit_cards.Credit_Score
  - credit_cards.Credit_Score: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: credit_cards.Customer_id
  - credit_cards.Customer_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: customers.Customer_id
  - customers.Customer_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: customers.First_Name
  - customers.First_Name: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.First_Name
  - customers.First_Name: max length 11/45
- **✅ PASS** - NOT NULL: customers.Last_Name
  - customers.Last_Name: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.Last_Name
  - customers.Last_Name: max length 11/45
- **✅ PASS** - NOT NULL: customers.Date_of_Birth
  - customers.Date_of_Birth: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: customers.Street_Address
  - customers.Street_Address: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.Street_Address
  - customers.Street_Address: max length 33/50
- **✅ PASS** - NOT NULL: customers.City
  - customers.City: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.City
  - customers.City: max length 22/25
- **✅ PASS** - NOT NULL: customers.State
  - customers.State: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.State
  - customers.State: max length 2/2
- **✅ PASS** - NOT NULL: customers.Zipcode
  - customers.Zipcode: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: customers.Email
  - customers.Email: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.Email
  - customers.Email: max length 29/45
- **✅ PASS** - NOT NULL: customers.Sex
  - customers.Sex: 0 null values in NOT NULL column
- **✅ PASS** - Length: customers.Sex
  - customers.Sex: max length 1/1
- **✅ PASS** - NOT NULL: employees.Employee_id
  - employees.Employee_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: employees.First_Name
  - employees.First_Name: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.First_Name
  - employees.First_Name: max length 11/45
- **✅ PASS** - NOT NULL: employees.Last_Name
  - employees.Last_Name: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.Last_Name
  - employees.Last_Name: max length 11/45
- **✅ PASS** - NOT NULL: employees.Level_of_Access
  - employees.Level_of_Access: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.Level_of_Access
  - employees.Level_of_Access: max length 7/15
- **✅ PASS** - NOT NULL: employees.Date_of_Birth
  - employees.Date_of_Birth: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: employees.Street_Address
  - employees.Street_Address: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.Street_Address
  - employees.Street_Address: max length 34/50
- **✅ PASS** - NOT NULL: employees.City
  - employees.City: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.City
  - employees.City: max length 20/25
- **✅ PASS** - NOT NULL: employees.State
  - employees.State: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.State
  - employees.State: max length 2/2
- **✅ PASS** - NOT NULL: employees.Zipcode
  - employees.Zipcode: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: employees.Sex
  - employees.Sex: 0 null values in NOT NULL column
- **✅ PASS** - Length: employees.Sex
  - employees.Sex: max length 1/1
- **✅ PASS** - NOT NULL: loan.Loan_id
  - loan.Loan_id: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Duration_in_Years
  - loan.Duration_in_Years: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Loan_Start_Date
  - loan.Loan_Start_Date: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Interest_Rate
  - loan.Interest_Rate: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Loan_Amount_Taken
  - loan.Loan_Amount_Taken: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Loan_Amount_Repaid
  - loan.Loan_Amount_Repaid: 0 null values in NOT NULL column
- **✅ PASS** - NOT NULL: loan.Loan_Type
  - loan.Loan_Type: 0 null values in NOT NULL column
- **✅ PASS** - Length: loan.Loan_Type
  - loan.Loan_Type: max length 8/45
- **✅ PASS** - NOT NULL: loan.Customer_id
  - loan.Customer_id: 0 null values in NOT NULL column

## Business Logic Validation

- **✅ PASS** - Customer Age >= 18
  - 0 customers under 18 years old
- **✅ PASS** - Account Balance >= Minimum
  - 0 accounts below minimum balance
- **✅ PASS** - Loan Repaid <= Taken
  - 0 loans with repaid > taken
- **✅ PASS** - Credit Score Range
  - 0 credit scores outside 300-850 range
- **✅ PASS** - Credit Card Not Expired
  - 0 expired credit cards
- **✅ PASS** - Banking Transaction Amount Range
  - 0 banking transactions outside 1-2500 range
- **✅ PASS** - CC Transaction Amount Range
  - 0 CC transactions outside 1-2500 range

## Temporal Consistency

- **✅ PASS** - Banking Transactions Not Future
  - 0 banking transactions in future
- **✅ PASS** - CC Transactions Not Future
  - 0 CC transactions in future
- **❌ FAIL** - Transactions After Account Open
  - 1911 transactions before account opened
- **✅ PASS** - Employee End >= Start
  - 0 employees with end date before start date

## Uniqueness Constraints

- **❌ FAIL** - PK Unique: account_customers.Customer_id
  - account_customers.Customer_id: 659 total, 363 distinct
- **❌ FAIL** - PK Unique: account_customers.Account_id
  - account_customers.Account_id: 659 total, 500 distinct
- **✅ PASS** - PK Unique: account_type.Account_Type
  - account_type.Account_Type: 5 total, 5 distinct
- **✅ PASS** - PK Unique: accounts.Account_id
  - accounts.Account_id: 500 total, 500 distinct
- **✅ PASS** - PK Unique: banking_transactions.Transaction_id
  - banking_transactions.Transaction_id: 4534 total, 4534 distinct
- **❌ FAIL** - PK Unique: branch_employees.Employee_id
  - branch_employees.Employee_id: 656 total, 500 distinct
- **❌ FAIL** - PK Unique: branch_employees.Branch_id
  - branch_employees.Branch_id: 656 total, 355 distinct
- **✅ PASS** - PK Unique: branches.Branch_id
  - branches.Branch_id: 500 total, 500 distinct
- **✅ PASS** - PK Unique: cc_transactions.Transaction_id
  - cc_transactions.Transaction_id: 5802 total, 5802 distinct
- **✅ PASS** - PK Unique: credit_cards.CC_number
  - credit_cards.CC_number: 320 total, 320 distinct
- **✅ PASS** - PK Unique: customers.Customer_id
  - customers.Customer_id: 500 total, 500 distinct
- **✅ PASS** - PK Unique: employees.Employee_id
  - employees.Employee_id: 500 total, 500 distinct
- **✅ PASS** - PK Unique: loan.Loan_id
  - loan.Loan_id: 180 total, 180 distinct
- **✅ PASS** - Email Unique
  - customers.Email: 500 total, 500 distinct
- **✅ PASS** - CC Number Unique
  - credit_cards.CC_number: 320 total, 320 distinct

## Realistic Distribution

- **✅ PASS** - Account Type Variety
  - 5 distinct account types
- **✅ PASS** - Customer State Variety
  - 54 distinct states
- **✅ PASS** - Transaction Type Variety
  - 4 distinct transaction types

## Data Cleanliness

- **✅ PASS** - Email Trimmed
  - 0 emails with leading/trailing spaces
- **✅ PASS** - Valid Zipcodes
  - 0 invalid zipcodes

## Reproducibility

- **✅ PASS** - Seed-based Generation
  - All tables populated with seed-based generation

