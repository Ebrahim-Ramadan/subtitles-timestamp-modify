import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been modified. Restarting server...')
        subprocess.run(["python", "subtitles-modify-py.py"])


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
