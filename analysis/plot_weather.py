import matplotlib.pyplot as plt
import muons
import weather as w
import pi_muons as pi 

weather = w.get_data()
weather_times = w.get_times(weather)

muon_data = muons.get_data()
# Average in time intervals.
muon_data = muons.average_with_step(muon_data, 600*6)
muon_timestamps = muon_data[0]
muon_counts = muon_data[1]

pi_muons = pi.get_counts()
pi_muons_data = pi.get_counts_in_time(pi_muons, 600*6)
pi_times = pi_muons_data[0]
pi_counts = pi_muons_data[1]

time_initial = muon_timestamps[0]
time_final = muon_timestamps[-1]

subplots = []
weather_plot_data = (
    ("Temperature", "r.", w.get_temperatures(weather)),
    ("Humidity", "g.", w.get_humidity(weather)),
    ("Pressure", ".", w.get_pressures(weather)),
    ("Solar irradiation", "c.", w.get_solar_irradiation(weather)),
    ("Rainfall", "y.", w.get_rainfall(weather))
)

muons_plot = plt.subplot(331)
plt.plot(muon_timestamps, muon_counts, 'k.', label='Muons')
plt.legend()
muons_plot.set_ylim([2.8, max(muon_counts) + 0.05])

pi_muons_plot = plt.subplot(337)
subplots.append(pi_muons_plot)
plt.plot(pi_times, pi_counts, 'b.', label="RPi muons")
plt.legend()

for i in range(len(weather_plot_data)):
    plot_data = weather_plot_data[i]
    id = int("33{}".format(i + 2))

    subplots.append(plt.subplot(id))

    plt.plot(weather_times, plot_data[2], plot_data[1], label=plot_data[0])
    plt.legend()

for s in subplots:
    s.set_xlim([time_initial, time_final])

# muons.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=24*3600) ) # Show tick every 24 hours.

plt.tight_layout()
plt.show()
