from imageio import imread, imsave
from detector import timestamp
import multiprocessing as mp
import math
import numpy as np
import os
import time 


def get_pixels(img):
    pixels = imread(img, as_gray=False, pilmode='L')
    return pixels


def analyse(name, data):
    x, y = data.shape
    threshold = np.average(data) + 80
    marking = 100
    for row in data:
        if np.max(row) > threshold:
            row[0: marking] = 255
    save_image(name, data)
    print("{} - Saved edit of image {}".format(timestamp(), name))


def save_image(name, data): imsave(name.replace("save", "edit"), data)


def get_images(): return list(map(lambda x: "data/{}".format(x),
                                  filter(lambda x: ".png" == x[-4:] and "edit" != x[:4], os.listdir("data/"))))


def analyse_images(images):
    for i in images:
        try:
            pixels = get_pixels(i)
        except ValueError:
            continue  # Error reading image.
        analyse(i, pixels)


def divide_into(list, parts): return np.array_split(list, parts)


if __name__ == "__main__":
    t0 = time.time()

    # Use multiprocessing for an 8x performance improvement (depending on CPU).
    cores = mp.cpu_count()
    images = divide_into(get_images(), cores)
    processes = []
    for i in range(0, len(images)):
        processes.append(mp.Process(target=analyse_images, args=(images[i],)))
        processes[i].start()
    for p in processes:
        p.join()
    print("Time elapsed: {} seconds.".format(time.time() - t0))
