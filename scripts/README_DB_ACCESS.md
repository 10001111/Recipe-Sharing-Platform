# Direct Supabase Database Access

This directory contains utilities for direct SQL execution on your Supabase database.

## 🚀 Quick Start

### Method 1: Command Line (Windows Batch Files)

```batch
# Execute a single SQL query
bats\db_execute_sql.bat "SELECT * FROM users LIMIT 5;"

# Execute SQL from a file
bats\db_execute_file.bat queries\my_query.sql

# Start interactive shell
bats\db_shell.bat
```

### Method 2: Python Scripts

```bash
# Execute a single query
python scripts/execute_sql.py "SELECT * FROM users LIMIT 5;"

# Execute from file
python scripts/execute_sql.py --file queries/my_query.sql

# Interactive mode
python scripts/execute_sql.py --interactive

# JSON output
python scripts/execute_sql.py "SELECT * FROM users;" --json
```

### Method 3: Python API (in your code)

```python
from scripts.db_execute import execute_sql

# Execute SELECT query
results, count = execute_sql("SELECT * FROM users LIMIT 5;")
for row in results:
    print(row['username'])

# Execute INSERT/UPDATE/DELETE
_, count = execute_sql("INSERT INTO users (username) VALUES ('test');")

# Execute CREATE TABLE
execute_sql("""
    CREATE TABLE recipes (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
""")
```

## 📋 Available Scripts

### `execute_sql.py`
Main SQL execution utility with full feature set.

**Features:**
- Execute any SQL query
- Support for SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, etc.
- Execute SQL from files
- Interactive mode
- JSON output option
- Transaction control

**Usage:**
```bash
python scripts/execute_sql.py "YOUR SQL QUERY"
python scripts/execute_sql.py --file path/to/query.sql
python scripts/execute_sql.py --interactive
python scripts/execute_sql.py "SELECT * FROM users;" --json
```

### `db_execute.py`
Simplified interface for programmatic use.

**Usage:**
```python
from scripts.db_execute import execute_sql

results, count = execute_sql("SELECT * FROM users;")
```

### `db_shell.py`
Interactive Python shell with database access.

**Features:**
- Interactive Python shell
- Pre-loaded helper functions
- Access to Django ORM (if available)

**Usage:**
```bash
python scripts/db_shell.py
```

**Available functions in shell:**
- `execute_sql(sql)` - Execute SQL query
- `show_tables()` - List all tables
- `show_schemas()` - List all schemas
- `describe_table(table_name)` - Show table structure
- `get_db_connection()` - Get raw database connection

## 🔧 Supabase CLI Access

Supabase CLI is available via `npx`. You can use it for:

```bash
# Execute SQL via Supabase CLI (if linked)
npx supabase db execute "SELECT * FROM users;"

# Link to remote project
npx supabase link --project-ref YOUR_PROJECT_REF

# Pull schema from remote
npx supabase db pull

# Push migrations to remote
npx supabase db push
```

## 📝 Examples

### Create a Table
```sql
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Create a Function
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';
```

### Create a Trigger
```sql
CREATE TRIGGER update_recipes_updated_at 
BEFORE UPDATE ON recipes
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
```

### Insert Data
```sql
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com');
```

### Update Data
```sql
UPDATE users 
SET email = 'newemail@example.com' 
WHERE username = 'john_doe';
```

### Delete Data
```sql
DELETE FROM users WHERE id = 1;
```

### Query with Joins
```sql
SELECT 
    r.id,
    r.title,
    u.username as author
FROM recipes r
JOIN users u ON r.author_id = u.id
ORDER BY r.created_at DESC;
```

## 🔒 Security Notes

- All scripts read credentials from `.env` file
- Never commit `.env` file to git
- Use parameterized queries when possible (for user input)
- Be careful with DROP and DELETE operations
- Test queries in development before running in production

## 🐛 Troubleshooting

### Connection Errors

If you get connection errors:

1. **Check .env file** - Make sure all database credentials are set:
   ```
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=db.your-project.supabase.co
   DB_PORT=5432
   ```

2. **Check Supabase project status** - Make sure your project is not paused

3. **Test connection**:
   ```bash
   python scripts/test_database_connection.py
   ```

### Permission Errors

- Make sure you're using the correct database user
- Check that your Supabase project allows connections from your IP
- Verify database password is correct

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

