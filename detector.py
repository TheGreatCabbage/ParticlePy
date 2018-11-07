from abc import ABC, abstractmethod
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
        return open(self.file_path(), 'a')  # Open file in append mode.

    def file_path(self):
        return "{0}/{1}".format(self.output_folder, self.log_file)

    def log(self, msg):
        self.file.write("{0} - {1}\n".format(timestamp(), msg))

    def shutdown(self): self.file.close()


class Detector(ABC):

    logger = Logger()
    running = True

    def start(self):
        self.on_start()
        self.logger.log("Detector started.")
        while self.running:
            self.update()

    def stop(self):
        self.running = False
        self.on_stop()
        self.shutdown()

    def shutdown(self):
        self.logger.log("Detector stopped.")
        self.logger.shutdown()

    def on_start(self): pass

    def on_stop(self): pass

    @abstractmethod
    def update(self): pass
