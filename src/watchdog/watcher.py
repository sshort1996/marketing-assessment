import time
import os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SOURCE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../source_data'))
TRIGGER_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'trigger.py'))
ALLOWED_EXTENSIONS = ['.csv', '.txt']

DEBOUNCE_SECONDS = 1.0

# ANSI color codes
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.recent_events = {}

    def handle_event(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        _, ext = os.path.splitext(file_path)
        now = time.time()
        last_time = self.recent_events.get(file_path, 0)

        if now - last_time < DEBOUNCE_SECONDS:
            return

        self.recent_events[file_path] = now

        if ext.lower() not in ALLOWED_EXTENSIONS:
            print(f"{YELLOW}Ignored file: {file_path} (unsupported extension){RESET}", flush=True)
            return

        print(f"{GREEN}Detected change: {file_path}, triggering pipeline...{RESET}", flush=True)
        try:
            subprocess.run(["python", TRIGGER_SCRIPT], check=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}Error running trigger script: {e}{RESET}", flush=True)

    def on_created(self, event):
        self.handle_event(event)

    def on_modified(self, event):
        self.handle_event(event)

def start_watcher():
    print(f"{CYAN}[WATCHING] Directory: {SOURCE_DIR}{RESET}", flush=True)
    event_handler = FileChangeHandler()
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
