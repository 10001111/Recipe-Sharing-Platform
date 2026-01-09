"""
Simplified SQL Execution Interface

Quick interface for executing SQL queries. This is the main entry point
for direct database operations.

Usage:
    from scripts.db_execute import execute_sql
    
    # Execute a query and get results
    results, count = execute_sql("SELECT * FROM users LIMIT 5;")
    
    # Execute without results (INSERT/UPDATE/DELETE)
    _, count = execute_sql("INSERT INTO users (username) VALUES ('test');", fetch_results=False)
"""

import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.execute_sql import execute_query


def execute_sql(sql, fetch_results=True, commit=True):
    """
    Execute SQL query on Supabase database.
    
    Args:
        sql: SQL query string
        fetch_results: If True, return results (for SELECT queries)
        commit: If True, commit transaction
    
    Returns:
        Tuple of (results, rowcount)
        - results: List of dicts for SELECT queries, None otherwise
        - rowcount: Number of affected/returned rows
    """
    return execute_query(sql, fetch_results=fetch_results, commit=commit)


if __name__ == '__main__':
    # Allow direct execution
    if len(sys.argv) < 2:
        print("Usage: python scripts/db_execute.py 'SQL QUERY'")
        sys.exit(1)
    
    sql = sys.argv[1]
    results, count = execute_sql(sql)
    
    if results:
        print(f"\nReturned {count} row(s):")
        for i, row in enumerate(results, 1):
            print(f"\nRow {i}:")
            for key, value in row.items():
                print(f"  {key}: {value}")

