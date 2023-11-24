import threading
from datetime import datetime
from queue import Queue
import os

class LogLevel:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


class ILog:
    def write(self, level, message):
        pass

    def info(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

    def debug(self, message):
        pass

    def stop(self, wait=False):
        pass


class Message:
    def __init__(self, level, text):
        self.timestamp = datetime.now()
        self.level = level
        self.text = text


class LogComponent(ILog):
    def __init__(self, log_file_format="log_%Y%m%d.log", log_directory="logs"):
        self.log_file_format = log_file_format
        self.log_directory = log_directory
        self.stop_event = threading.Event()
        self.stop_immediately = threading.Event()
        self.log_queue = Queue()
        self.log_queue_lock = threading.Lock()
        self.thread = threading.Thread(target=self._write_logs)
        self.current_date = None
        self.thread.start()

    def write(self, level, message_text):
        with self.log_queue_lock:
            message = Message(level, message_text)
            self.log_queue.put(message)

    def info(self, message):
        self.write(LogLevel.INFO, message)

    def warning(self, message):
        self.write(LogLevel.WARNING, message)

    def error(self, message):
        self.write(LogLevel.ERROR, message)

    def debug(self, message):
        self.write(LogLevel.DEBUG, message)

    def stop(self, wait=False):
        self.stop_event.set()
        if not wait:
            self.stop_immediately.set()
        self.thread.join()

    def _write_logs(self):
        while not self.stop_event.is_set():
            current_date = datetime.now().strftime(self.log_file_format)
            if not self.current_date or current_date != self.current_date:
                self.current_date = current_date

            with self.log_queue_lock:
                while not self.log_queue.empty() and not self.stop_immediately.is_set():
                    message = self.log_queue.get()
                    self._write_log_to_file(message)

    def _write_log_to_file(self, message):
        log_file = self.current_date
        log_path = os.path.join(self.log_directory, log_file)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        try:
            with open(log_path, "a") as file:
                file.write(f"{message.timestamp} - {message.level}: {message.text}\n")
        except Exception as e:
            print(f"Error writing log to file: {e}")
