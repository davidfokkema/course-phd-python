import sys

# import ipdb
import numpy as np
import pandas as pd
from lmfit import models

from PyQt5 import QtWidgets
import pyqtgraph as pg


class PlotApplication(QtWidgets.QWidget):

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
        menubar = QtWidgets.QMenuBar()

        open_file_action = QtWidgets.QAction('&Open file', self)
        open_file_action.triggered.connect(self.open_file_dialog)

        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_action)

        # Main UI components
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.plot = pg.PlotWidget()

        self.text = QtWidgets.QPlainTextEdit(readOnly=True)
        self.button = QtWidgets.QPushButton('Fit linear model')
        self.button.clicked.connect(self.fit_linear_model)

        # UI Layout
        layout = QtWidgets.QGridLayout()
        layout.setMenuBar(menubar)
        layout.addWidget(self.plot, 0, 0)
        layout.addWidget(self.text, 0, 1)
        layout.addWidget(self.button, 1, 1)

        self.setLayout(layout)
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

    def fit_linear_model(self):
        """Fit a linear model to the data."""

        data = self.data
        model = models.LinearModel()
        fit = model.fit(data.y, x=data.x, weights=1 / data.yerr)

        self.text.setPlainText(fit.fit_report())

        x = np.linspace(data.x.min(), data.x.max())
        self.plot.plot(x, fit.eval(x=x), pen={'color': 'r'})


if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)
    app = PlotApplication()

    qtapp.exec_()
