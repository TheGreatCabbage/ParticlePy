from matplotlib import pyplot as pyplot
import weather as w

data = w.get_weather()
temp = w.get_temperatures(data)

mock_times = [10*i for i in range(0, len(temp))]

pyplot.plot(mock_times, temp, '.')
pyplot.show()
