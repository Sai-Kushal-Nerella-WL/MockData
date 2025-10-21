from __future__ import annotations
from collections import defaultdict
from datetime import date, timedelta
import random
from typing import Dict, List, Tuple

from sqlalchemy import create_engine, MetaData, Table, select, insert, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from config import Config
from schema_reflector import SchemaReflector
from utils import (
    get_faker,
    ensure_max_length,
    random_state_us,
    random_sex,
    future_date,
    past_date,
    dob_for_age,
    random_phone,
    random_cc_number,
)


class DataGenerator:
    def __init__(self, database_url: str | None = None, seed: int | None = None):
        self.database_url = database_url or Config.get_database_url()
        self.seed = seed if seed is not None else Config.RANDOM_SEED
        self.fake = get_faker(self.seed)
        self.reflector = SchemaReflector(self.database_url)
        self.metadata = MetaData()
        self.engine: Engine = self.reflector.engine
        self.metadata.reflect(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self._table_objs: Dict[str, Table] = {t.name: t for t in self.metadata.sorted_tables}

    def table(self, name: str) -> Table:
        return self._table_objs[name]

    def truncate_all(self):
        with self.engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            order = self.reflector.get_table_dependencies()
            for tname in reversed(order):
                if tname in self._table_objs:
                    conn.execute(self.table(tname).delete())
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    def _string_len(self, table: Table, col_name: str):
        col = table.c[col_name]
        try:
            return getattr(col.type, 'length', None)
        except Exception:
            return None

    def generate_account_type(self) -> List[dict]:
        t = self.table('account_type')
        rows = []
        base = [
            ('Checking', 0.00),
            ('Savings', 100.00),
            ('Business', 1000.00),
            ('Student', 25.00),
            ('Money Market', 2500.00),
        ]
        for name, min_bal in base:
            name = ensure_max_length(name, self._string_len(t, 'Account_Type'))
            rows.append({'Account_Type': name, 'Minimum_Balance_Restriction': float(min_bal)})
        return rows

    def generate_branches(self, n: int) -> List[dict]:
        t = self.table('branches')
        rows = []
        for _ in range(n):
            street = ensure_max_length(self.fake.street_address(), self._string_len(t, 'Street_Address'))
            city = ensure_max_length(self.fake.city(), self._string_len(t, 'City'))
            state = ensure_max_length(random_state_us(self.fake), self._string_len(t, 'State'))
            phone = ensure_max_length(random_phone(self.fake), self._string_len(t, 'Phone_Number'))
            rows.append({
                'Branch_Name': ensure_max_length(f"{city} Branch", self._string_len(t, 'Branch_Name')),
                'Street_Address': street,
                'City': city,
                'State': state,
                'Zipcode': int(self.fake.postcode().split('-')[0][:5] or 10000),
                'Phone_Number': phone,
            })
        return rows

    def generate_customers(self, n: int) -> List[dict]:
        t = self.table('customers')
        rows = []
        emails = set()
        for _ in range(n):
            first = ensure_max_length(self.fake.first_name(), self._string_len(t, 'First_Name'))
            last = ensure_max_length(self.fake.last_name(), self._string_len(t, 'Last_Name'))
            dob = dob_for_age(self.fake, 18, 90)
            email = self.fake.unique.email()
            email = ensure_max_length(email, self._string_len(t, 'Email'))
            while email in emails:
                email = ensure_max_length(self.fake.unique.email(), self._string_len(t, 'Email'))
            emails.add(email)
            rows.append({
                'First_Name': first,
                'Last_Name': last,
                'Date_of_Birth': dob,
                'Street_Address': ensure_max_length(self.fake.street_address(), self._string_len(t, 'Street_Address')),
                'City': ensure_max_length(self.fake.city(), self._string_len(t, 'City')),
                'State': ensure_max_length(random_state_us(self.fake), self._string_len(t, 'State')),
                'Zipcode': int(self.fake.postcode().split('-')[0][:5] or 10000),
                'Email': email,
                'Sex': ensure_max_length(random_sex(), self._string_len(t, 'Sex')),
            })
        return rows

    def generate_employees(self, n: int) -> List[dict]:
        t = self.table('employees')
        rows = []
        for _ in range(n):
            rows.append({
                'First_Name': ensure_max_length(self.fake.first_name(), self._string_len(t, 'First_Name')),
                'Last_Name': ensure_max_length(self.fake.last_name(), self._string_len(t, 'Last_Name')),
                'Supervisor_id': None,  # fill later probabilistically
                'Level_of_Access': ensure_max_length(random.choice(['Teller', 'Manager', 'Analyst', 'Clerk']), self._string_len(t, 'Level_of_Access')),
                'Date_of_Birth': dob_for_age(self.fake, 21, 70),
                'Street_Address': ensure_max_length(self.fake.street_address(), self._string_len(t, 'Street_Address')),
                'City': ensure_max_length(self.fake.city(), self._string_len(t, 'City')),
                'State': ensure_max_length(random_state_us(self.fake), self._string_len(t, 'State')),
                'Zipcode': int(self.fake.postcode().split('-')[0][:5] or 10000),
                'Sex': ensure_max_length(random_sex(), self._string_len(t, 'Sex')),
            })
        return rows

    def generate_accounts(self, n: int, branch_ids: List[int], account_types: List[str]) -> List[dict]:
        t = self.table('accounts')
        rows = []
        for _ in range(n):
            atype = random.choice(account_types)
            branch_id = random.choice(branch_ids)
            date_opened = past_date(self.fake, 0, 20)
            rows.append({
                'Account_Balance': round(random.uniform(0, 50000), 2),
                'Branch_id': branch_id,
                'Date_Opened': date_opened,
                'Account_Type': atype,
            })
        return rows

    def generate_account_customers(self, account_ids: List[int], customer_ids: List[int]) -> List[dict]:
        t = self.table('account_customers')
        rows = []
        used_pairs = set()
        for acc_id in account_ids:
            owners = random.sample(customer_ids, k=random.choice([1, 1, 2]))
            for cust_id in owners:
                key = (cust_id, acc_id)
                if key not in used_pairs:
                    rows.append({'Account_id': acc_id, 'Customer_id': cust_id})
                    used_pairs.add(key)
        return rows

    def generate_banking_transactions(self, customer_ids_with_account: List[int]) -> List[dict]:
        t = self.table('banking_transactions')
        rows = []
        tx_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
        for cust_id in customer_ids_with_account:
            for _ in range(random.randint(5, 20)):
                amount = round(random.uniform(1, 2500), 2)
                tx_date = past_date(self.fake, 0, 10)
                rows.append({
                    'Transaction_Type': ensure_max_length(random.choice(tx_types), self._string_len(t, 'Transaction_Type')),
                    'Description': ensure_max_length(self.fake.sentence(nb_words=4), self._string_len(t, 'Description')),
                    'Amount': amount,
                    'Transaction_Date': tx_date,
                    'Customer_id': cust_id,
                })
        return rows

    def generate_credit_cards(self, customer_ids: List[int]) -> List[dict]:
        t = self.table('credit_cards')
        rows = []
        seen = set()
        for cust_id in customer_ids:
            if random.random() < 0.6:
                cc = random_cc_number()
                while cc in seen:
                    cc = random_cc_number()
                seen.add(cc)
                rows.append({
                    'CC_number': ensure_max_length(cc, self._string_len(t, 'CC_number')),
                    'Maximum_Limit': round(random.uniform(1000, 20000), 2),
                    'Expiry_Date': future_date(self.fake, 1, 5),
                    'Credit_Score': random.randint(300, 850),
                    'Customer_id': cust_id,
                })
        return rows

    def generate_cc_transactions(self, cards: List[dict]) -> List[dict]:
        t = self.table('cc_transactions')
        rows = []
        for card in cards:
            cc_number = card['CC_number']
            expiry = card['Expiry_Date']
            for _ in range(random.randint(5, 30)):
                tx_date = past_date(self.fake, 0, 5)
                if tx_date > expiry:
                    tx_date = expiry - timedelta(days=random.randint(1, 365))
                rows.append({
                    'CC_Number': cc_number,
                    'Transaction_Date': tx_date,
                    'Amount': round(random.uniform(1, 2500), 2),
                    'Merchant_Details': ensure_max_length(self.fake.company(), self._string_len(t, 'Merchant_Details')),
                })
        return rows

    def generate_loans(self, customer_ids: List[int]) -> List[dict]:
        t = self.table('loan')
        rows = []
        for cust_id in customer_ids:
            if random.random() < 0.35:
                amount_taken = round(random.uniform(2000, 100000), 2)
                repaid = round(random.uniform(0, amount_taken), 2)
                duration_years = round(random.uniform(0.5, 30.0), 2)
                start_date = past_date(self.fake, 0, 15)
                rows.append({
                    'Duration_in_Years': duration_years,
                    'Loan_Start_Date': start_date,
                    'Interest_Rate': round(random.uniform(2.5, 18.0), 2),
                    'Loan_Amount_Taken': amount_taken,
                    'Loan_Amount_Repaid': repaid,
                    'Loan_Type': ensure_max_length(random.choice(['Home', 'Auto', 'Personal', 'Student']), self._string_len(t, 'Loan_Type')),
                    'Customer_id': cust_id,
                })
        return rows

    def generate_branch_employees(self, branch_ids: List[int], employee_ids: List[int]) -> List[dict]:
        t = self.table('branch_employees')
        rows = []
        pairs = set()
        for emp_id in employee_ids:
            for _ in range(random.choice([1, 1, 2])):
                br = random.choice(branch_ids)
                key = (emp_id, br)
                if key in pairs:
                    continue
                start = past_date(self.fake, 0, 10)
                if random.random() < 0.7:
                    end = start + timedelta(days=random.randint(30, 2000))
                    if end > date.today():
                        end = None
                else:
                    end = None
                rows.append({'Branch_id': br, 'Employee_id': emp_id, 'Start_Date': start, 'End_Date': end})
                pairs.add(key)
        return rows

    def enforce_business_rules(self, conn):
        at = self.table('account_type')
        ac = self.table('accounts')
        res = conn.execute(select(at.c.Account_Type, at.c.Minimum_Balance_Restriction))
        min_map = {r[0]: float(r[1]) for r in res.fetchall()}
        res2 = conn.execute(select(ac.c.Account_id, ac.c.Account_Type, ac.c.Account_Balance))
        for acc_id, atype, bal in res2.fetchall():
            min_req = min_map.get(atype, 0.0)
            if float(bal) < min_req:
                new_bal = round(random.uniform(min_req, max(min_req + 1000, min_req + 1)), 2)
                conn.execute(ac.update().where(ac.c.Account_id == acc_id).values(Account_Balance=new_bal))
        emp = self.table('employees')
        ids = [row[0] for row in conn.execute(select(emp.c.Employee_id)).fetchall()]
        for e in ids:
            if random.random() < 0.6:
                sup = random.choice(ids)
                if sup != e:
                    conn.execute(emp.update().where(emp.c.Employee_id == e).values(Supervisor_id=sup))

    def generate_and_insert_all(self):
        with self.engine.begin() as conn:
            if 'account_type' in self._table_objs:
                types = self.generate_account_type()
                if types:
                    conn.execute(insert(self.table('account_type')), types)
            branches = self.generate_branches(Config.NUM_BRANCHES)
            result = conn.execute(insert(self.table('branches')), branches)
            branch_ids = [row[0] for row in conn.execute(select(self.table('branches').c.Branch_id)).fetchall()]
            customers = self.generate_customers(Config.NUM_CUSTOMERS)
            conn.execute(insert(self.table('customers')), customers)
            customer_ids = [row[0] for row in conn.execute(select(self.table('customers').c.Customer_id)).fetchall()]
            employees = self.generate_employees(Config.NUM_EMPLOYEES)
            conn.execute(insert(self.table('employees')), employees)
            employee_ids = [row[0] for row in conn.execute(select(self.table('employees').c.Employee_id)).fetchall()]
            atypes = [r[0] for r in conn.execute(select(self.table('account_type').c.Account_Type)).fetchall()]
            accounts = self.generate_accounts(Config.NUM_ACCOUNTS, branch_ids, atypes)
            conn.execute(insert(self.table('accounts')), accounts)
            account_ids = [row[0] for row in conn.execute(select(self.table('accounts').c.Account_id)).fetchall()]
            ac_rows = self.generate_account_customers(account_ids, customer_ids)
            if ac_rows:
                conn.execute(insert(self.table('account_customers')), ac_rows)
            customers_with_accounts = list({r['Customer_id'] for r in ac_rows})
            bt_rows = self.generate_banking_transactions(customers_with_accounts)
            if bt_rows:
                conn.execute(insert(self.table('banking_transactions')), bt_rows)
            cc_rows = self.generate_credit_cards(customer_ids)
            if cc_rows:
                conn.execute(insert(self.table('credit_cards')), cc_rows)
            cc_tx_rows = self.generate_cc_transactions(cc_rows)
            if cc_tx_rows:
                conn.execute(insert(self.table('cc_transactions')), cc_tx_rows)
            loan_rows = self.generate_loans(customer_ids)
            if loan_rows:
                conn.execute(insert(self.table('loan')), loan_rows)
            be_rows = self.generate_branch_employees(branch_ids, employee_ids)
            if be_rows:
                conn.execute(insert(self.table('branch_employees')), be_rows)
            self.enforce_business_rules(conn)

        return True
