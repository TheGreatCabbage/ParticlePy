import weather
import get_muon_data
import numpy as np
import matplotlib.pyplot as plt

cyl_2 = get_muon_data.get_cyl_data(2)
cyl_3 = get_muon_data.get_cyl_data(3)

pi_data = get_muon_data.get_pi_data()

pi_data[0] = sorted(pi_data[0])
pi_data[1] = sorted(pi_data[1])

cyl_2_av = get_muon_data.average_minutes_prior_to_x_cyl(cyl_2, 120)
cyl_3_av = get_muon_data.average_minutes_prior_to_x_cyl(cyl_3, 120)

pi_1 = get_muon_data.average_minutes_prior_to_x_pi(pi_data[0], 120)

data_dict = {}
# time: [cyl2, cyl3, pi2, pi3_3, pressure, temperature, rainfall, humidity, solar]
for time in range(len(cyl_2_av[1])):
    if not float(cyl_2_av[1][time]) in data_dict:
        data_dict[float(cyl_2_av[1][time])] = [cyl_2_av[0][time],np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    else:
        data_dict[float(cyl_2_av[1][time])][0] = cyl_2_av[0][time]

for time in range(len(cyl_3_av[1])):
    if not float(cyl_3_av[1][time]) in data_dict:
        data_dict[float(cyl_3_av[1][time])] = [0,cyl_3_av[0][time],np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    else:
        data_dict[float(cyl_3_av[1][time])][1] = cyl_3_av[0][time]

for time in range(len(pi_1[1])):
    if not float(pi_1[1][time]) in data_dict:
        data_dict[float(pi_1[1][time])] = [np.nan,np.nan,pi_1[0][time],np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    else:
        data_dict[float(pi_1[1][time])][2] = pi_1[0][time]

weather_data = weather.get_data()
times = weather.get_times(weather_data)
pressures = weather.get_pressures(weather_data)
rainfall = weather.get_rainfall(weather_data)
temperatures= weather.get_temperatures(weather_data)
humidity = weather.get_humidity(weather_data)
solar = weather.get_solar_irradiation(weather_data)


for time in range(len(times)):
    if not float(times[time]) in data_dict:
        data_dict[float(times[time])] = [np.nan,np.nan,np.nan,np.nan,pressures[time],temperatures[time],rainfall[time],humidity[time],solar[time]]
    else:
        data_dict[float(times[time])][4] = pressures[time]
        data_dict[float(times[time])][5] = temperatures[time]
        data_dict[float(times[time])][6] = rainfall[time]
        data_dict[float(times[time])][7] = humidity[time]
        data_dict[float(times[time])][8] = solar[time]

cyl_2 = []
cyl_3 = []
pi_1 = []
temp = []
press = []
rain = []
hum = []
solar = []

for key, value in data_dict.items():
    cyl_2.append(data_dict[key][0])
    cyl_3.append(data_dict[key][1])
    pi_1.append(data_dict[key][2])
    temp.append(data_dict[key][5])
    press.append(data_dict[key][4])
    rain.append(data_dict[key][6])
    hum.append(data_dict[key][7])
    solar.append(data_dict[key][8])

#plt.plot(cyl_3_av[1],cyl_3_av[0],'r.')
#plt.plot(pi_1[1],pi_1[0],'b.')

count = cyl_3

plt.subplot(3,2,1)
plt.plot(solar,count,'c.', label='solar')
plt.legend()

plt.subplot(3,2,2)
plt.plot(hum,count,'g.', label='hum')
plt.legend()

plt.subplot(3,2,3)
plt.plot(rain,count,'y.', label='rain')
plt.legend()

plt.subplot(3,2,4)
plt.plot(press,count,'b.', label='press')
plt.legend()

plt.subplot(3,2,5)
plt.plot(temp,count,'r.', label='temp')
plt.legend()

plt.tight_layout()
plt.show()

with open('listed2.txt', 'a') as f:
    f.write('solar,hum,rain,press,temp,count\n')
    for i in range(len(solar)):
        f.write('{},{},{},{},{},{}\n'.format(solar[i],hum[i],rain[i],press[i],temp[i],count[i]))
