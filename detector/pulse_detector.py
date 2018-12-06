from detector import Detector
import RPi.GPIO as gpio
import time
from functools import reduce

pin = 2


class PulseDetector(Detector):

    last_state = False # The last known state of the input pin. True means that there was a detection.
    cache_data = True
    cache = []
    max_cache_size = 100

    def on_start(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.IN)

    def update(self):
        state = gpio.input(pin) # The current state of the input pin. True means that there was a detection.
        # If state and last_state both true, it's probably still the same pulse. Skip to next update.
        if state and self.last_state:   
            return
        else:
            if state:
                self.on_detect()
            self.last_state = state # Set last state to current state for next update.

    def on_detect(self):
        t = time.time()
        # msg = self.get_msg(time)
        if self.cache_data:
            self.cache.append(t)
            if len(self.cache) > self.max_cache_size:
                self.save_cache()
                print("Saved cache")
                self.cache = []
        else:
            self.save_data(self.get_msg(time))
        # print(msg)

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
