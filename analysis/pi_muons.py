import os
from datetime import datetime
import muons
from matplotlib import pyplot as plt

folder = "data"
time_offset = 365760  # Raspberry pi time lags behind by this amount.


def get_counts():  # This only gets data from data.txt!
    """
        Returns a list containing the time of every recorded count. 
        There is only one count corresponding to each time, so a 1D
        list is sufficient.
    """
    lines = []
    with open("{}/data.txt".format(folder), 'r') as f:
        for l in f:
            lines.append(l)
    return parse_data(lines)


def parse_data(lines):
    """ 
        Gets the times of each count from the file, applying the 
        time_offset to ensure times are in sync with "real" time
        from other detectors and data.
    """
    return [float(i.split(": ")[-1]) + time_offset for i in lines]


def get_counts_in_time(counts, seconds=60):
    start = counts[0]  # The start value of each interval.
    # Tuple containing list of times and associated times.
    counts_in_time = ([], [])
    temp_counts = 0  # Number of counts in the current interval.
    for c in counts:
        if c - start > seconds:  # If we exceed interval, start a new one.
            counts_in_time[0].append(start)
            counts_in_time[1].append(temp_counts)
            temp_counts = 0
            start = c
        temp_counts += 1
    return counts_in_time


if __name__ == "__main__":
    data = get_counts()
    counts_per_min = get_counts_in_time(data, 600)
    times = counts_per_min[0]
    counts = counts_per_min[1]
    plt.plot(times, counts, ".")
    plt.show()
