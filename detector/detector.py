from abc import ABC, abstractmethod
from datetime import datetime
from time import time
import shutil
import os


def timestamp():
    return datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H-%M-%S").replace(" ", "_")


class Logger:

    output_folder = "data"
    log_file_name = "log.txt"
    data_file_name = "data.txt"

    def __init__(self):
        self.log_file, self.data_file = self.open_files()

    def open_files(self):
        self.create_folder()
        return (self.open_file_append(self.log_file_name),
                self.open_file_append(self.data_file_name))

    def file_path(self, name):
        return "{}/{}".format(self.output_folder, name)

    def log(self, msg):
        self.log_file.write("{} - {}\n".format(timestamp(), msg))

    def log_data(self, msg):
        self.data_file.write(msg + "\n")

    def purge(self):
        shutil.rmtree(self.output_folder)
        self.create_folder()

    def create_folder(self):
        # Create folder if not exists.
        if self.output_folder not in os.listdir("."):
            os.mkdir(self.output_folder)  

    def open_file_append(self, name):
        # Create file if not exists.
        if name not in os.listdir(self.output_folder):
            open(self.file_path(name), 'w').close()
        return open(self.file_path(name), 'a')  # Open file in append mode.

    def shutdown(self):
        self.log_file.close()
        self.data_file.close()


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