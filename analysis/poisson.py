import pi_muons as mu
import math
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

counts = mu.get_counts()
diffs = []
num_counts = len(counts)

for i in range(0, num_counts):
    if i >= num_counts-1:  # Reached last value to find differences for.
        break
    diffs.append(counts[i+1] - counts[i])


def poisson(x, l): return math.log(l * math.exp(-l*x), math.e)
def ln(x): return math.log(x, math.e)
# popt, pcov = curve_fit(poisson, diffs, )

factor = 0.1
hist, bins = np.histogram(diffs, bins=[i * factor for i in range(0, int(50 / factor))])
midpoints = bins[:-1] + factor/2
logs = [ln(i) for i in hist]

plt.plot(midpoints, logs, ".")
plt.show()
