"""
Data export module for JSON and CSV formats.
Exports all tables from the database to ./exports/ directory.
"""
import csv
import json
import os
from pathlib import Path
from typing import List, Dict

from sqlalchemy import select
from sqlalchemy.engine import Engine

from schema_reflector import SchemaReflector


class DataExporter:
    def __init__(self, reflector: SchemaReflector, export_dir: str = "./exports"):
        self.reflector = reflector
        self.engine: Engine = reflector.engine
        self.metadata = reflector.metadata
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)

    def export_table_to_json(self, table_name: str) -> str:
        """Export a single table to JSON format."""
        table = self.metadata.tables[table_name]
        with self.engine.connect() as conn:
            result = conn.execute(select(table))
            rows = result.fetchall()
            columns = result.keys()
            
            data = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    if hasattr(value, 'isoformat'):
                        value = value.isoformat()
                    elif isinstance(value, (bytes, bytearray)):
                        value = value.decode('utf-8', errors='ignore')
                    else:
                        value = str(value) if value is not None else None
                    row_dict[col] = value
                data.append(row_dict)
        
        output_path = self.export_dir / f"{table_name}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)

    def export_table_to_csv(self, table_name: str) -> str:
        """Export a single table to CSV format."""
        table = self.metadata.tables[table_name]
        with self.engine.connect() as conn:
            result = conn.execute(select(table))
            rows = result.fetchall()
            columns = result.keys()
            
            output_path = self.export_dir / f"{table_name}.csv"
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                
                for row in rows:
                    processed_row = []
                    for value in row:
                        if hasattr(value, 'isoformat'):
                            processed_row.append(value.isoformat())
                        elif isinstance(value, (bytes, bytearray)):
                            processed_row.append(value.decode('utf-8', errors='ignore'))
                        else:
                            processed_row.append(str(value) if value is not None else '')
                    writer.writerow(processed_row)
        
        return str(output_path)

    def export_all_tables(self) -> Dict[str, Dict[str, str]]:
        """Export all tables to both JSON and CSV formats."""
        tables = self.reflector.get_all_tables()
        results = {}
        
        for table_name in tables:
            print(f"Exporting {table_name}...")
            json_path = self.export_table_to_json(table_name)
            csv_path = self.export_table_to_csv(table_name)
            results[table_name] = {
                'json': json_path,
                'csv': csv_path
            }
        
        return results

    def get_export_summary(self) -> Dict[str, int]:
        """Get summary of exported data."""
        summary = {}
        tables = self.reflector.get_all_tables()
        
        with self.engine.connect() as conn:
            for table_name in tables:
                table = self.metadata.tables[table_name]
                count = conn.execute(select(table)).rowcount
                if count == -1:
                    from sqlalchemy import func
                    count = conn.execute(select(func.count()).select_from(table)).scalar()
                summary[table_name] = count
        
        return summary
