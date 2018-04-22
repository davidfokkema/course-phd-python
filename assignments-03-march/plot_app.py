import pdb
import sys

from PyQt5 import QtWidgets, QtCore


class PlotApplication(QtWidgets.QMainWindow):

    """The main application."""

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        menubar = self.menuBar()

        open_file_action = QtWidgets.QAction('&Open file', self)
        open_file_action.triggered.connect(self.open_file_dialog)

        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_file_action)

        self.show()

    def open_file_dialog(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self)

        QtCore.pyqtRemoveInputHook()
        pdb.set_trace()
        QtCore.pyqtRestoreInputHook()
        

if __name__ == '__main__':
    qtapp = QtWidgets.QApplication(sys.argv)
    app = PlotApplication()

    qtapp.exec_()
