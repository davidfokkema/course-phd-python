"""Data acquisition application.

   This is a very simple Qt application demonstrating a data acquisition setup.
   The DAQ runs in a separate process, supervised by a dedicated thread in the
   Qt app.

   To run this script, you need to have a few packages installed (PyQt5, numpy
   and pyqtgraph). Not all packages are included in the main conda channel, but
   you can simply add the conda-forge channel. Create a conda environment for
   this app:

      $ conda config --add channels conda-forge
      $ conda create -n daq python=3 numpy pyqt pyqtgraph

   On MacOS/Linux:

      $ source activate daq

   On Windows:

      $ activate daq

   Then run the application:

      $ python daq_gui.py

"""

import multiprocessing
import sys
import signal
import threading

from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg

from fake_daq import DataAcquistion


class UserInterface(QtWidgets.QWidget):

    """Graphical user interface for the data acquisition application."""

    def __init__(self):
        super().__init__()

        self.must_shutdown = threading.Event()

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

        self.daq_worker = DAQWorker(self.must_shutdown)
        self.daq_thread = QtCore.QThread()
        self.daq_worker.moveToThread(self.daq_thread)
        self.daq_worker.new_data_signal.connect(self.plot_data)
        self.daq_thread.started.connect(self.daq_worker.run)

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

    def closeEvent(self, event):
        """Close the application.

        This method is called whenever a close event is triggered. We need to
        stop the DAQ process.

        """
        self.stop_daq()

    def start_daq(self):
        """Start the DAQ process."""
        self.daq_thread.start()

    def stop_daq(self):
        """Stop the DAQ process."""

        # signal the DAQ worker to shutdown
        self.must_shutdown.set()
        # quit and wait for the DAQ thread to shutdown
        self.daq_thread.quit()
        self.daq_thread.wait()

    @QtCore.pyqtSlot(dict)
    def plot_data(self, data):
        """Plot the event data."""

        self.plot.clear()
        self.plot.plot(data['x'] * 1e9, data['y'], pen='k')
        self.plot.setLabels(title='Scintillator event', bottom='Time [ns]',
                            left='Signal [mV]')
        self.plot.setYRange(0, -500)


class DAQWorker(QtCore.QObject):

    """Worker thread to manage the data acquisition process."""

    new_data_signal = QtCore.pyqtSignal(dict)

    def __init__(self, must_shutdown, **kwargs):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        super().__init__(**kwargs)
        self.must_shutdown = must_shutdown

    @QtCore.pyqtSlot()
    def run(self):
        """Run the DAQ and process incoming data."""

        queue = multiprocessing.Queue()
        daq_shutdown = multiprocessing.Event()
        daq = DataAcquistion(queue, daq_shutdown)

        daq.start()

        while not self.must_shutdown.is_set():
            data = queue.get()
            self.new_data_signal.emit(data)

        print("DAQ shutting down...")
        daq_shutdown.set()
        daq.join()
        print("Done.")


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)

    ui = UserInterface()

    qtapp.exec_()
