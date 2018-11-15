import time
import os
import sys
from datetime import datetime

folder = "data"


def parse_data(files):
    """
    Parses a data file, returning a dictionary containing the time in
    seconds since the epoch (key) and muon count (value).
    """
    # Add the path to the filenames (they are in the 'data/' folder).
    files = map(lambda x: "{}/{}".format(folder, x), files)

    # All the lines from the selected files combined into one list.
    lines = read_lines(files)
    data = {}  # Dictionary with time as key, muon count as value.
    for l in lines:
        # Separate any elements of text that have a space between them.
        result = l.split(" ")

        # Muon count if positive, unwanted data if negative.
        count = int(result[0]) - 40000
        # Time in seconds since the epoch.
        time = int(result[1])

        # Ensure that count is non-negative and set as value in 'data' associated with time.
        data[time] = count if count > 0 else 0
    return data


def read_lines(files):
    lines = []
    for file in files:
        try:
            with open(file, 'r') as f:
                lines.extend(f.readlines())
        except IsADirectoryError:
            print("Ignoring directory: {}".format(file))
        except FileNotFoundError:
            print("File does not exist, please check path: {}".format(file))
        except UnicodeDecodeError:
            print("Unicode error with {} - program will exit.".format(file))
            sys.exit(0)
    return lines


def get_data(files=[], time_format="unix"):
    """
    Parses a data file, providing an option to format the
    time into a readable format.  Returns a dictionary
    containing the time (key) and muon count (value).
    """
    if len(files) == 0:
        print("No files specified. Using all files in data directory...")
        files = [i for i in os.listdir(folder)]

    data = parse_data(files)

    if time_format == "unix":
        return data

    new_data = {}
    if time_format == "utc":
        for k in data.keys():
            new_data[datetime.utcfromtimestamp(k).strftime(
                "%Y-%m-%d, %H:%M:%S")] = data[k]
    return new_data


# The if statement ensures that its code does not run when this file is imported.
if __name__ == "__main__":
    data = get_data()
    for v in (data.keys()):
        print("{} counts at {}".format(data[v], v))
