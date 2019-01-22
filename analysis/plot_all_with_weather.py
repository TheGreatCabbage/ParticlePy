import data
from matplotlib import pyplot as plt
import weather as w

"""
Plot muons from all detectors separately, with weather.
"""

lab_set2 = data.get_lab_data_set2_3600()
lab_set2_times = lab_set2.get(data.type_time)

lab_set3 = data.get_lab_data_set3_3600()
lab_set3_times = lab_set3.get(data.type_time)

pi = data.get_data(data.file_pi_3600)
weather = w.get_data()
weather_times = w.get_times(weather)

# Use these for x-limits, so all plots aligned.
min_time = min(lab_set2_times[0], pi.get(data.type_time)[0])
max_time = max(lab_set2_times[-1], pi.get(data.type_time)[-1])


class Subplot:
    """
    A data object to make many subplots simpler.
    """

    def __init__(self, xvalues, yvalues, xlabel, ylabel, subplot_index, plot_appearance=".", ylim=None, label=None, yerr=None):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.subplot_index = subplot_index
        self.plot_appearance = plot_appearance
        self.ylim = ylim
        self.label = label
        self.yerr = yerr

    def set_ylimits(self):
        if self.ylim and len(self.ylim) == 2:
            plt.ylim(self.ylim[0], self.ylim[1])

    def legend(self):
        """Set the legend, using the label specified in the constructor."""
        if self.label:
            plt.legend([self.label])


# The ratio of points plotted to error bars plotted.
error_bars_ratio = 10

subplots = (
    # Counts for lab_set2 data.
    Subplot(lab_set2_times, lab_set2.get(data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            331, ylim=(1, 6), label="Lab muon detector (set 2)"),

    # Error bars for lab_set2 data.
    Subplot(lab_set2.get_subset(error_bars_ratio, data.type_time),
            lab_set2.get_subset(error_bars_ratio,
                                data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            331,
            "none",
            yerr=lab_set2.get_subset(error_bars_ratio, data.type_error)),

    Subplot(lab_set3_times, lab_set3.get(data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            334, ylim=(1, 6), label="Lab muon detector (set 3)"),

    Subplot(lab_set3.get_subset(error_bars_ratio, data.type_time),
            lab_set3.get_subset(error_bars_ratio,
                                data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            334,
            "none",
            yerr=lab_set3.get_subset(error_bars_ratio, data.type_error)),


    Subplot(pi.get(data.type_time), pi.get(data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            337, ylim=(0, 1.2), label="Raspberry Pi muon detector"),

    Subplot(pi.get_subset(error_bars_ratio, data.type_time),
            pi.get_subset(error_bars_ratio,
                          data.type_count),
            "Unix time (s)", "Count rate ($s^{-1}$)",
            337,
            "none",
            yerr=pi.get_subset(error_bars_ratio, data.type_error)),

    # Plot weather data.
    Subplot(weather_times, w.get_pressures(weather),
            "Unix time (s)", "Pressure (mbar)", 332, "b.", label="Pressure"),

    Subplot(weather_times, w.get_temperatures(weather),
            "Unix time (s)", "Temperature (°C)", 333, "r.", label="Temperature"),

    Subplot(weather_times, w.get_humidity(weather),
            "Unix time (s)", "Relative humidity (percent)", 335, "g.", label="Humidity"),

    Subplot(weather_times, w.get_rainfall(weather),
            "Unix time (s)", "Rainfall (mm per 10 minutes)", 336, "y.", label="Rainfall"),

    Subplot(weather_times, w.get_solar_irradiation(weather),
            "Unix time (s)", "Solar irradiation ($kWm^{-2}$ avg 10 min)", 338, "c.", label="Solar irradiation"),
)

for s in subplots:
    plt.subplot(s.subplot_index)
    plt.errorbar(s.xvalues, s.yvalues, s.yerr, fmt=s.plot_appearance)
    plt.xlabel(s.xlabel)
    plt.ylabel(s.ylabel)
    plt.xlim(min_time, max_time)
    s.set_ylimits()
    s.legend()

figure = plt.gcf()
figure.set_size_inches(16, 12)
plt.savefig("all_muons_weather", dpi=200)
