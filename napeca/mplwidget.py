"""# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------

Adapted from : https://yapayzekalabs.blogspot.com/2018/11/pyqt5-gui-qt-designer-matplotlib.html


"""
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvas

from matplotlib.figure import Figure


class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)