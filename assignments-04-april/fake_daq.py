"""Fake data acquisition application."""

import multiprocessing
import random
import sys
import time

import numpy as np

from PyQt5 import QtWidgets
import pyqtgraph as pg


class DataAcquistion(multiprocessing.Process):

    """Fake data acquisition processself.

    This process will inject fake data into a queueself.

    """

    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = queue

    def run(self):
        while True:
            time.sleep(random.uniform(0, 1))

            x = np.arange(0, 3e-6, 2.5e-9)
            y = np.random.normal(size=x.shape)

            self.queue.put({'x': x, 'y': y})


class UserInterface(QtWidgets.QWidget):

    def __init__(self, queue):
        super().__init__()

        self.queue = queue
        self.init_ui()

    def run(self):
        while True:
            data = self.queue.get()
            print(data)

    def init_ui(self):
        """Create the user interface."""

        # Main UI components
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.plot = pg.PlotWidget()

        # UI Layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.plot, 0, 0)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)

    queue = multiprocessing.Queue()
    daq = DataAcquistion(queue)
    ui = UserInterface(queue)

    daq.start()
    qtapp.exec_()
