#!/usr/bin/env python3
"""
Main script for data generation and validation system.
Orchestrates schema reflection, data generation, validation, and export.
"""
import sys
import time
from pathlib import Path

from config import Config
from schema_reflector import SchemaReflector
from data_generator import DataGenerator
from data_validator import DataValidator
from data_exporter import DataExporter


def print_banner():
    print("=" * 80)
    print("  MySQL Mock Data Generation and Validation System")
    print("=" * 80)
    print()


def main():
    print_banner()
    
    print(f"Configuration:")
    print(f"  Database: {Config.DB_NAME}")
    print(f"  Host: {Config.DB_HOST}:{Config.DB_PORT}")
    print(f"  Random Seed: {Config.RANDOM_SEED}")
    print(f"  Customers: {Config.NUM_CUSTOMERS}")
    print(f"  Employees: {Config.NUM_EMPLOYEES}")
    print(f"  Branches: {Config.NUM_BRANCHES}")
    print(f"  Accounts: {Config.NUM_ACCOUNTS}")
    print()
    
    try:
        print("Step 1: Connecting to database and reflecting schema...")
        reflector = SchemaReflector()
        reflector.reflect_schema()
        tables = reflector.get_all_tables()
        print(f"  ✓ Found {len(tables)} tables: {', '.join(tables)}")
        
        dependencies = reflector.get_table_dependencies()
        print(f"  ✓ Determined insertion order: {' -> '.join(dependencies)}")
        print()
        
        print("Step 2: Generating mock data...")
        start_time = time.time()
        generator = DataGenerator(seed=Config.RANDOM_SEED)
        
        print("  - Truncating existing data...")
        generator.truncate_all()
        
        print("  - Generating and inserting data...")
        generator.generate_and_insert_all()
        
        elapsed = time.time() - start_time
        print(f"  ✓ Data generation completed in {elapsed:.2f} seconds")
        print()
        
        print("Step 3: Validating data quality...")
        validator = DataValidator(reflector)
        results = validator.validate_all()
        
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed)
        print(f"  ✓ Validation completed: {passed} passed, {failed} failed")
        
        if failed > 0:
            print("\n  Failed validations:")
            for result in results:
                if not result.passed:
                    print(f"    ❌ {result.category} - {result.rule}")
                    print(f"       {result.details}")
        print()
        
        print("Step 4: Generating validation report...")
        report = validator.generate_report()
        report_path = Path("validation_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  ✓ Validation report saved to: {report_path}")
        print()
        
        print("Step 5: Exporting data to JSON and CSV...")
        exporter = DataExporter(reflector)
        export_results = exporter.export_all_tables()
        
        print(f"  ✓ Exported {len(export_results)} tables to ./exports/")
        for table_name, paths in export_results.items():
            print(f"    - {table_name}: {Path(paths['json']).name}, {Path(paths['csv']).name}")
        print()
        
        print("Step 6: Summary...")
        summary = exporter.get_export_summary()
        total_records = sum(summary.values())
        print(f"  Total records generated: {total_records}")
        for table_name, count in summary.items():
            print(f"    - {table_name}: {count} records")
        print()
        
        print("=" * 80)
        print("  ✓ All operations completed successfully!")
        print("=" * 80)
        print()
        print("Output files:")
        print(f"  - Validation report: validation_report.md")
        print(f"  - Exported data: ./exports/*.json and ./exports/*.csv")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
