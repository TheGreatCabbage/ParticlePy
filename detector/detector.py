from abc import ABC, abstractmethod
from datetime import datetime
from time import time
import shutil
import os


def timestamp():
    return datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H-%M-%S").replace(" ", "_")


class Logger:

    output_folder = "data"
    log_file = "log.txt"
    data_file = "data.txt"

    def __init__(self):
        self.file = self.open_file()
        self.data_file = self.open_data_file()

    def open_file(self):
        self.create_folder()
        if self.log_file not in os.listdir(self.output_folder):
            open(self.file_path(), 'w').close()  # Create file.
        return open(self.file_path(), 'a')  # Open file in append mode.

    def open_data_file(self):
        if self.data_file not in os.listdir(self.output_folder):
            open(self.file_path(self.data_file), 'w').close()  # Create file.
        return open(self.file_path(self.data_file), 'a') # Open file in append mode.

    def file_path(self, name=log_file):
        return "{0}/{1}".format(self.output_folder, name)

    def log(self, msg):
        self.file.write("{0} - {1}\n".format(timestamp(), msg))

    def log_data(self, msg):
        self.data_file.write(msg + "\n")

    def purge(self):
        shutil.rmtree(self.output_folder)
        self.create_folder()

    def create_folder(self):
        if self.output_folder not in os.listdir("."):
            os.mkdir(self.output_folder)  # Create folder.

    def shutdown(self): self.file.close()


class Detector(ABC):

    logger = Logger()
    running = True
    purge_on_start = False

    def start(self):
        if self.purge_on_start:
            self.logger.purge()
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
