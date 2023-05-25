import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Directory to observe
directory = os.environ.get("PATH_LOGS")

# Log file path
log_file = os.path.join("log/", "daemon.log")

# Configure logging settings
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)


class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info("Running process_7days_log.py")
        os.system("python process_7days_log.py")


def observe_directory():
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    logging.info("Observer started for directory: %s", directory)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    # We run process_7days_log.py a first time to process the logs
    # that are already in the directory
    os.system("python process_7days_log.py")
    observe_directory()
