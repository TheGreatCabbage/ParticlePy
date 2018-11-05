from datetime import datetime
from time import time


def timestamp():
    return datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
