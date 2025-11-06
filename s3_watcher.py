import os
import time
import boto3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------- CONFIGURATION ----------
FOLDER_TO_WATCH = "/home/najam/S3bucket/"
BUCKET_NAME = "presignedb12"   # 🔴 change this to your actual S3 bucket name
AWS_REGION = "ap-south-1"          # change if your bucket is in another region
# ----------------------------------

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION)

class S3SyncHandler(FileSystemEventHandler):

    # -------- Upload to S3 --------
    def upload_file(self, file_path):
        if os.path.isdir(file_path):
            return  # ignore folders, handled separately

        file_key = os.path.relpath(file_path, FOLDER_TO_WATCH)
        try:
            s3.upload_file(file_path, BUCKET_NAME, file_key)
            print(f"✅ Uploaded/Updated: {file_key}")
        except Exception as e:
            print(f"❌ Upload failed for {file_key}: {e}")

    # -------- Delete from S3 --------
    def delete_file(self, file_path):
        file_key = os.path.relpath(file_path, FOLDER_TO_WATCH)
        try:
            s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
            print(f"🗑️ Deleted from S3: {file_key}")
        except Exception as e:
            print(f"⚠️ Delete failed for {file_key}: {e}")

    # -------- Event Handlers --------
    def on_created(self, event):
        if event.is_directory:
            # Simulate folder in S3 using a .keep placeholder file
            folder_key = os.path.relpath(event.src_path, FOLDER_TO_WATCH).rstrip("/") + "/.keep"
            try:
                s3.put_object(Bucket=BUCKET_NAME, Key=folder_key, Body=b'')
                print(f"📁 Folder created (placeholder uploaded): {folder_key}")
            except Exception as e:
                print(f"❌ Folder upload failed: {e}")
        else:
            print(f"📄 Local file created: {event.src_path}")
            self.upload_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"✏️ Local file modified: {event.src_path}")
            self.upload_file(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            folder_key = os.path.relpath(event.src_path, FOLDER_TO_WATCH).rstrip("/") + "/.keep"
            try:
                s3.delete_object(Bucket=BUCKET_NAME, Key=folder_key)
                print(f"🗑️ Folder deleted from S3: {folder_key}")
            except Exception as e:
                print(f"⚠️ Folder delete failed: {e}")
        else:
            print(f"🗑️ Local file deleted: {event.src_path}")
            self.delete_file(event.src_path)

# -------- Main Watcher Setup --------
if __name__ == "__main__":
    print(f"👀 Watching local folder: {FOLDER_TO_WATCH}")
    print(f"☁️ Syncing changes to S3 bucket: {BUCKET_NAME}")

    event_handler = S3SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("🛑 Stopped watching.")
    observer.join()
