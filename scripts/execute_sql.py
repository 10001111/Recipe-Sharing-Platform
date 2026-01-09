"""
Direct SQL Execution Utility for Supabase Database

This script provides direct access to execute any SQL query on the Supabase database.
It can be used to:
- Create/alter/drop tables
- Create/update/delete functions
- Insert/update/delete data
- Run any PostgreSQL query

Usage:
    python scripts/execute_sql.py "SELECT * FROM users;"
    python scripts/execute_sql.py --file path/to/query.sql
    python scripts/execute_sql.py --interactive
"""

import os
import sys
import argparse
from pathlib import Path
from decouple import config
import psycopg2
from psycopg2.extras import RealDictCursor
import json

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


def get_db_connection():
    """Get database connection using credentials from .env"""
    try:
        db_name = config('DB_NAME', default=None)
        if not db_name:
            raise ValueError("DB_NAME not set in .env file")
        
        conn = psycopg2.connect(
            dbname=db_name,
            user=config('DB_USER', default='postgres'),
            password=config('DB_PASSWORD', default=''),
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default='5432'),
            connect_timeout=10
        )
        return conn
    except Exception as e:
        print(f"[ERROR] Error connecting to database: {e}")
        print("\n[TIP] Make sure your .env file has correct database credentials:")
        print("   - DB_NAME")
        print("   - DB_USER")
        print("   - DB_PASSWORD")
        print("   - DB_HOST")
        print("   - DB_PORT")
        sys.exit(1)


def execute_query(sql, fetch_results=True, commit=True):
    """
    Execute a SQL query and return results.
    
    Args:
        sql: SQL query string
        fetch_results: If True, fetch and return results (for SELECT queries)
        commit: If True, commit the transaction (for INSERT/UPDATE/DELETE)
    
    Returns:
        Tuple of (results, rowcount)
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("Executing SQL query...")
        cursor.execute(sql)
        
        if fetch_results and cursor.description:
            # SELECT query - fetch results
            results = cursor.fetchall()
            rowcount = len(results)
            print(f"[OK] Query executed successfully. Returned {rowcount} row(s).")
            return results, rowcount
        else:
            # INSERT/UPDATE/DELETE/CREATE/etc - no results to fetch
            rowcount = cursor.rowcount
            if commit:
                conn.commit()
                print(f"[OK] Query executed successfully. Affected {rowcount} row(s).")
            return None, rowcount
            
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Database error: {e}")
        print(f"\nQuery that failed:")
        print(f"{sql}")
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[ERROR] Unexpected error: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()


def format_results(results):
    """Format query results for display"""
    if not results:
        return "No results."
    
    if len(results) == 0:
        return "Query returned 0 rows."
    
    # Convert to list of dicts for JSON serialization
    formatted = []
    for row in results:
        formatted.append(dict(row))
    
    return formatted


def main():
    parser = argparse.ArgumentParser(
        description='Execute SQL queries directly on Supabase database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute a SELECT query
  python scripts/execute_sql.py "SELECT * FROM users LIMIT 5;"
  
  # Execute a CREATE TABLE query
  python scripts/execute_sql.py "CREATE TABLE test (id SERIAL PRIMARY KEY, name VARCHAR(100));"
  
  # Execute SQL from a file
  python scripts/execute_sql.py --file queries/create_tables.sql
  
  # Interactive mode (coming soon)
  python scripts/execute_sql.py --interactive
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='SQL query to execute'
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Path to SQL file to execute'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Interactive mode (enter queries one by one)'
    )
    parser.add_argument(
        '--no-commit',
        action='store_true',
        help='Do not commit transaction (for testing)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress non-error output'
    )
    
    args = parser.parse_args()
    
    # Determine SQL source
    sql = None
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[ERROR] File not found: {file_path}")
            sys.exit(1)
        sql = file_path.read_text()
    elif args.query:
        sql = args.query
    elif args.interactive:
        print("[INFO] Interactive mode")
        print("Enter SQL queries (type 'exit' or 'quit' to exit)")
        print("=" * 70)
        
        while True:
            try:
                query = input("\nSQL> ").strip()
                if query.lower() in ('exit', 'quit', 'q'):
                    break
                if not query:
                    continue
                
                results, rowcount = execute_query(
                    query,
                    fetch_results=True,
                    commit=not args.no_commit
                )
                
                if results is not None:
                    if args.json:
                        print(json.dumps(format_results(results), indent=2, default=str))
                    else:
                        formatted = format_results(results)
                        if isinstance(formatted, list) and len(formatted) > 0:
                            print("\nResults:")
                            for i, row in enumerate(formatted, 1):
                                print(f"\nRow {i}:")
                                for key, value in row.items():
                                    print(f"  {key}: {value}")
                        else:
                            print("No results returned.")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
        
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Execute the query
    try:
        results, rowcount = execute_query(
            sql,
            fetch_results=True,
            commit=not args.no_commit
        )
        
        # Output results
        if results is not None:
            if args.json:
                formatted = format_results(results)
                print(json.dumps(formatted, indent=2, default=str))
            else:
                formatted = format_results(results)
                if isinstance(formatted, list) and len(formatted) > 0:
                    print("\n" + "=" * 70)
                    print("RESULTS")
                    print("=" * 70)
                    for i, row in enumerate(formatted, 1):
                        print(f"\nRow {i}:")
                        for key, value in row.items():
                            print(f"  {key}: {value}")
                    print("\n" + "=" * 70)
                else:
                    print("Query returned no results.")
        
        sys.exit(0)
        
    except Exception as e:
        if not args.quiet:
            print(f"\n[ERROR] Failed to execute query: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

