from detector import Detector
import RPi.GPIO as gpio
import time

pin = 20


class PulseDetector(Detector):

    last_state = False

    def on_start(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(pin, gpio.IN)

    def update(self):
        state = gpio.input(pin)
        if state and self.last_state:
            return
        else:
            if state:
                self.on_detect()
            self.last_state = state

    def on_detect(self):
        msg = "{}: {}".format("Detection at", time.time())
        self.logger.log_data(msg)
        print(msg)
