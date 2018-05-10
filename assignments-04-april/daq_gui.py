"""Fake data acquisition application."""

import multiprocessing
import sys
import time
import threading

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from fake_daq import DataAcquistion


class UserInterface(QtWidgets.QWidget):

    def __init__(self, queue):
        super().__init__()

        self.queue = queue
        self.init_worker()
        self.init_ui()
        self.start_daq()

    def init_worker(self):
        """Setup the worker thread.

        First, instantiate the worker and a QThread. Then, make sure the worker
        will run in a thread managed by the QThread by calling the
        :meth:`QObject.moveToThread` method. Finally, attach the `started`
        signal to the `run` slot on the worker, so that the worker will
        actually start.

        """

        self.daq_worker = DAQWorker(self.queue)
        self.daq_thread = QtCore.QThread()
        self.daq_worker.moveToThread(self.daq_thread)
        self.daq_worker.new_data_signal.connect(self.plot_data)
        self.daq_thread.started.connect(self.daq_worker.run)
        self.daq_worker.second_signal.connect(self.daq_worker.second)

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

    def start_daq(self):
        self.daq_thread.start()

    def stop_daq(self):
        self.daq_thread.stop()

    @QtCore.pyqtSlot(dict)
    def plot_data(self, data):
        self.plot.clear()
        self.plot.plot(data['x'], data['y'])

        print("GUI:", threading.currentThread().getName())

        self.daq_worker.second_signal.emit()


class DAQWorker(QtCore.QObject):

    new_data_signal = QtCore.pyqtSignal(dict)
    second_signal = QtCore.pyqtSignal()

    def __init__(self, queue, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue

    @QtCore.pyqtSlot()
    def run(self):
        daq = DataAcquistion(self.queue)
        daq.start()

        # while True:
        data = self.queue.get()
        self.new_data_signal.emit(data)

        print("GUI worker:", threading.currentThread().getName())

    @QtCore.pyqtSlot()
    def second(self):
        print("Second")


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)

    queue = multiprocessing.Queue()
    ui = UserInterface(queue)

    qtapp.exec_()
