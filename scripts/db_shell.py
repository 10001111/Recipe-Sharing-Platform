"""
Interactive Database Shell

Provides an interactive Python shell with direct database access.

Usage:
    python scripts/db_shell.py
    
Then you can use:
    execute_sql("SELECT * FROM users;")
    execute_sql("CREATE TABLE test (id SERIAL PRIMARY KEY);")
"""

import os
import sys
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django environment (optional, for Django ORM access)
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()
    from django.db import connection
    django_available = True
except Exception:
    django_available = False

from scripts.execute_sql import execute_query, get_db_connection


def execute_sql(sql, fetch_results=True, commit=True):
    """
    Execute SQL query and return results.
    
    Args:
        sql: SQL query string
        fetch_results: If True, return results
        commit: If True, commit transaction
    
    Returns:
        Tuple of (results, rowcount)
    """
    return execute_query(sql, fetch_results=fetch_results, commit=commit)


def show_tables():
    """Show all tables in the database"""
    sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    results, _ = execute_sql(sql)
    if results:
        print("\nTables in database:")
        for row in results:
            print(f"  - {row['table_name']}")
    else:
        print("No tables found.")


def show_schemas():
    """Show all schemas"""
    sql = "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name;"
    results, _ = execute_sql(sql)
    if results:
        print("\nSchemas:")
        for row in results:
            print(f"  - {row['schema_name']}")
    else:
        print("No schemas found.")


def describe_table(table_name):
    """Describe a table structure"""
    sql = f"""
    SELECT 
        column_name,
        data_type,
        character_maximum_length,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name = '{table_name}'
    ORDER BY ordinal_position;
    """
    results, _ = execute_sql(sql)
    if results:
        print(f"\nTable: {table_name}")
        print("-" * 70)
        for row in results:
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {row['column_default']}" if row['column_default'] else ""
            length = f"({row['character_maximum_length']})" if row['character_maximum_length'] else ""
            print(f"  {row['column_name']:<30} {row['data_type']}{length:<20} {nullable}{default}")
    else:
        print(f"Table '{table_name}' not found.")


# Make functions available in shell
__all__ = ['execute_sql', 'show_tables', 'show_schemas', 'describe_table', 'get_db_connection']

if django_available:
    __all__.extend(['connection'])

if __name__ == '__main__':
    print("=" * 70)
    print("Supabase Database Shell")
    print("=" * 70)
    print("\nAvailable functions:")
    print("  execute_sql(sql, fetch_results=True, commit=True) - Execute SQL query")
    print("  show_tables() - List all tables")
    print("  show_schemas() - List all schemas")
    print("  describe_table(table_name) - Show table structure")
    print("  get_db_connection() - Get raw database connection")
    if django_available:
        print("  connection - Django database connection")
    print("\nExample:")
    print("  results, count = execute_sql('SELECT * FROM users LIMIT 5;')")
    print("  show_tables()")
    print("  describe_table('users')")
    print("\n" + "=" * 70)
    print("Starting interactive shell...")
    print("=" * 70 + "\n")
    
    # Start IPython if available, otherwise use standard Python shell
    try:
        from IPython import embed
        embed(using=False)
    except ImportError:
        import code
        code.interact(local=dict(globals(), **locals()))

