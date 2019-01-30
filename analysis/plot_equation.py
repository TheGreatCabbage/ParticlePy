import data
from matplotlib import pyplot as plt
import muons as mu
import numpy as np
from scipy import stats
import weather as w

"""
Plots (I-I_0)/I_0 against X-X_0 for X=pressure and X=temperature 
for all muon detectors.
"""

xlabel_temp = "$T-T_0$ (°C)"
xlabel_pressure = "$P-P_0$ (millibar)"
ylabel = "$\\frac{I-I_0}{I_0}$"

data_tuples = (
    # (Data over 10-minute intervals, subplot index, plot label)
    (data.get_lab_data_set2_600(), 321, "Set 2"),
    (data.get_lab_data_set3_600(), 323, "Set 3"),
    (data.get_pi_data(), 325, "Raspberry Pi"),
)


def lhs(var, mean):
    """LHS of the equation."""
    return (var-mean)/mean


def rhs(var, mean):
    """RHS of the equation."""
    return var-mean


def plot(subplot, x, y, label=None, xlabel=None):
    plt.subplot(subplot)
    plt.plot(x, y, ".", ms=4)

    plt.legend([label])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Get best fit parameters and plot it.
    slope, intercept, r, p, err = stats.linregress(x, y)
    plt.plot(x, slope * np.array(x) + intercept)

    print("{} ({}): \nGradient = {}\nError = {}\nCorrelation = {}\n".format(
        label, "pressure" if subplot % 2 == 0 else "temperature", slope, err, r))


for d in data_tuples:
    data_obj = d[0]

    counts = data_obj.get(data.type_count)
    pressures = data_obj.get(data.type_pressure)
    temperatures = data_obj.get(data.type_temperature)

    avg_count = np.mean(counts)
    avg_pressure = np.mean(pressures)
    avg_temperature = np.mean(temperatures)

    y = [lhs(i, avg_count) for i in counts]

    # Plot temperature.
    plot(d[1], [rhs(i, avg_temperature) for i in temperatures],
         y, d[2], xlabel_temp)
    # Plot pressure.         
    plot(d[1]+1, [rhs(i, avg_pressure) for i in pressures],
         y, d[2], xlabel_pressure)

plt.show()
