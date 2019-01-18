from functools import reduce
import os
import sys

type_pressure = "p"
type_temperature = "t"
type_humidity = "h"
type_solar_irradiation = "s"
type_rainfall = "r"
type_time = "time"
type_count = "count"

file_lab = "generated_lab_data"
file_pi = "generated_pi_data"
file_lab_avg_600 = "generated_lab_data_avg_600"
file_lab_set2_600 = "generated_lab_data_set2_600"
file_lab_set3_600 = "generated_lab_data_set3_600"
file_lab_set2_3600 = "generated_lab_data_set2_3600"
file_lab_set3_3600 = "generated_lab_data_set3_3600"


class Datum:
    """A single datum object containing count, time and weather data."""

    def __init__(self,
                 count=None,
                 time=None,
                 pressure=None,
                 temperature=None,
                 humidiity=None,
                 solar_irradiation=None,
                 rainfall=None):

        self.data = {
            type_pressure: pressure,
            type_humidity: humidiity,
            type_temperature: temperature,
            type_solar_irradiation: solar_irradiation,
            type_rainfall: rainfall,
            type_count: count,
            type_time: time
        }

    def get(self, data_type):
        """Get the value of a particular data type, such as `type_pressure`."""
        data = self.data[data_type]
        if data and data != "None":
            return float(data)
        return data

    def set(self, data_type, data_item):
        """Set the value of a particular data type, such as `type_pressure`."""
        self.data[data_type] = data_item

    def set_weather(self, index, pressures, temperatures, solars, rainfalls, humidities):
        """
        Set all the weather values for a datum object by providing 
        lists of different weather types and the index for the appropriate
        item in all lists.
        """
        self.set(type_pressure, pressures[index])
        self.set(type_temperature, temperatures[index])
        self.set(type_solar_irradiation, solars[index])
        self.set(type_rainfall, rainfalls[index])
        self.set(type_humidity, humidities[index])

    def from_string(self, string):
        """Load the datum object from its string representation."""
        for item in string.split(","):
            data = item.split(":")
            new_item = data[1]
            if new_item and new_item != "None":
                new_item = float(new_item)
            self.data[data[0]] = new_item
        return self

    def to_string(self):
        """Convert the datum object to its string representation."""
        m = map(lambda x: "{}:{}".format(x, self.data[x]), self.data)
        return reduce(lambda a, b: "{},{}".format(a, b), m)


class Data:
    """A data object containing many datum objects."""

    def __init__(self):
        self.data = []

    def add(self, datum):
        """Add a datum object."""
        self.data.append(datum)

    def add_from_string(self, string):
        """Add a datum object from its string representation."""
        self.data.append(Datum().from_string(string))

    def get(self, data_type):
        """Get a list of a particular type of data, such as count or pressure."""
        return list(map(lambda x: x.get(data_type), self.data))

    def write_to_file(self, file_name):
        """Write all contained datum objects to a file as their string representations."""
        with open(get_file_path(file_name), 'w') as f:
            strings = map(lambda x: x.to_string(), self.data)
            out = "\n".join(strings)
            f.write(out)

    def from_file(self, file_name):
        """Load all datum objects from their string representations in a file."""
        if file_name not in map(lambda x: x.split(".")[0], os.listdir("data")):
            print("\n{1}\nNo file named \"{0}\" found, may need to generate it by running reformatter.py!\n{1}\n".format(
                file_name, 30*"*"))
            sys.exit(0)
        with open(get_file_path(file_name), 'r') as f:
            for line in f:
                self.add_from_string(line)
        return self

    def from_counts_times(self, counts, times):
        """
        Load datum objects based on a list of counts and list of times.
        These datum objects will not have any associated weather data 
        until it is specifically assigned.
        """
        for i in range(len(times)):
            datum = Datum(count=counts[i], time=times[i])
            self.add(datum)
        return self


def get_file_path(file_name): return "data/{}.txt".format(file_name)


def get_data(file_name): return Data().from_file(file_name)


def get_lab_data(): return get_data(file_lab)


def get_lab_data_avg_600(): return get_data(file_lab_avg_600)


def get_lab_data_set2_600(): return get_data(file_lab_set2_600)


def get_lab_data_set3_600(): return get_data(file_lab_set3_600)


def get_lab_data_set2_3600(): return get_data(file_lab_set2_3600)


def get_lab_data_set3_3600(): return get_data(file_lab_set3_3600)


def get_pi_data(): return get_data(file_pi)