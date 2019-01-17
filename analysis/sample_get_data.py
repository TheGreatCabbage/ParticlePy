import data
from matplotlib import pyplot as plt
import sys

"""
    This is a sample showing how to access data using the new data.py file.
"""

# Here's the Raspberry Pi data.
pi_data = data.get_pi_data()

# Another way to get the data. This method works for all datasets, just change the parameter.
pi_data = data.get_data(data.file_pi)

# You can get a particular type of data from a Data object using `get(data_type)`.
counts = pi_data.get(data.type_count)
times = pi_data.get(data.type_time)
# Get weather data from the same Data object.
pressures = pi_data.get(data.type_pressure)
temperatures = pi_data.get(data.type_temperature)

plt.subplot(3, 1, 1)
plt.plot(times, counts, ".")

plt.subplot(3, 1, 2)
plt.plot(times, pressures, "b.")

plt.subplot(3, 1, 3)
plt.plot(times, temperatures, "r.")

plt.show()  # Program pauses until window is closed.

# Get hourly lab data for set 2 and set 3.
set2 = data.get_data(data.file_lab_set2_3600)
set3 = data.get_data(data.file_lab_set3_3600)

# Plot times and counts for set 2 and set 3.
plt.plot(set2.get(data.type_time), set2.get(data.type_count), "g.")
plt.plot(set3.get(data.type_time), set3.get(data.type_count), "b.")
plt.show()
