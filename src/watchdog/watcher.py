import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../source_data'))
TRIGGER_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'trigger.py'))
ALLOWED_EXTENSIONS = ['.csv', '.txt']

# ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

class FileCreateHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.processed_files = set()

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        _, ext = os.path.splitext(file_path)

        if ext.lower() not in ALLOWED_EXTENSIONS:
            print(f"{YELLOW}Ignored file: {file_path} (unsupported extension){RESET}", flush=True)
            return

        if file_path in self.processed_files:
            # Already processed this file
            return

        self.processed_files.add(file_path)

        print(f"{GREEN}New file detected: {file_path}, triggering pipeline...{RESET}", flush=True)
        try:
            subprocess.run(["python", TRIGGER_SCRIPT], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}Error running trigger script: {e}{RESET}", flush=True)

def start_watcher():
    print(f"{CYAN}[WATCHING] Directory: {SOURCE_DIR}{RESET}", flush=True)
    event_handler = FileCreateHandler()
    observer = Observer()
    observer.schedule(event_handler, SOURCE_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watcher()
