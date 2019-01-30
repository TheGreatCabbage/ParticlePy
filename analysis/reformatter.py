from data import *
import pi_muons as pi
import muons as mu
import sys
import weather as w
from multiprocessing import Process

"""
    This script is used to calculate useful datasets, then save them in a form easy and quick to parse using data.py.
    
    You can create a new dataset by adding a new Process to the dictionary and an appropriate function to save the data. 
    You should also add a new `file_` variable in data.py.
"""


def associate_weather(data, weather_dict, min_difference=60*30):
    weather_index = 0
    for datum in data.data:
        weather_index = get_closest(datum, weather_dict, weather_index)
        apply_weather(datum, weather_dict, weather_index, min_difference)


def get_closest(datum, weather_dict, previous_index):
    index = previous_index
    datum_time = datum.get(type_time)

    times = weather_dict[type_time]
    smallest_diff = times[-1]
    for i in range(index, len(times)):
        diff = abs(times[i] - datum_time)
        if diff > smallest_diff:
            index = i
            break
        smallest_diff = diff
    return index


def apply_weather(datum, weather_dict, index, min_difference):
    if abs(datum.get(type_time)-weather_dict[type_time][index]) <= min_difference:
        datum.set_weather(index, pressures=weather_dict[type_pressure], temperatures=weather_dict[type_temperature],
                          solars=weather_dict[type_solar_irradiation], rainfalls=weather_dict[type_rainfall], humidities=weather_dict[type_humidity])


def write_lab_data():
    times, counts = mu.get_data(no_print=True)
    data = Data().from_counts_times(counts, times)
    associate_weather(data, w.get_data())
    data.write_to_file(file_lab)

def write_lab_set_2(weather_dict):
    times, counts = mu.average_with_step(mu.get_data_set_2(no_print=True), 600)
    write_lab_10min(weather_dict, times, counts, file_lab_set2_600)


def write_lab_set_3(weather_dict):
    times, counts = mu.average_with_step(mu.get_data_set_3(no_print=True), 600)
    write_lab_10min(weather_dict, times, counts, file_lab_set3_600)


def write_lab_10min(weather_dict, times, counts, output_file):
    data = Data().from_counts_times(counts, times)

    associate_weather(data, weather_dict)
    data.write_to_file(output_file)


def write_lab_set_2_hourly(weather_dict):
    times, counts = mu.average_with_step(
        mu.get_data_set_2(no_print=True), 3600)
    write_lab_hourly(weather_dict, times, counts, file_lab_set2_3600)


def write_lab_set_3_hourly(weather_dict):
    times, counts = mu.average_with_step(
        mu.get_data_set_3(no_print=True), 3600)
    write_lab_hourly(weather_dict, times, counts, file_lab_set3_3600)


def write_lab_hourly(weather_dict, times, counts, output_file):
    data = Data().from_counts_times(counts, times)
    associate_weather(data, weather_dict)
    data.write_to_file(output_file)


def write_pi_data(weather_dict):
    times, counts = pi.get_counts_in_time(pi.get_counts(), seconds=600)
    data = Data().from_counts_times(counts, times)

    associate_weather(data, weather_dict)
    data.write_to_file(file_pi)


def write_pi_data_hourly(weather_dict):
    times, counts = pi.get_counts_in_time(pi.get_counts(), seconds=3600)
    data = Data().from_counts_times(counts, times)

    associate_weather(data, weather_dict)
    data.write_to_file(file_pi_3600)


if __name__ == "__main__":
    print("Loading weather data...")
    weather = w.get_data()
    weather_dict = {
        type_humidity: w.get_humidity(weather),
        type_pressure: w.get_pressures(weather),
        type_rainfall: w.get_rainfall(weather),
        type_solar_irradiation: w.get_solar_irradiation(weather),
        type_temperature: w.get_temperatures(weather),
        type_time: w.get_times(weather)
    }
    processes = {
        Process(target=write_lab_set_2, args=(weather_dict,)): "write lab data (set 2) averaged over 10 minutes",
        Process(target=write_lab_set_3, args=(weather_dict,)): "write lab data (set 3) averaged over 10 minutes",
        Process(target=write_lab_set_2_hourly, args=(weather_dict,)): "write lab data (set 2) averaged over 1 hour",
        Process(target=write_lab_set_3_hourly, args=(weather_dict,)): "write lab data (set 3) averaged over 1 hour",
        Process(target=write_pi_data, args=(weather_dict,)): "write Raspberry Pi data averaged over 10 minutes",
        Process(target=write_pi_data_hourly, args=(weather_dict,)): "write Raspberry Pi data averaged over 1 hour"
    }

    for p in processes:
        p.start()

    print("All tasks in progress; this may take a while...")
    for p in processes:
        p.join()
        print("Process finished: {}".format(processes[p]))

    print("All tasks finished.")
