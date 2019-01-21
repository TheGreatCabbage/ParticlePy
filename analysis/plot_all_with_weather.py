import data
from matplotlib import pyplot as plt

"""
Plot muons from all detectors separately, with weather.
"""

lab_set2 = data.get_lab_data_set2_3600()
lab_set3 = data.get_lab_data_set3_3600()
pi = data.get_data(data.file_pi_3600)

# Use these for x-limits, so all plots aligned.
min_time = min(lab_set2.get(data.type_time)[0], pi.get(data.type_time)[0])
max_time = max(lab_set2.get(data.type_time)[-1], pi.get(data.type_time)[-1])


class Subplot:
    """
    A data object to make many subplots simpler.
    """

    def __init__(self, xvalues, yvalues, xlabel, ylabel, subplot_index, plot_appearance=".", ylim=None, label=None):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.subplot_index = subplot_index
        self.plot_appearance = plot_appearance
        self.ylim = ylim
        self.label = label

    def set_ylimits(self):
        if self.ylim and len(self.ylim) == 2:
            plt.ylim(self.ylim[0], self.ylim[1])

    def legend(self):
        """Set the legend, using the label specified in the constructor."""
        if self.label:
            plt.legend([self.label])


subplots = (
    Subplot(lab_set2.get(data.type_time), lab_set2.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 331, ylim=(2.6, 4.1), label="Lab muon detector (set 2)"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 334, ylim=(2.6, 4.1), label="Lab muon detector (set 3)"),
    Subplot(pi.get(data.type_time), pi.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 337, ylim=(0.16, 0.42), label="Raspberry Pi muon detector"),

    # Plot weather from set 2 and set 3 on same subplot to fill in gaps where one detector is not running.
    Subplot(lab_set2.get(data.type_time), lab_set2.get(data.type_pressure),
            "Unix time (s)", "Pressure (mbar)", 332, "b.", label="Pressure"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(data.type_pressure),
            "Unix time (s)", "Pressure (mbar)", 332, "b."),

    Subplot(lab_set2.get(data.type_time), lab_set2.get(data.type_temperature),
            "Unix time (s)", "Temperature (°C)", 333, "r.", label="Temperature"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(data.type_temperature),
            "Unix time (s)", "Temperature (°C)", 333, "r."),

    Subplot(lab_set2.get(data.type_time), lab_set2.get(data.type_humidity),
            "Unix time (s)", "Relative humidity (percent)", 335, "g.", label="Humidity"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(data.type_humidity),
            "Unix time (s)", "Relative humidity (percent)", 335, "g."),

    Subplot(lab_set2.get(data.type_time), lab_set2.get(data.type_rainfall),
            "Unix time (s)", "Rainfall (mm per 10 minutes)", 336, "y.", label="Rainfall"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(data.type_rainfall),
            "Unix time (s)", "Rainfall (mm per 10 minutes)", 336, "y."),

    Subplot(lab_set2.get(data.type_time), lab_set2.get(data.type_solar_irradiation),
            "Unix time (s)", "Solar irradiation (kW/m2 avg 10 min)", 338, "c.", label="Solar irradiation"),
    Subplot(lab_set3.get(data.type_time), lab_set3.get(data.type_solar_irradiation),
            "Unix time (s)", "Solar irradiation (kW/m2 avg 10 min)", 338, "c.")
)

for s in subplots:
    plt.subplot(s.subplot_index)
    plt.plot(s.xvalues, s.yvalues,  s.plot_appearance)
    plt.xlabel(s.xlabel)
    plt.ylabel(s.ylabel)
    plt.xlim(min_time, max_time)
    s.set_ylimits()
    s.legend()

plt.show()
