import subprocess
import os

def run_trigger():
    print("Trigger script called — staging data now...")

    # Absolute path to the staging script
    STAGING_SCRIPT = 'src/app/pipeline/stage_raw_data.py'

    try:
        # Call the staging script
        subprocess.run(["python", STAGING_SCRIPT], check=True)
        print("Staging process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running staging script: {e}")

if __name__ == "__main__":
    run_trigger()
