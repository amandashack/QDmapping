from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time

class mainWidget(QWidget):

    def __init__(self, signals, Parent = None):
        super(mainWidget, self).__init__(Parent)

        
        self.signals = signals
        self.parent = Parent

        self.signals.newImage.connect(self.setImage)
    
    def newImage(self):
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
