import muons
from matplotlib import pyplot as plot
import numpy as np

data = muons.get_data()
# plot.bar(muons.get_times_from(data), muons.get_counts_from(data))
plot.plot(muons.get_times_from(data), muons.get_counts_from(data))
plot.grid(True)
plot.show()
