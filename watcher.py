# watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class CreatedHandler(FileSystemEventHandler):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            # short wait so file writes (esp. large files) finish
            time.sleep(0.25)
            try:
                self.callback(event.src_path)
            except Exception as e:
                print("Error in callback for", event.src_path, ":", e)

def start_watcher(path_to_watch, callback):
    handler = CreatedHandler(callback)
    observer = Observer()
    observer.schedule(handler, path_to_watch, recursive=True)
    observer.start()
    print(f"[Watcher] Watching folder: {path_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[Watcher] Stopping...")
        observer.stop()
    observer.join()
