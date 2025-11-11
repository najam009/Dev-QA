import os
import time
import boto3
import psycopg2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv


load_dotenv()

# ---------- CONFIGURATION ----------
FOLDER_TO_WATCH = "/home/najam/S3bucket/"
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
HOST = os.getenv("HOST")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USERR")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

print(os.getenv("USERR"))

# PostgreSQL credentials
DB_CONFIG = {
    "host": HOST,      # your EC2/RDS endpoint
    "dbname": DBNAME,
    "user": USER,
    "password": PASSWORD,
    "port": PORT
}
# ----------------------------------

# Initialize S3 client
s3 = boto3.client("s3", region_name=AWS_REGION)

# ---------- DATABASE HELPERS ----------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def insert_file_record(file_name, s3_url):
    """Insert or update file info in s3_links table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO s3_links (file_name, s3_url)
            VALUES (%s, %s)
            ON CONFLICT (file_name)
            DO UPDATE SET
                s3_url = EXCLUDED.s3_url,
                uploaded_at = NOW();
            """,
            (file_name, s3_url)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"🗃️ Saved/Updated in database: {file_name}")
    except Exception as e:
        print(f"⚠️ Database insert failed: {e}")

def delete_file_record(file_name):
    """Delete file record from s3_links table."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM s3_links WHERE file_name = %s;", (file_name,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"🗑️ Deleted from database: {file_name}")
    except Exception as e:
        print(f"⚠️ Database delete failed: {e}")

# ---------- FILE EVENT HANDLER ----------
class S3SyncHandler(FileSystemEventHandler):
    def upload_file(self, file_path):
        if os.path.isdir(file_path):
            return

        file_key = os.path.relpath(file_path, FOLDER_TO_WATCH)

        try:
            # Upload file to S3
            s3.upload_file(file_path, BUCKET_NAME, file_key)
            print(f"✅ Uploaded/Updated: {file_key}")

            # Generate permanent public URL
            s3_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"

            # Insert record in PostgreSQL
            insert_file_record(file_key, s3_url)

        except Exception as e:
            print(f"❌ Upload failed for {file_key}: {e}")

    def delete_file(self, file_path):
        file_key = os.path.relpath(file_path, FOLDER_TO_WATCH)
        try:
            # Delete from S3
            s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
            print(f"🗑️ Deleted from S3: {file_key}")

            # Delete record from PostgreSQL
            delete_file_record(file_key)

        except Exception as e:
            print(f"⚠️ Delete failed for {file_key}: {e}")

    def on_created(self, event):
        if event.is_directory:
            # Create folder placeholder
            folder_key = os.path.relpath(event.src_path, FOLDER_TO_WATCH).rstrip("/") + "/.keep"
            try:
                s3.put_object(Bucket=BUCKET_NAME, Key=folder_key, Body=b"")
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

# ---------- MAIN ----------
if __name__ == "__main__":
    print(f"👀 Watching local folder: {FOLDER_TO_WATCH}")
    print(f"☁️ Syncing changes to S3 bucket: {BUCKET_NAME}")
    print(f"🗃️ Logging uploads to PostgreSQL table: s3_links")

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
