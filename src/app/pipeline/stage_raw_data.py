import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    account=os.getenv("ACCOUNT"),
    warehouse=os.getenv("WAREHOUSE"),
    database=os.getenv("DATABASE"),
    schema="RAW"
)
cur = conn.cursor()

# Define stage and data directory
stage_name = 'STAGE_RAW_DATA'
data_dir = os.path.join(os.getcwd(), 'source_data')

# Track if all uploads were successful
all_successful = True

# Upload each CSV file in the data directory
for file_name in os.listdir(data_dir):
    if file_name in [
        'advertiser_fee.csv',
        'lumina_plan_information3.csv',
        'vod_platform4.csv'
    ]:
        file_path = os.path.join(data_dir, file_name)
        print(f"Uploading {file_name} to @{stage_name}...")

        # Execute PUT command
        cur.execute(f"PUT file://{file_path} @{stage_name} AUTO_COMPRESS=TRUE, OVERWRITE=TRUE")

        # Fetch result — typically a single row per file
        result = cur.fetchall()

        for row in result:
            status = row[6]  # Status column (7th field)
            if status != 'UPLOADED':
                print(f"Failed to upload {file_name}. Status: {status}")
                all_successful = False
            else:
                print(f"Successfully uploaded {file_name}.")

# If everything uploaded successfully, trigger the data load procedure
if all_successful:
    print("All files uploaded successfully — running staging master task...")
    cur.execute("EXECUTE TASK ASSESSMENT.RAW.MASTER_RAW_PIPELINE_TASK;")
    print("Data load and deduplication procedures completed.")

else:
    print("One or more files failed to upload. Skipping data load procedure.")

cur.close()
conn.close()
