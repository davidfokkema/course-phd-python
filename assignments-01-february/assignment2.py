import matplotlib.pyplot as plt
import time
import random
import numpy as np

xsample = np.linspace(0, 100, 100)
ysample = random.sample(range(-50, 50), 100)
xdata = []
ydata = []
plt.show()

# not necessary wth ipython --pylab
#plt.ion()

axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(-50, +50)

for x, y in zip(xsample, ysample):
    xdata.append(x)
    ydata.append(y)
    line, = axes.plot(xdata, ydata, 'r-') #note the comma after line!!!
    plt.pause(.1)
