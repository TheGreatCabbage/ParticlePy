import matplotlib.pyplot as plt
import muons as mu
import numpy as np
import weather as w
import pi_muons as pi
import sys

weather = w.get_data()
pressures = w.get_pressures(weather)
weather_times = w.get_times(weather)

muons = mu.get_data()
muon_times = mu.get_times_from(muons)
muon_counts = mu.get_counts_from(muons)

