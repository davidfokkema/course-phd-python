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

        # temporary code to speed up development
        self.data = pd.read_csv('data.csv')
        self.plot_data()

    def init_ui(self):
        """Create the user interface."""

        # Menubar
        menubar = self.menuBar()

        open_file_action = QtWidgets.QAction('&Open file', self)
        open_file_action.triggered.connect(self.open_file_dialog)

        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_action)

        # Main UI
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.plot = pg.PlotWidget()

        self.setCentralWidget(self.plot)
        self.show()

    def open_file_dialog(self):
        """Dialog for opening a data file."""

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self)

        self.data = pd.read_csv(file_path)
        self.plot_data()

    def plot_data(self):
        """Plot the data in a graph."""

        # Use a black pen and brush (fill)
        pen = pg.mkPen(width=3, color='k')
        brush = pg.mkBrush(color='k')

        # Plot the data, with errorbars
        self.plot.plot(self.data.x, self.data.y, pen=None, symbol='o',
                       symbolSize=7, symbolPen=None, symbolBrush=brush)
        errorbars = pg.ErrorBarItem(x=self.data.x, y=self.data.y,
                                    height=self.data.yerr, pen=pen)
        self.plot.addItem(errorbars)


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)
    app = PlotApplication()

    qtapp.exec_()
