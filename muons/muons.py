import time
import os
import numpy as np
import sys
from datetime import datetime

folder = "data"


def parse_data(*files):
    """
    Parses a data file, returning a dictionary containing the time in
    seconds since the epoch (key) and muon count (value).
    """
    # Add the path to the filenames (they are in the 'data/' folder).
    files = map(lambda x: "{}/{}".format(folder, x), files)
    result = []  # List of disctionaries.

    for file in files:
        # All the lines from the file in one list.
        lines = read_lines(file)
        
        data = {}  # Dictionary with time as key, muon count as value.
        for l in lines:
            # Separate any elements of text that have a space between them.
            line_data = l.split(" ")

            # Muon count if positive, unwanted data if negative.
            count = int(line_data[0]) - 40000
            # Time in seconds since the epoch.
            time = int(line_data[1])

            # Ensure that count is non-negative and set as value in 'data' associated with time.
            data[time] = count if count > 0 else 0
        result.append(data)
    return result


def read_lines(file):
    try:
        with open(file, 'r') as f:
            return f.readlines()
    except IsADirectoryError:
        print("Ignoring directory: {}".format(file))
    except FileNotFoundError:
        print("File does not exist, please check path: {}".format(file))
    except UnicodeDecodeError:
        print("Unicode error with {} - program will exit.".format(file))
        sys.exit(0)
    return []


def average(data):
    result = {}  # Final result.
    for item in data:  # Iterate over the data for each file.
        for key in item:  # Take key from current dict.
            # If that key already has been added to the final data, we don't want to do the average again.
            if key in result:
                continue  # Skip to next key.
            # Make a list to contain the values corresponding to the counts from different dicts.
            values = []
            for i in data:  # Iterate over dicts again to check which have the current key.
                # If it doesn't have the key, it will give -10.
                value = i.get(key, -10)
                # Only want to average valid (positive) results.
                if value >= 0:
                    values.append(value)
            # Add the average for this key to the final data.
            result[key] = sum(values) / len(values)
    return result


def make_unique(data):
    result = {}
    for item in data:  # Iterate over the data for each file.
        for key in item:  # Take key from current dict.
            result[key] = item[key]
    return result


def get_data(*files, conflict_strategy="average"):
    """
    Parses data files, averaging any duplicate entries by default. Returns a dictionary
    containing the time (key) and muon count (value).
    """
    if len(files) == 0:
        print("No files specified. Using all files in data directory...")
        files = [i for i in os.listdir(folder)]

    # List of dictionaries containing data from all files.
    data = parse_data(*files)
    # Deal with duplicate data.
    if conflict_strategy == "average":
        print("Averaging data...")
        return average(data)
    elif conflict_strategy == "overwrite":
        print("Overwriting duplicate data. This is dangerous! Take care...")
        return make_unique(data)
    else:
        print("Unknown conflict strategy: '{}'\nExiting.".format(conflict_strategy))
        sys.exit(-1)

def get_counts_from(data):
    return list(data.values())

def get_times_from(data):
    return list(data.keys())


# The if statement ensures that its code does not run when this file is imported.
if __name__ == "__main__":
    data = get_data()
    for v in (data.keys()):
        print("{} counts at {}".format(data[v], v))
