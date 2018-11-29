import muons
from matplotlib import pyplot as plot
import numpy as np

data = muons.get_data()
# plot.bar(muons.get_times_from(data), muons.get_counts_from(data))

x = muons.sorted_data_from(data)
d = x
# d = (x[0][:10000], x[1][:10000])

# TODO: check if this is correctly replaced by muons.average_with_step().
# tempAverage = [[], []]
# times = d[0][:10000]
# values = d[1][:10000]
# for i in range(100):
#     tempAverage[0].append(times[0+100*i])
# for temp1 in range(100):
#     temp = sum(values[100*temp1:100*(temp1+1)-1])/100
#     tempAverage[1].append(temp)
# plot.plot(tempAverage[0], tempAverage[1], '.')

d = muons.average_with_step(d, 1000)
plot.plot(d[0], d[1], '.')

plot.grid(True)
plot.show()
