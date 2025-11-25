import subprocess
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartOnChange(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_bot()

    def start_bot(self):
        print("[dev] Starting bot...")
        self.process = subprocess.Popen(["python", "discord_interface.py"])

    def stop_bot(self):
        if self.process:
            print("[dev] Stopping bot...")
            self.process.terminate()
            self.process.wait()

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"[dev] Detected change in {event.src_path}. Reloading bot...")
            self.stop_bot()
            self.start_bot()

if __name__ == "__main__":
    path = "."
    event_handler = RestartOnChange()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[dev] Exiting...")
        event_handler.stop_bot()
        observer.stop()
        observer.join()
