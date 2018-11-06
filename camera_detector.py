from camera import *
from detector import Detector
from numpy import ndarray
from picamera import PiCamera
import time


class CameraDetector(Detector):

    def update(self):
        img = grab_image(self.camera)
        analyse_image(img)
        print("Taken image")

    def on_start(self):
        self.camera = PiCamera()
        set_params(self.camera)
