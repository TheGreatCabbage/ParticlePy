from time_utils import timestamp
import os


class Logger:

    output_folder = "data"
    log_file = "log.txt"

    def __init__(self):
        self.file = self.open_file()

    def open_file(self):
        if self.output_folder not in os.listdir("."):
            os.mkdir(self.output_folder)  # Create folder.
        if self.log_file not in os.listdir(self.output_folder):
            open(self.file_path(), 'w').close()  # Create file.
        return open(self.file_path(), 'a')

    def file_path(self): return f"{self.output_folder}/{self.log_file}"

    def log(self, msg):
        self.file.write(f"{timestamp()} - {msg}\n")

    def shutdown(self): self.file.close()
