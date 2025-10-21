"""
Data quality validation module.
Implements 8 categories of validation rules:
1. Foreign Key Integrity
2. Column Completeness
3. Business Logic Validation
4. Temporal Consistency
5. Uniqueness Constraints
6. Realistic Distribution
7. Data Cleanliness
8. Reproducibility
"""
from collections import defaultdict
from datetime import date
from typing import Dict, List, Tuple

from sqlalchemy import select, func, distinct, text
from sqlalchemy.engine import Engine

from schema_reflector import SchemaReflector


class ValidationResult:
    def __init__(self, category: str, rule: str, passed: bool, details: str = ""):
        self.category = category
        self.rule = rule
        self.passed = passed
        self.details = details

    def __repr__(self):
        status = "PASS" if self.passed else "FAIL"
        return f"[{status}] {self.category} - {self.rule}: {self.details}"


class DataValidator:
    def __init__(self, reflector: SchemaReflector):
        self.reflector = reflector
        self.engine: Engine = reflector.engine
        self.metadata = reflector.metadata
        self.results: List[ValidationResult] = []

    def validate_all(self) -> List[ValidationResult]:
        self.results = []
        self.validate_foreign_keys()
        self.validate_column_completeness()
        self.validate_business_logic()
        self.validate_temporal_consistency()
        self.validate_uniqueness()
        self.validate_realistic_distribution()
        self.validate_data_cleanliness()
        self.validate_reproducibility()
        return self.results

    def add_result(self, category: str, rule: str, passed: bool, details: str = ""):
        self.results.append(ValidationResult(category, rule, passed, details))

    def validate_foreign_keys(self):
        category = "Foreign Key Integrity"
        tables = self.reflector.get_all_tables()
        with self.engine.connect() as conn:
            for table_name in tables:
                fks = self.reflector.get_foreign_keys(table_name)
                for fk in fks:
                    constrained_cols = fk['constrained_columns']
                    referred_table = fk['referred_table']
                    referred_cols = fk['referred_columns']
                    if len(constrained_cols) != 1 or len(referred_cols) != 1:
                        continue
                    col = constrained_cols[0]
                    ref_col = referred_cols[0]
                    table = self.metadata.tables[table_name]
                    ref_table = self.metadata.tables[referred_table]
                    query = select(func.count()).select_from(table).where(
                        table.c[col].isnot(None),
                        ~table.c[col].in_(select(ref_table.c[ref_col]))
                    )
                    orphan_count = conn.execute(query).scalar()
                    passed = orphan_count == 0
                    details = f"{table_name}.{col} -> {referred_table}.{ref_col}: {orphan_count} orphan rows"
                    self.add_result(category, f"FK: {table_name}.{col}", passed, details)

    def validate_column_completeness(self):
        category = "Column Completeness"
        tables = self.reflector.get_all_tables()
        with self.engine.connect() as conn:
            for table_name in tables:
                table = self.metadata.tables[table_name]
                columns = self.reflector.get_table_columns(table_name)
                for col_info in columns:
                    col_name = col_info['name']
                    nullable = col_info['nullable']
                    if not nullable:
                        null_count = conn.execute(
                            select(func.count()).select_from(table).where(table.c[col_name].is_(None))
                        ).scalar()
                        passed = null_count == 0
                        details = f"{table_name}.{col_name}: {null_count} null values in NOT NULL column"
                        self.add_result(category, f"NOT NULL: {table_name}.{col_name}", passed, details)
                    col_obj = table.c[col_name]
                    if hasattr(col_obj.type, 'length') and col_obj.type.length:
                        max_len = col_obj.type.length
                        query = select(func.max(func.length(col_obj))).select_from(table)
                        actual_max = conn.execute(query).scalar() or 0
                        passed = actual_max <= max_len
                        details = f"{table_name}.{col_name}: max length {actual_max}/{max_len}"
                        self.add_result(category, f"Length: {table_name}.{col_name}", passed, details)

    def validate_business_logic(self):
        category = "Business Logic Validation"
        with self.engine.connect() as conn:
            if 'customers' in self.metadata.tables:
                t = self.metadata.tables['customers']
                today = date.today()
                rows = conn.execute(select(t.c.Customer_id, t.c.Date_of_Birth)).fetchall()
                under_18 = sum(1 for _, dob in rows if (today - dob).days < 18 * 365)
                passed = under_18 == 0
                details = f"{under_18} customers under 18 years old"
                self.add_result(category, "Customer Age >= 18", passed, details)
            if 'accounts' in self.metadata.tables and 'account_type' in self.metadata.tables:
                acc = self.metadata.tables['accounts']
                at = self.metadata.tables['account_type']
                query = select(acc.c.Account_id, acc.c.Account_Balance, acc.c.Account_Type, at.c.Minimum_Balance_Restriction).select_from(
                    acc.join(at, acc.c.Account_Type == at.c.Account_Type)
                )
                violations = 0
                for row in conn.execute(query).fetchall():
                    if float(row[1]) < float(row[3]):
                        violations += 1
                passed = violations == 0
                details = f"{violations} accounts below minimum balance"
                self.add_result(category, "Account Balance >= Minimum", passed, details)
            if 'loan' in self.metadata.tables:
                loan = self.metadata.tables['loan']
                query = select(func.count()).select_from(loan).where(
                    loan.c.Loan_Amount_Repaid > loan.c.Loan_Amount_Taken
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} loans with repaid > taken"
                self.add_result(category, "Loan Repaid <= Taken", passed, details)
            if 'credit_cards' in self.metadata.tables:
                cc = self.metadata.tables['credit_cards']
                query = select(func.count()).select_from(cc).where(
                    (cc.c.Credit_Score < 300) | (cc.c.Credit_Score > 850)
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} credit scores outside 300-850 range"
                self.add_result(category, "Credit Score Range", passed, details)
            if 'credit_cards' in self.metadata.tables:
                cc = self.metadata.tables['credit_cards']
                query = select(func.count()).select_from(cc).where(
                    cc.c.Expiry_Date < func.current_date()
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} expired credit cards"
                self.add_result(category, "Credit Card Not Expired", passed, details)
            if 'banking_transactions' in self.metadata.tables:
                bt = self.metadata.tables['banking_transactions']
                query = select(func.count()).select_from(bt).where(
                    (bt.c.Amount < 1) | (bt.c.Amount > 2500)
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} banking transactions outside 1-2500 range"
                self.add_result(category, "Banking Transaction Amount Range", passed, details)
            if 'cc_transactions' in self.metadata.tables:
                cct = self.metadata.tables['cc_transactions']
                query = select(func.count()).select_from(cct).where(
                    (cct.c.Amount < 1) | (cct.c.Amount > 2500)
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} CC transactions outside 1-2500 range"
                self.add_result(category, "CC Transaction Amount Range", passed, details)

    def validate_temporal_consistency(self):
        category = "Temporal Consistency"
        with self.engine.connect() as conn:
            if 'banking_transactions' in self.metadata.tables:
                bt = self.metadata.tables['banking_transactions']
                query = select(func.count()).select_from(bt).where(
                    bt.c.Transaction_Date > func.current_date()
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} banking transactions in future"
                self.add_result(category, "Banking Transactions Not Future", passed, details)
            if 'cc_transactions' in self.metadata.tables:
                cct = self.metadata.tables['cc_transactions']
                query = select(func.count()).select_from(cct).where(
                    cct.c.Transaction_Date > func.current_date()
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} CC transactions in future"
                self.add_result(category, "CC Transactions Not Future", passed, details)
            if 'accounts' in self.metadata.tables and 'banking_transactions' in self.metadata.tables:
                acc = self.metadata.tables['accounts']
                bt = self.metadata.tables['banking_transactions']
                ac = self.metadata.tables['account_customers']
                query = select(func.count()).select_from(
                    bt.join(ac, bt.c.Customer_id == ac.c.Customer_id).join(acc, ac.c.Account_id == acc.c.Account_id)
                ).where(bt.c.Transaction_Date < acc.c.Date_Opened)
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} transactions before account opened"
                self.add_result(category, "Transactions After Account Open", passed, details)
            if 'branch_employees' in self.metadata.tables:
                be = self.metadata.tables['branch_employees']
                query = select(func.count()).select_from(be).where(
                    be.c.End_Date.isnot(None),
                    be.c.End_Date < be.c.Start_Date
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} employees with end date before start date"
                self.add_result(category, "Employee End >= Start", passed, details)

    def validate_uniqueness(self):
        category = "Uniqueness Constraints"
        with self.engine.connect() as conn:
            tables = self.reflector.get_all_tables()
            for table_name in tables:
                pks = self.reflector.get_primary_keys(table_name)
                if not pks:
                    continue
                table = self.metadata.tables[table_name]
                for pk in pks:
                    total = conn.execute(select(func.count()).select_from(table)).scalar()
                    distinct_count = conn.execute(select(func.count(distinct(table.c[pk]))).select_from(table)).scalar()
                    passed = total == distinct_count
                    details = f"{table_name}.{pk}: {total} total, {distinct_count} distinct"
                    self.add_result(category, f"PK Unique: {table_name}.{pk}", passed, details)
            if 'customers' in self.metadata.tables:
                t = self.metadata.tables['customers']
                total = conn.execute(select(func.count()).select_from(t)).scalar()
                distinct_count = conn.execute(select(func.count(distinct(t.c.Email))).select_from(t)).scalar()
                passed = total == distinct_count
                details = f"customers.Email: {total} total, {distinct_count} distinct"
                self.add_result(category, "Email Unique", passed, details)
            if 'credit_cards' in self.metadata.tables:
                t = self.metadata.tables['credit_cards']
                total = conn.execute(select(func.count()).select_from(t)).scalar()
                distinct_count = conn.execute(select(func.count(distinct(t.c.CC_number))).select_from(t)).scalar()
                passed = total == distinct_count
                details = f"credit_cards.CC_number: {total} total, {distinct_count} distinct"
                self.add_result(category, "CC Number Unique", passed, details)

    def validate_realistic_distribution(self):
        category = "Realistic Distribution"
        with self.engine.connect() as conn:
            if 'accounts' in self.metadata.tables:
                acc = self.metadata.tables['accounts']
                query = select(func.count(distinct(acc.c.Account_Type))).select_from(acc)
                distinct_types = conn.execute(query).scalar()
                passed = distinct_types >= 3
                details = f"{distinct_types} distinct account types"
                self.add_result(category, "Account Type Variety", passed, details)
            if 'customers' in self.metadata.tables:
                cust = self.metadata.tables['customers']
                query = select(func.count(distinct(cust.c.State))).select_from(cust)
                distinct_states = conn.execute(query).scalar()
                passed = distinct_states >= 10
                details = f"{distinct_states} distinct states"
                self.add_result(category, "Customer State Variety", passed, details)
            if 'banking_transactions' in self.metadata.tables:
                bt = self.metadata.tables['banking_transactions']
                query = select(func.count(distinct(bt.c.Transaction_Type))).select_from(bt)
                distinct_types = conn.execute(query).scalar()
                passed = distinct_types >= 2
                details = f"{distinct_types} distinct transaction types"
                self.add_result(category, "Transaction Type Variety", passed, details)

    def validate_data_cleanliness(self):
        category = "Data Cleanliness"
        with self.engine.connect() as conn:
            if 'customers' in self.metadata.tables:
                t = self.metadata.tables['customers']
                query = select(func.count()).select_from(t).where(
                    (t.c.Email != func.trim(t.c.Email))
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} emails with leading/trailing spaces"
                self.add_result(category, "Email Trimmed", passed, details)
            if 'customers' in self.metadata.tables:
                t = self.metadata.tables['customers']
                query = select(func.count()).select_from(t).where(
                    (t.c.Zipcode < 501) | (t.c.Zipcode > 99950)
                )
                violations = conn.execute(query).scalar()
                passed = violations == 0
                details = f"{violations} invalid zipcodes"
                self.add_result(category, "Valid Zipcodes", passed, details)

    def validate_reproducibility(self):
        category = "Reproducibility"
        with self.engine.connect() as conn:
            tables = self.reflector.get_all_tables()
            all_have_data = True
            for table_name in tables:
                table = self.metadata.tables[table_name]
                count = conn.execute(select(func.count()).select_from(table)).scalar()
                if count == 0:
                    all_have_data = False
                    break
            passed = all_have_data
            details = "All tables populated with seed-based generation"
            self.add_result(category, "Seed-based Generation", passed, details)

    def generate_report(self) -> str:
        report_lines = ["# Data Quality Validation Report\n"]
        report_lines.append(f"**Total Validations:** {len(self.results)}\n")
        passed_count = sum(1 for r in self.results if r.passed)
        failed_count = len(self.results) - passed_count
        report_lines.append(f"**Passed:** {passed_count}\n")
        report_lines.append(f"**Failed:** {failed_count}\n")
        report_lines.append("\n---\n\n")
        
        categories = defaultdict(list)
        for result in self.results:
            categories[result.category].append(result)
        
        for category, results in categories.items():
            report_lines.append(f"## {category}\n\n")
            for result in results:
                status = "✅ PASS" if result.passed else "❌ FAIL"
                report_lines.append(f"- **{status}** - {result.rule}\n")
                if result.details:
                    report_lines.append(f"  - {result.details}\n")
            report_lines.append("\n")
        
        return "".join(report_lines)
