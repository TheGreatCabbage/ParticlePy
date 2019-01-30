import data
from matplotlib import pyplot as plt
import muons as mu
import numpy as np
from scipy import stats

data_tuple = (
    (data.get_lab_data_set2_600(), "Set 2"),
    (data.get_lab_data_set3_600(), "Set 3"),
    (data.get_pi_data(), "Raspberry Pi"),
)

weather_types = {
    "pressure": data.type_pressure,
    "temperature": data.type_temperature,
    "humidity": data.type_humidity,
    "solar irradiation": data.type_solar_irradiation,
    "rainfall": data.type_rainfall
}

for d in data_tuple:
    data_obj = d[0]

    count = 0

    for key, value in weather_types.items():
        y = data_obj.get(data.type_count)
        x = data_obj.get(value)

        slope, intercept, r, p, err = stats.linregress(x, y)
        if count == 1:  # Plotting temperatures.
            plt.plot(x, y, ".")
            plt.plot(x, np.array(x)*slope + intercept)
        print("{}, {}: correlation = {}".format(
            d[1], key, r))

        count += 1

    print("\n")

plt.show()
