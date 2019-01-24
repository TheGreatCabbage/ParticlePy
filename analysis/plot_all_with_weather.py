import data
import math
from matplotlib import pyplot as plt
import weather as w

"""
Plot muons from all detectors separately, with weather.
"""

factor = 600


def mapper(datum):
    datum.set(data.type_count, datum.get(data.type_count)*factor)
    datum.set(data.type_error, math.sqrt(datum.get(data.type_count)))
    return datum


lab_set2 = data.get_lab_data_set2_600().map(mapper)
lab_set2_times = lab_set2.get(data.type_time)

lab_set3 = data.get_lab_data_set3_600().map(mapper)
lab_set3_times = lab_set3.get(data.type_time)

pi = data.get_data(data.file_pi_600).map(mapper)
weather = w.get_data()
weather_times = w.get_times(weather)

# Use these for x-limits, so all plots aligned.
min_time = min(lab_set2_times[0], pi.get(data.type_time)[0])
max_time = max(lab_set2_times[-1], pi.get(data.type_time)[-1])


class Subplot:
    """
    A data object to make many subplots simpler.
    """

    def __init__(self, xvalues, yvalues, xlabel, ylabel, subplot_index, plot_appearance=".", ylim=None, label=None, yerr=None, marker_size=4):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.subplot_index = subplot_index
        self.plot_appearance = plot_appearance
        self.ylim = ylim
        self.label = label
        self.yerr = yerr
        self.marker_size = marker_size

    def set_ylimits(self):
        if self.ylim and len(self.ylim) == 2:
            plt.ylim(self.ylim[0], self.ylim[1])

    def legend(self):
        """Set the legend, using the label specified in the constructor."""
        if self.label:
            plt.legend([self.label])


# The ratio of points plotted to error bars plotted.
error_bars_ratio = 1
unix_time_label = "Seconds since 01/01/1970, 00:00:00 UTC"
counts_label = "Counts per 10 minutes"
#counts_label = "Counts (10 min$^{-1}$)"

subplots = (
    # Counts for lab_set2 data.
    Subplot(lab_set2_times, lab_set2.get(data.type_count),
            unix_time_label, counts_label,
            421, ylim=(1, 6), label="Lab muon detector (set 2)",
            marker_size=1),

    # Error bars for lab_set2 data.
    Subplot(lab_set2.get_subset(error_bars_ratio, data.type_time),
            lab_set2.get_subset(error_bars_ratio,
                                data.type_count),
            unix_time_label, counts_label,
            421,
            "none",
            yerr=lab_set2.get_subset(error_bars_ratio, data.type_error),
            marker_size=1),

    Subplot(lab_set3_times, lab_set3.get(data.type_count),
            unix_time_label, counts_label,
            423, ylim=(1, 6), label="Lab muon detector (set 3)",
            marker_size=1),

    Subplot(lab_set3.get_subset(error_bars_ratio, data.type_time),
            lab_set3.get_subset(error_bars_ratio,
                                data.type_count),
            unix_time_label, counts_label,
            423,
            "none",
            yerr=lab_set3.get_subset(error_bars_ratio, data.type_error),
            marker_size=1),


    Subplot(pi.get(data.type_time), pi.get(data.type_count),
            unix_time_label, counts_label,
            425, ylim=(0, 1.2), label="Raspberry Pi muon detector",
            marker_size=1),

    Subplot(pi.get_subset(error_bars_ratio, data.type_time),
            pi.get_subset(error_bars_ratio,
                          data.type_count),
            unix_time_label, counts_label,
            425,
            "none",
            yerr=pi.get_subset(error_bars_ratio, data.type_error),
            marker_size=1),

    # Plot weather data.
    Subplot(weather_times, w.get_pressures(weather),
            unix_time_label, "Pressure (mbar)", 427, "b.", label="Pressure"),

    Subplot(weather_times, w.get_temperatures(weather),
            unix_time_label, "Temperature (°C)", 422, "r.", label="Temperature"),

    Subplot(weather_times, w.get_humidity(weather),
            unix_time_label, "Relative humidity (percent)", 424, "g.", label="Humidity"),

    Subplot(weather_times, w.get_rainfall(weather),
            unix_time_label, "Rainfall (mm per 10 minutes)", 426, "y.", label="Rainfall"),

    Subplot(weather_times, w.get_solar_irradiation(weather),
            unix_time_label, "Solar irradiation ($kWm^{-2}$ avg 10 min)", 428, "c.", label="Solar irradiation"),
)

for s in subplots:
    plt.subplot(s.subplot_index)
    plt.errorbar(s.xvalues, s.yvalues, s.yerr,
                 fmt=s.plot_appearance, markersize=s.marker_size)
    plt.xlabel(s.xlabel)
    plt.ylabel(s.ylabel)
    plt.xlim(min_time, max_time)
    # s.set_ylimits()
    s.legend()

figure = plt.gcf()
figure.set_size_inches(8.27*1.8, 11.69*1.4)
plt.savefig("all_muons_weather", dpi=200)
