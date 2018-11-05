from camera import *
from detector import Detector
from picamera import PiCamera
import time


class CameraDetector(Detector):

    def update(self):
        img = grab_image(self.camera)
        print(img)

    def on_start(self):
        self.camera = PiCamera()
        set_params(self.camera)
