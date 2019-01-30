import matplotlib.pyplot as plt
import muons as mu
import numpy as np
import pi_muons as pi
import sys

muons2 = mu.average_with_step(mu.get_data_set_2(), 600*6)
muons3 = mu.average_with_step(mu.get_data_set_3(), 600*6)

id = 311
subplots = [] 
start = min(muons2[0][0], muons3[0][1])
end = min(muons2[0][-1], muons3[0][-1])

for m in (muons2, muons3):
    x = m[0]
    y = m[1]
    s = plt.subplot(id)
    s.set_ylim(2.5, 4.1)

    plt.plot(x,y, "b.", label="Set {}".format(str(id + 1)[-1]))
    plt.legend()
    subplots.append(s)
    id += 1

pi_data = pi.get_counts()
pi_counts = pi.get_counts_in_time(pi_data, 600)
s = plt.subplot(id)
plt.plot(pi_counts[0], pi_counts[1], "k.", label="RPi muons")
plt.legend()
subplots.append(s)

for s in subplots:
    s.set_xlim(start, end)

plt.show()