"""Fake data acquisition application."""

import multiprocessing
import sys

from PyQt5 import QtWidgets
import pyqtgraph as pg

from fake_daq import DataAcquistion


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
