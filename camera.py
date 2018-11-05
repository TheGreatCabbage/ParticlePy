from picamera import PiCamera
import time

def set_params(camera):
    camera.led = False 
    time.sleep(2) # Allow camera to warm up.
    camera.awb_mode = "off"
    camera.awb_gains = (1, 1.)
    camera.exposure_mode = "off"
    camera.iso = 100
    camera.framerate = 1
    camera.drc_strength = 'off'
    camera.image_denoise = False
    camera.image_effect = 'none'