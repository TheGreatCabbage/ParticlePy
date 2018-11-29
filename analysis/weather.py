import string
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

letters = string.ascii_uppercase
indices = list(map(lambda x: letters.index(x), list(letters)))
dict_letters = dict(zip(letters, indices))


def get_weather():
    data = []
    with open("data/{}".format("weather_nov.csv")) as f:
        index = 0
        for line in f:
            if index < 4:
                index += 1
                continue
            data.append(line.split(","))

    return data


def get_column(data, designation):
    index = dict_letters[designation]
    return list(map(lambda x: x[index], data))


def get_temperatures(data):
    return map_float(get_column(data, "E"))


def map_float(data):
    return list(map(lambda x: float(x), data))


def get_times(data):
    return list(map(lambda x: datetime.strptime(x, "%a"), get_column(data, "A")))


if __name__ == "__main__":
    data = get_weather()
    for datum in get_column(data, "E"):
        print(datum)
