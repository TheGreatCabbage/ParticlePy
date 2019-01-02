import matplotlib.pyplot as plt
import pyqtgraph as pg
import numpy as np
import csv
import datetime
import time


def get_unix_time(timestamp):
    unixtime = time.mktime(datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M").timetuple())
    return unixtime

def get_weather_data(datatype):
    data_list = []
    for weather_file in weather_files:
        with open(filename) as weather_file:
            weather_data = csv.reader(weather_file, delimiter=',')
            i=0
            for row in weather_data:
                if not i < 4:
                    data_list.append(row[get_data_index(datatype)])
                i += 1
    return data_list

def get_muon_data(filename):
    data_list = [[],[]]
    with open(filename) as muon_file:
        muon_data = csv.reader(muon_file, delimiter=' ')
        for row in muon_data:
            #count
            data_list[0].append(row[0])
            #timestamp
            data_list[1].append(row[1])
    return data_list

def get_data_index(datatype):
    data_key = {
            'timestamp':0,
            'temperature':4,
            'humidity':5,
            'total solar irradiation':6,
            'rainfall':21,
            'pressure':22,
            }

    return data_key[datatype]

#muon_files = ['18-11-15-14-19 Set 2.data', '18-11-15-16-59 Set 2.data', '18-11-16-11-30 Set 2.data', '18-11-16-16-05 Set 2.data', '18-11-20-10-01 Set 2.data', '18-11-22-10-08 Set 2.data']

data_folder = 'data'

set_2_data_files = []
set_3_data_files = []
#weatherfile = 'Nov2018.csv'
weather_files = []

for file in os.listdir(data_folder):
    if "weather_" in file:
        weather_files.append("{}/{}".format(data_folder, file))
    elif "2.data" in file:
        set_2_data_files.append("{}/{}".format(data_folder, file))
    elif "3.data" in file:
        set_3_data_files.append("{}/{}".format(data_folder, file))

pi_data_files_1 = ['data/pi_data_0.txt', 'data/pi_data_1.txt', 'data/pi_data_2.txt']
pi_data_files_3_3 = ['data/pi_data_3.txt']

weather_timestamps = get_weather_data('timestamp')
pressures = get_weather_data('pressure')
temperatures = get_weather_data('temperature')
humidity = get_weather_data('humidity')
solar = get_weather_data('total solar irradiation')
rainfall = get_weather_data('rainfall')


weather_data_store = {} 





unixtimes = []
for timestamp in weather_timestamps:
    unixtimes.append(get_unix_time(timestamp))

muon_timestamps = []
muon_counts = []
for muon_file in muon_files:
    muon_counts += get_muon_data(muon_file)[0]
    muon_timestamps += get_muon_data(muon_file)[1]

muon_counts[:] = [int(x) for x in muon_counts]
muon_timestamps[:] = [int(x) for x in muon_timestamps]
temperatures[:] = [float(x) for x in temperatures]
pressures[:] = [float(x) for x in pressures]
humidity[:] = [float(x) for x in humidity]
solar[:] = [float(x) for x in solar]
rainfall[:] = [float(x) for x in rainfall]

#plt.plot(temperatures,'.')

plt.subplot(321)
plt.plot(unixtimes, pressures, '.',label='pressures')
plt.legend()

plt.subplot(322)
plt.plot(unixtimes, temperatures, 'r.', label='temperatures')
plt.legend()

plt.subplot(323)
plt.plot(unixtimes, humidity, 'g.', label='humidity')
plt.legend()

plt.subplot(324)
plt.plot(unixtimes, solar, 'c.', label='solar irradiation')
plt.legend()

plt.subplot(325)
plt.plot(unixtimes, rainfall, 'y.', label='rainfall')
plt.legend()

plt.subplot(326)
plt.plot(muon_timestamps, muon_counts, 'k.', label='muons')
plt.legend()

plt.tight_layout()
plt.show()
