from picamera import PiCamera
from scipy.misc import bytescale, imsave
from io import BytesIO
from numpy import frombuffer, uint16, uint8, delete, s_, ones
from pdb import set_trace
import picamera.array
import numpy as np
import time


def set_params(camera):
    camera.led = False
    time.sleep(2)  # Allow camera to warm up.
    camera.awb_mode = 'off'
    camera.awb_gains = (1, 1.)
    camera.exposure_mode = 'off'
    camera.iso = 400
    camera.framerate = 1
    camera.drc_strength = 'off'
    camera.image_denoise = False
    camera.image_effect = 'none'


def grab_image(camera):
    """
    See https://picamera.readthedocs.io/en/release-1.11/recipes2.html#raw-bayer-data-captures
    and https://github.com/pietkuip/raspberrypi_muon_microscope/blob/master/getrawimage.py
    """
    S = BytesIO()
    camera.capture(S, format='jpeg', bayer=True)
    data = S.getvalue()[-10270208:]  # Only need raw bayer data.
    data = data[32768:]
    data = frombuffer(data, dtype=uint8).reshape((2480, 4128))[:2464, :4100]
    data = data.astype(uint16) << 2
    for byte in range(4):
        data[:, byte::5] |= ((data[:, 4::5] >> ((4 - byte) * 2)) & 3)
    data = delete(data, s_[4::5], axis=1)
    return data


def save_image(img): imsave("out.png", img)


def analyse_image(img):
    count = 0
    for i in img:
        if count > 0: break
        for pixel in i:
            if pixel > 80:
                count += 1
    print("{0} bright pixels.".format(count))
