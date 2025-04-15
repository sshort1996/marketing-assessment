import snowflake.connector
from dotenv import load_dotenv
import os
import glob

# Load environment variables
load_dotenv()

def get_connection():
    """Create and return a Snowflake connection."""
    return snowflake.connector.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        account=os.getenv("ACCOUNT"),
        warehouse=os.getenv("WAREHOUSE")
    )

def create_objects(obj_dir="src/app/pipeline/obj", recreate_objs=None):
    """Create database, schema, and tables in Snowflake based on SQL files."""
    conn = get_connection()
    cur = conn.cursor()

    database = os.getenv("DATABASE")
    schema = "RAW"

    try:
        # Create database and schema
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {database}.{schema}")

        # Find all .sql files in the directory
        all_objs = glob.glob(os.path.join(obj_dir, "*.sql"))
        all_obj_names = [os.path.basename(obj) for obj in all_objs]

        # Determine which objects to create
        objs_to_create = recreate_objs if recreate_objs else all_obj_names

        for obj_file in objs_to_create:
            file_path = os.path.join(obj_dir, obj_file)
            if not os.path.isfile(file_path):
                print(f"File not found: {file_path}")
                continue

            with open(file_path, 'r') as f:
                ddl = f.read()

            print(f"Creating object from: {obj_file}")
            cur.execute(f"USE DATABASE {database}")
            cur.execute(f"USE SCHEMA {schema}")
            cur.execute(ddl)
        
        print("Objects created successfully.")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Run with default — create everything in 'obj'
    create_objects()
    # Example to only recreate one or two specific tables:
    # create_objects(recreate_objs=["RAW_ADVERTISER_FEE.sql", "RAW_VOD_PLATFORM.sql"])
