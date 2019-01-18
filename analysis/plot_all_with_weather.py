import data
from matplotlib import pyplot as plt

lab_set2 = data.get_lab_data_set2_3600()
lab_set3 = data.get_lab_data_set3_3600()
pi = data.get_data(data.file_pi_3600)

min_time = min(lab_set2.get(data.type_time)[0], pi.get(data.type_time)[0])
max_time = max(lab_set2.get(data.type_time)[-1], pi.get(data.type_time)[-1])


class Plot:

    def __init__(self, xvalues, yvalues, xlabel, ylabel, subplot_index, plot_appearance="."):
        self.xvalues = xvalues
        self.yvalues = yvalues
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.subplot_index = subplot_index
        self.plot_appearance = plot_appearance


subplots = (
    Plot(lab_set2.get(data.type_time), lab_set2.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 331),
    Plot(lab_set3.get(data.type_time), lab_set3.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 334),
    Plot(pi.get(data.type_time), pi.get(
        data.type_count), "Unix time (s)", "Count rate (1/s)", 337),
    Plot(lab_set2.get(data.type_time), lab_set2.get(data.type_pressure),
         "Unix time (s)", "Pressure (???)", 332, "b."),
    Plot(lab_set3.get(data.type_time), lab_set3.get(data.type_pressure),
         "Unix time (s)", "Pressure (???)", 332, "b."),
    Plot(lab_set2.get(data.type_time), lab_set2.get(data.type_temperature),
         "Unix time (s)", "Temperature (???)", 333, "r."),
    Plot(lab_set2.get(data.type_time), lab_set2.get(data.type_humidity),
         "Unix time (s)", "Humidity (???)", 335, "g."),
    Plot(lab_set3.get(data.type_time), lab_set3.get(data.type_humidity),
         "Unix time (s)", "Humidity (???)", 335, "g.")

)

for p in subplots:
    plt.subplot(p.subplot_index)
    plt.plot(p.xvalues, p.yvalues,  p.plot_appearance)
    plt.xlabel(p.xlabel)
    plt.ylabel(p.ylabel)
    plt.xlim(min_time, max_time)

plt.show()
