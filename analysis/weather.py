import string
import os
from datetime import datetime

"""
E - Temperature (°C) (measured by temp/RH sensor in Stevenson Screen)
F - Relative Humidity (%) in Stevenson Screen
G - Solar irradiation: 10 min average (kW/m2)
H - Solar irradiation: 10 min total (kJ/m2)
I, J - Sunshine duration (minutes, seconds)
K - Air temperature in Stevenson Screen (°C)
L - Concrete temperature (°C)
M - Grass temperature (°C)
N, O, P, Q, R, S - Soil temperatures at 5, 10, 20, 30, 50, 100cm (°C)
T, U, V, W - Sonic Anemometer (wind speed in 3 planes)
Y - Windspeed at 10m on mast (m/s)
Z - Wind direction at 10m on mast (degrees)
AA - Rainfall 10 min total (mm)
AB - Air Pressure (mbar)

"""

data_type = {
    'timestamp': 0,
    'temperature': 4,
    'humidity': 5,
    'total_solar_irradiation': 6,
    'rainfall': 21,
    'pressure': 22,
}
folder = "data"


def get_data():
    """
        Returns a list, sorted by time, whose items are each 
        a list containing the value of each column in a row
        from the weather CSV file. 
    """
    data = []
    for file in os.listdir(folder):
        if "weather_" not in file:  # Use only files with "weather_" in their name.
            continue
        with open("{}/{}".format(folder, file), 'r') as f:
            index = 0
            for line in f:
                # Skip first few lines - they don't contain weather data.
                if index < 4:
                    index += 1
                    continue
                line_data = line.split(",")
                # Convert timestamp to Unix time.
                line_data[0] = unix_time(line_data[0])
                data.append(line_data)

    return sorted(data, key=lambda i: i[0])  # Sort data by time.


def get_column(data, designation):
    """
        Returns a list containing the appropriate data type,
        retaining the same order as in the 'data' parameter.
    """
    index = data_type[designation]
    return list(map(lambda x: x[index], data))


def get_times(data): return get_column(data, "timestamp")


def get_temperatures(data): return map_float(get_column(data, "temperature"))


def get_pressures(data): return map_float(get_column(data, "pressure"))


def get_rainfall(data): return map_float(get_column(data, "rainfall"))


def get_humidity(data): return map_float(get_column(data, "humidity"))


def get_solar_irradiation(data):
    return map_float(get_column(data, "total_solar_irradiation"))


def map_float(data):
    """
        Converts a list's items to floats, returning the modified list.
    """
    return list(map(lambda x: float(x), data))


def unix_time(time_str):
    """
        Converts a timestamp from the weather data to Unix time.
    """
    return datetime.strptime(time_str, "%d/%m/%Y %H:%M").timestamp()
