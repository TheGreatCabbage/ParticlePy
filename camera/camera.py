from picamera import PiCamera
from detector import timestamp
from scipy.misc import bytescale, imsave
from io import BytesIO
from numpy import frombuffer, uint16, uint8, delete, s_, ones
from pdb import set_trace
import picamera.array
from analyse import folder
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


def save_image(img, name="out"): imsave("{}/{}.png".format(folder, name), img)


threshold = 521630000


def analyse_image(img):
    brightness = np.sum(img)
    print("Brightness is {}. {}".format(brightness,
                                        "Above threshold!" if brightness > threshold else ""))
    if brightness > threshold:
        save_image(img, "save_{}".format(timestamp()))
