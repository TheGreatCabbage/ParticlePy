import os
from datetime import datetime
import muons
from matplotlib import pyplot as plt

folder = "data"


def get_counts():  # This only gets data from data.txt!
    """
        Returns a list containing the time of every recorded count. 
        There is only one count corresponding to each time.
    """
    lines = []
    with open("{}/data.txt".format(folder), 'r') as f:
        for l in f:
            lines.append(l)
    return parse_data(lines)


def parse_data(lines):
    return [float(i.split(": ")[-1]) for i in lines]


def get_counts_in_time(counts, seconds=60):
    start = counts[0]
    counts_in_time = ([], [])
    current = 0
    for c in counts:
        if c - start > seconds:
            counts_in_time[1].append(current)
            counts_in_time[0].append(start)
            current = 0
            start = c
        current += 1
    return counts_in_time


if __name__ == "__main__":
    data = get_counts()
    counts_per_min = get_counts_in_time(data)
    times = counts_per_min[0]
    counts = counts_per_min[1]
    plt.plot(times, counts, ".")
    plt.show()
