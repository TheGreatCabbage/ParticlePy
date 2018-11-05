from camera import set_params
from detector import Detector
from picamera import PiCamera
import time


class CameraDetector(Detector):

    def update(self):
        pass

    def on_start(self):
        self.camera = PiCamera()
        set_params(self.camera)
