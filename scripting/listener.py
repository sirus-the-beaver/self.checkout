import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_name, file_extension = os.path.splitext(event.src_path)

        if file_extension.lower() == ".mov":
            print(f'Image created: {event.src_path}')
            observer.stop()
        
            os.system("python3 facial_detection.py clip/IMG_0378.MOV")


if __name__ == "__main__":
    path = "clip"

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)

    print(f"Watching for new images...")

    try:
        observer.start()

    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()