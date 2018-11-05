from picamera import PiCamera
import picamera.array
import numpy as np
import time

def set_params(camera):
    camera.led = False 
    time.sleep(2) # Allow camera to warm up.
    camera.awb_mode = 'off'
    camera.awb_gains = (1, 1.)
    camera.exposure_mode = 'off'
    camera.iso = 100
    camera.framerate = 1
    camera.drc_strength = 'off'
    camera.image_denoise = False
    camera.image_effect = 'none'

def grab_image(camera):
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        output = (stream.array() >> 2).astype(np.uint8)
        return output