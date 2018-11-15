import time
from datetime import datetime

file = "C:/Program Files (x86)/Muon/sample_data/muon.data"


def get_basic_data(filename=file):
    data = {}  # Dictionary with time as key, muon count as value.
    with open(file, 'r') as f:
        for l in f.readlines():
            result = l.split(" ")

            # Muon count if positive, unwanted data if negative.
            count = int(result[0]) - 40000
            # Time in seconds since the epoch.
            time = int(result[1])

            data[time] = count if count > 0 else 0

    return data


def get_data(filename=file, time_format="unix"):
    data = get_basic_data(filename)
    if time_format == "unix":
        return data

    new_data = {}
    if time_format == "utc":
        for k in data.keys():
            new_data[datetime.utcfromtimestamp(k).strftime(
                "%Y-%m-%d, %H:%M:%S")] = data[k]
    return new_data


data = get_data()
for v in (data.keys()):
    print("{} counts at {}".format(data[v], v))
