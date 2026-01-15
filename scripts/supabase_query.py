"""
Simple Supabase SQL Query Utility

Quick utility to execute SQL queries directly on Supabase database.
Uses psycopg2 for direct PostgreSQL connection.

Usage:
    python scripts/supabase_query.py "SELECT * FROM users_customuser;"
    python scripts/supabase_query.py "SELECT COUNT(*) FROM recipes_recipe;"
"""

import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.execute_sql import execute_query
import json


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/supabase_query.py 'SQL QUERY'")
        print("\nExamples:")
        print("  python scripts/supabase_query.py \"SELECT * FROM users_customuser LIMIT 5;\"")
        print("  python scripts/supabase_query.py \"SELECT COUNT(*) FROM recipes_recipe;\"")
        sys.exit(1)
    
    sql = sys.argv[1]
    
    try:
        results, count = execute_query(sql, fetch_results=True, commit=True)
        
        if results:
            print(f"\n[OK] Query executed successfully. Returned {count} row(s).\n")
            
            # Print results in a table format
            if isinstance(results[0], dict):
                # Get headers
                headers = list(results[0].keys())
                
                # Calculate column widths
                col_widths = {}
                for header in headers:
                    col_widths[header] = max(
                        len(str(header)),
                        max((len(str(row.get(header, ''))) for row in results), default=0)
                    )
                
                # Print header
                header_row = " | ".join(f"{h:<{col_widths[h]}}" for h in headers)
                print(header_row)
                print("-" * len(header_row))
                
                # Print rows
                for row in results:
                    row_str = " | ".join(f"{str(row.get(h, '')):<{col_widths[h]}}" for h in headers)
                    print(row_str)
            else:
                for i, row in enumerate(results, 1):
                    print(f"Row {i}: {row}")
        else:
            print(f"\n[OK] Query executed successfully. Affected {count} row(s).")
            
    except Exception as e:
        print(f"\n[ERROR] Query failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

