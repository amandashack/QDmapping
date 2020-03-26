import sys, os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from mainwindow import MainWindow
from signals import Signals
from context import Context
#from context import Context

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    signals = Signals()
    context = Context(signals)
    
    w = MainWindow(signals, context)
    w.show()
    sys.exit(app.exec())
