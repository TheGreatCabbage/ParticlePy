import os
from datetime import datetime
import muons
from matplotlib import pyplot as plt

folder = "data"
name = "pi_data"
# Raspberry pi time lags behind by this amount. Need to adjust it to align with weather data and other muon data.
time_offset = 365760
# Only get data from files with "pi_data" in their names.
files = filter(lambda i: name in i[:len(name)], os.listdir(folder))


def get_counts():
    """
        Returns a list containing the time of every recorded count. 
        There is only one count corresponding to each time, so a 1D
        list is sufficient.
    """
    lines = []
    for f in files:
        with open("{}/{}".format(folder, f), 'r') as current_file:
            for l in current_file:
                lines.append(l)
    return parse_data(lines)


def parse_data(lines):
    """ 
        Gets the times of each count from the lines of data, applying the 
        time_offset to ensure times are in sync with "real" time
        from other detectors and data.
    """
    data_set = set(  # Remove duplicate items by using a set.
        map(lambda i: float(i.split(": ")[-1]) + time_offset, lines))  # Extract the time from each line, and adjust for the offset.
    return sorted(list(data_set))  # Convert back to a list, and sort.


def get_counts_in_time(counts, seconds=60):
    """
        Split up a list of times (each representing a single count)
        to get a list containing the number of counts in each interval of
        the parameter 'seconds'.
    """
    start = counts[0]  # The start value of each interval.
    # Tuple containing list of times and associated counts.
    counts_in_time = ([], [])
    temp_counts = 0  # Number of counts in the current interval.
    for c in counts:
        if c - start > seconds:  # If we exceed interval, start a new one.
            counts_in_time[0].append(start)
            counts_in_time[1].append(temp_counts / (c-start))
            temp_counts = 0
            start = c
        temp_counts += 1
    return counts_in_time


if __name__ == "__main__":
    data = get_counts()
    counts_per_time = get_counts_in_time(data, 600)
    times = counts_per_time[0]
    counts = counts_per_time[1]
    plt.plot(times, counts, ".")
    plt.show()
