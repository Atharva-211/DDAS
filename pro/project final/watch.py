import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder to be monitored
FOLDER_TO_WATCH = "D:/SIH/pro/project final/download"

# FastAPI upload endpoint
UPLOAD_URL = "http://127.0.0.1:8000/upload"

class FileWatcher(FileSystemEventHandler):
    def on_created(self, event):
        # Check if the created event is for a file
        if not event.is_directory:
            file_path = event.src_path
            print(f"New file detected: {file_path}")
            # Add a delay to ensure the file is fully written
            time.sleep(2)
            upload_file(file_path)

def upload_file(file_path, retries=3):
    """Tries to upload the file, with retry mechanism."""
    attempt = 0
    while attempt < retries:
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file)}
                response = requests.post(UPLOAD_URL, files=files)
                if response.status_code == 200:
                    print(f"File {file_path} uploaded successfully.")
                else:
                    print(f"Failed to upload {file_path}. Status code: {response.status_code}")
            break
        except PermissionError as e:
            print(f"Permission error for file {file_path}. Retrying... {attempt + 1}/{retries}")
            time.sleep(1)
            attempt += 1
        except Exception as e:
            print(f"Error uploading file {file_path}: {e}")
            break

if __name__ == "__main__":
    event_handler = FileWatcher()
    observer = Observer()
    observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=False)

    print(f"Monitoring folder: {FOLDER_TO_WATCH}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
