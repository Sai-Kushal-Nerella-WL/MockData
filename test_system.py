#!/usr/bin/env python3
"""
Test script to verify the system components work correctly.
This tests the modules without requiring a live MySQL connection.
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import config
        print("  ✓ config")
        import utils
        print("  ✓ utils")
        import schema_reflector
        print("  ✓ schema_reflector")
        import data_generator
        print("  ✓ data_generator")
        import data_validator
        print("  ✓ data_validator")
        import data_exporter
        print("  ✓ data_exporter")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    try:
        from config import Config
        print(f"  ✓ DB_HOST: {Config.DB_HOST}")
        print(f"  ✓ DB_NAME: {Config.DB_NAME}")
        print(f"  ✓ RANDOM_SEED: {Config.RANDOM_SEED}")
        print(f"  ✓ NUM_CUSTOMERS: {Config.NUM_CUSTOMERS}")
        url = Config.get_database_url()
        print(f"  ✓ Database URL generated (credentials hidden)")
        return True
    except Exception as e:
        print(f"  ❌ Config error: {e}")
        return False

def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    try:
        from utils import get_faker, ensure_max_length, random_sex, random_cc_number
        
        fake = get_faker(42)
        print(f"  ✓ Faker initialized with seed 42")
        
        name = fake.name()
        print(f"  ✓ Generated name: {name}")
        
        truncated = ensure_max_length("Hello World", 5)
        assert truncated == "Hello", f"Expected 'Hello', got '{truncated}'"
        print(f"  ✓ String truncation works")
        
        sex = random_sex()
        assert sex in ["M", "F"], f"Expected M or F, got {sex}"
        print(f"  ✓ Random sex generation: {sex}")
        
        cc = random_cc_number()
        assert len(cc) == 16, f"Expected 16 digits, got {len(cc)}"
        assert cc.isdigit(), f"Expected digits only, got {cc}"
        print(f"  ✓ Credit card number generation: {cc[:4]}...")
        
        return True
    except Exception as e:
        print(f"  ❌ Utils error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    required_files = [
        'main.py',
        'config.py',
        'schema_reflector.py',
        'data_generator.py',
        'data_validator.py',
        'data_exporter.py',
        'utils.py',
        'requirements.txt',
        '.env.example',
        'Sql_code.txt',
        'SETUP.md',
        'PROJECT_README.md'
    ]
    
    all_exist = True
    for filename in required_files:
        path = Path(filename)
        if path.exists():
            print(f"  ✓ {filename}")
        else:
            print(f"  ❌ {filename} not found")
            all_exist = False
    
    return all_exist

def test_sql_schema():
    """Test that SQL schema file is valid."""
    print("\nTesting SQL schema file...")
    try:
        with open('Sql_code.txt', 'r') as f:
            content = f.read()
        
        required_tables = [
            'customers', 'account_type', 'branches', 'employees',
            'accounts', 'account_customers', 'banking_transactions',
            'credit_cards', 'cc_transactions', 'loan', 'branch_employees'
        ]
        
        all_found = True
        for table in required_tables:
            if f"CREATE TABLE {table}" in content:
                print(f"  ✓ Table definition found: {table}")
            else:
                print(f"  ❌ Table definition missing: {table}")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"  ❌ SQL schema error: {e}")
        return False

def main():
    print("=" * 80)
    print("  System Component Tests")
    print("=" * 80)
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Utilities", test_utils),
        ("SQL Schema", test_sql_schema),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    print("\n" + "=" * 80)
    print("  Test Summary")
    print("=" * 80)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print()
    print(f"  Total: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Set up your MySQL database: mysql -u root -p < Sql_code.txt")
        print("  2. Configure .env with your database credentials")
        print("  3. Run the system: python main.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
