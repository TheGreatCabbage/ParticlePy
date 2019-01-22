from matplotlib import pyplot as plt
import muons as mu
import numpy as np
import pi_muons as pi


def divide(data1, data2):
    """
    Divides the counts of data1 by the counts of data2 and 
    returns tuple containing two numpy arrays (times, counts).
    """
    times, counts = [], []

    dict1 = create_dict(data1)
    dict2 = create_dict(data2)

    for key, value1 in dict1.items():
        value2 = dict2.get(key)
        if value2:
            times.append(key)
            counts.append(value1 / value2)
    return np.array(times), np.array(counts)


def create_dict(data):
    d = {}
    for i in range(0, len(data[0])):
        d[data[0][i]] = data[1][i]
    return d


set2 = mu.get_data_set_2()
set3 = mu.get_data_set_3()

n_mean = 2000
ratio_2_3 = divide(set2, set3)
size = len(ratio_2_3[0])


def max_index(): return n_mean * (size//n_mean)


x = ratio_2_3[0][:max_index()]
y = ratio_2_3[1][:max_index()]

plt.plot(np.mean(x.reshape(-1, n_mean), axis=1),
         np.mean(y.reshape(-1, n_mean), axis=1), ".")
plt.show()
