from abc import ABC, abstractmethod
from logging import Logger


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
