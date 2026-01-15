"""
Supabase SQL Execution Utility

Execute SQL queries directly using Supabase Python client.
This uses the Supabase REST API with service role key for direct SQL execution.

Usage:
    python scripts/supabase_sql.py "SELECT * FROM users;"
    python scripts/supabase_sql.py --file path/to/query.sql
    python scripts/supabase_sql.py --interactive
"""

import sys
import os
import argparse
from pathlib import Path
from decouple import config

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django (for accessing settings)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.conf import settings
from supabase import create_client, Client
import json


def get_supabase_client() -> Client:
    """Create and return Supabase client with service role key"""
    supabase_url = getattr(settings, 'SUPABASE_URL', '')
    supabase_service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
    
    if not supabase_url:
        raise ValueError("SUPABASE_URL not set in .env file")
    
    if not supabase_service_key:
        raise ValueError("SUPABASE_SERVICE_ROLE_KEY not set in .env file")
    
    return create_client(supabase_url, supabase_service_key)


def execute_sql_query(client: Client, sql: str) -> dict:
    """
    Execute SQL query using Supabase client
    
    Args:
        client: Supabase client instance
        sql: SQL query string
        
    Returns:
        dict with results or error information
    """
    try:
        # Use RPC (Remote Procedure Call) to execute SQL
        # Note: Supabase doesn't have a direct SQL execution endpoint in the Python client
        # We'll use the PostgREST API directly via httpx
        
        import httpx
        
        supabase_url = getattr(settings, 'SUPABASE_URL', '')
        supabase_service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        
        # Use PostgREST REST API for SQL execution
        # This requires using the REST API endpoint directly
        response = httpx.post(
            f"{supabase_url}/rest/v1/rpc/exec_sql",
            headers={
                "apikey": supabase_service_key,
                "Authorization": f"Bearer {supabase_service_key}",
                "Content-Type": "application/json",
            },
            json={"query": sql},
            timeout=30.0
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json(),
                "status_code": response.status_code
            }
        else:
            return {
                "success": False,
                "error": response.text,
                "status_code": response.status_code
            }
            
    except Exception as e:
        # Fallback: Try using psycopg2 for direct database connection
        try:
            from scripts.execute_sql import execute_query
            results, count = execute_query(sql, fetch_results=True, commit=True)
            return {
                "success": True,
                "data": results,
                "count": count,
                "method": "psycopg2"
            }
        except Exception as pg_error:
            return {
                "success": False,
                "error": f"Supabase API error: {str(e)}\nPostgreSQL error: {str(pg_error)}",
                "method": "both_failed"
            }


def execute_sql_direct(sql: str) -> dict:
    """
    Execute SQL using direct PostgreSQL connection (psycopg2)
    This is more reliable for direct SQL execution
    
    Args:
        sql: SQL query string
        
    Returns:
        dict with results or error information
    """
    try:
        from scripts.execute_sql import execute_query
        results, count = execute_query(sql, fetch_results=True, commit=True)
        return {
            "success": True,
            "data": results,
            "count": count,
            "method": "psycopg2"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "method": "psycopg2"
        }


def format_results(results: dict):
    """Format and print query results"""
    if not results["success"]:
        print(f"\n[ERROR] Query failed:")
        print(f"  {results.get('error', 'Unknown error')}")
        return
    
    data = results.get("data", [])
    count = results.get("count", len(data) if isinstance(data, list) else 0)
    method = results.get("method", "unknown")
    
    print(f"\n[SUCCESS] Query executed successfully (using {method})")
    print(f"Rows returned: {count}")
    
    if isinstance(data, list) and len(data) > 0:
        print("\nResults:")
        print("=" * 70)
        
        # Print header
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            print(" | ".join(f"{h:20}" for h in headers))
            print("-" * 70)
            
            # Print rows
            for i, row in enumerate(data[:100], 1):  # Limit to 100 rows
                values = [str(row.get(h, ''))[:20] for h in headers]
                print(" | ".join(f"{v:20}" for v in values))
            
            if len(data) > 100:
                print(f"\n... ({len(data) - 100} more rows)")
        else:
            for i, row in enumerate(data[:100], 1):
                print(f"Row {i}: {row}")
    elif count == 0:
        print("\n(No rows returned)")


def interactive_mode():
    """Run in interactive mode"""
    print("=" * 70)
    print("Supabase SQL Interactive Mode")
    print("=" * 70)
    print("Enter SQL queries (type 'exit' or 'quit' to exit)")
    print("Type 'help' for examples")
    print("=" * 70)
    
    while True:
        try:
            sql = input("\nSQL> ").strip()
            
            if not sql:
                continue
            
            if sql.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if sql.lower() == 'help':
                print("\nExample queries:")
                print("  SELECT * FROM users LIMIT 5;")
                print("  SELECT COUNT(*) FROM recipes;")
                print("  SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
                continue
            
            # Execute query
            result = execute_sql_direct(sql)
            format_results(result)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n[ERROR] {str(e)}")


def main():
    parser = argparse.ArgumentParser(
        description='Execute SQL queries on Supabase database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/supabase_sql.py "SELECT * FROM users LIMIT 5;"
  python scripts/supabase_sql.py --file queries.sql
  python scripts/supabase_sql.py --interactive
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
        help='Execute SQL from file'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.file:
        # Read SQL from file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[ERROR] File not found: {args.file}")
            sys.exit(1)
        
        sql = file_path.read_text()
        print(f"Executing SQL from {args.file}...")
        result = execute_sql_direct(sql)
        format_results(result)
    elif args.query:
        # Execute single query
        result = execute_sql_direct(args.query)
        format_results(result)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

