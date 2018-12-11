from detector import Detector
import RPi.GPIO as gpio
import time
from functools import reduce

pin = 2


class PulseDetector(Detector):

    # The last known state of the input pin. True means that there was a detection.
    last_state = False
    cache_data = True
    cache = []
    max_cache_size = 100
    current_size = 0

    def on_start(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.IN)

    def update(self):
        # The current state of the input pin. True means that there was a detection.
        state = gpio.input(pin)
        # If state and last_state both true, it's probably still the same pulse. Skip to next update.
        if state and self.last_state:
            return
        else:
            if state:
                self.on_detect()
            # Set last state to current state for next update.
            self.last_state = state

    def on_detect(self):
        t = time.time()
        if self.cache_data:
            self.cache.append(t)
            self.current_size += 1
            if self.current_size > self.max_cache_size:
                self.save_cache()
                print("Saved cache")
                self.cache = []
                self.current_size = 0
            return
        self.save_data(self.get_msg(time))

    def on_stop(self):
        self.save_cache()
        print("Detector stopping... Saved cache.")

    def get_msg(self, time):
        return "{}: {}".format("Detection at", time)

    def save_data(self, data):
        self.logger.log_data(data)

    def save_cache(self):
        m = map(lambda x: self.get_msg(x), self.cache)
        out = reduce(lambda a, b: "{}\n{}".format(a, b), m)
        self.save_data(out)
