import matplotlib.pyplot as plt
import muons
import weather as w


weather = w.get_data()
weather_times = w.get_times(weather)

muon_data = muons.get_data()
# Average every 60 minutes.
muon_data = muons.average_with_step(muon_data, 600*6)
muon_timestamps = muon_data[0]
muon_counts = muon_data[1]

time_initial = muon_timestamps[0]
time_final = muon_timestamps[-1]

subplots = []
weather_plot_data = (
    ("Temperature", "r.", w.get_temperatures(weather)),
    ("Pressure", ".", w.get_pressures(weather)),
    ("Humidity", "g.", w.get_humidity(weather)),
    ("Solar irradiation", "c.", w.get_solar_irradiation(weather)),
    ("Rainfall", "y.", w.get_rainfall(weather))
)

for i in range(len(weather_plot_data)):
    plot_data = weather_plot_data[i]
    id = int("32{}".format(i + 2))

    subplots.append(plt.subplot(id))
    subplots[i].set_xlim([time_initial, time_final])

    plt.plot(weather_times, plot_data[2], plot_data[1], label=plot_data[0])
    plt.legend()

muons_plot = plt.subplot(321)
plt.plot(muon_timestamps, muon_counts, 'k.', label='Muons')
plt.legend()
muons_plot.set_ylim([2.8, max(muon_counts) + 0.05])
muons_plot.set_xlim([time_initial, time_final])
# muons.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=24*3600) ) # Show tick every 24 hours.

plt.tight_layout()
plt.show()
