import matplotlib.pyplot as plt
import time
import random

ysample = random.sample(range(-50, 50), 100)
xdata = []
ydata = []
plt.show()

axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(-50, +50)
line, = axes.plot(xdata, ydata, 'r-') #note the comma after line!!!
maxt = 100
