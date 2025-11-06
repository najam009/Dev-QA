import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to watch (change this to your local folder path)
FOLDER_TO_WATCH = "/home/najam/S3bucket/"  # for Windows
# FOLDER_TO_WATCH = "/home/najam/watched_folder"  # for WSL/Linux

class FolderWatcher(FileSystemEventHandler):
    def on_created(self, event):
        print(f"📁 File created: {event.src_path}")

    def on_deleted(self, event):
        print(f"🗑️ File deleted: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ File modified: {event.src_path}")

if __name__ == "__main__":
    print(f"👀 Watching folder: {FOLDER_TO_WATCH}")
    event_handler = FolderWatcher()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
