import sys

# import ipdb
import pandas as pd

from PyQt5 import QtWidgets
import pyqtgraph as pg


class PlotApplication(QtWidgets.QMainWindow):

    """The main application."""

    data = None

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        """Create the user interface."""

        # Menubar
        menubar = self.menuBar()

        open_file_action = QtWidgets.QAction('&Open file', self)
        open_file_action.triggered.connect(self.open_file_dialog)

        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_action)

        # Main UI
        plot = pg.PlotWidget()

        self.setCentralWidget(plot)
        self.show()

    def open_file_dialog(self):
        """Dialog for opening a data file."""

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self)

        self.data = pd.read_csv(file_path)
        self.plot_data()

    def plot_data(self):
        """Plot the data in a graph."""

        pass


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)
    app = PlotApplication()

    qtapp.exec_()
