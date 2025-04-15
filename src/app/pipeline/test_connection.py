import snowflake.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
ACCOUNT = os.getenv("ACCOUNT")
WAREHOUSE = os.getenv("WAREHOUSE")

# Read the table DDL from file
with open("test_table.sql", "r") as f:
    table_ddl = f.read()

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE
)

cur = conn.cursor()

try:
    # Create database
    cur.execute("CREATE DATABASE IF NOT EXISTS test_db")

    # Create schema
    cur.execute("CREATE SCHEMA IF NOT EXISTS test_db.test_schema")

    # Create table using the loaded DDL
    cur.execute(table_ddl)

    print("Database, schema, and table created successfully.")

finally:
    cur.close()
    conn.close()
