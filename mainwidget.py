from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import sys
import math
import cv2
import qimage2ndarray as qi
from collections import defaultdict

from GraphicsView import *
from fftpop import *


class myApp2(QWidget, photoManager):
    def __init__(self, parent=None):
        super(myApp2, self).__init__(parent)
        
        self.setWindowTitle("selecting")
        self.initUI()
    
    def initUI(self):
        # TODO - add reset button

        grid = QGridLayout()
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(50)
        

        
        self.drawView = QGraphicsView(self)
        self.view = GraphicsView(self.drawView, self)
        self.drawView.setMouseTracking(True)
        self.view.setMouseTracking(True)
        self.rd = rdButton(self.view)
        

        self.editDict = defaultdict(list)

        # TODO - add a radiobutton to have a slider turned on and off
        self.lbl1 = QLabel()
        self.lbl1.setText("erode")
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.sl1 = QSlider(Qt.Horizontal)
        self.sl1.setObjectName("erode")
        self.sl1.setMinimum(0)
        self.sl1.setMaximum(10)
        self.sl1.setValue(1)
        self.sl1.setTickPosition(QSlider.TicksBelow)
        self.sl1.setTickInterval(1)

        self.lbl2 = QLabel()
        self.lbl2.setText("open")
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setObjectName('open')
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(10)
        self.sl2.setValue(1)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(1)

        self.lbl3 = QLabel()
        self.lbl3.setText("blackhat")
        self.lbl3.setAlignment(Qt.AlignCenter)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setObjectName('blackhat')
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(10)
        self.sl3.setValue(1)
        self.sl3.setTickPosition(QSlider.TicksBelow)
        self.sl3.setTickInterval(1)

        self.lbl4 = QLabel()
        self.lbl4.setText("tophat")
        self.lbl4.setAlignment(Qt.AlignCenter)
        self.sl4 = QSlider(Qt.Horizontal)
        self.sl4.setObjectName('tophat')
        self.sl4.setMinimum(0)
        self.sl4.setMaximum(10)
        self.sl4.setValue(1)
        self.sl4.setTickPosition(QSlider.TicksBelow)
        self.sl4.setTickInterval(1)


        self.lbl5 = QLabel()
        self.lbl5.setText("close")
        self.lbl5.setAlignment(Qt.AlignCenter)
        self.sl5 = QSlider(Qt.Horizontal)
        self.sl5.setObjectName('close')
        self.sl5.setMinimum(0)
        self.sl5.setMaximum(10)
        self.sl5.setValue(1)
        self.sl5.setTickPosition(QSlider.TicksBelow)
        self.sl5.setTickInterval(1)


        self.lbl6 = QLabel()
        self.lbl6.setText("dilate")
        self.lbl6.setAlignment(Qt.AlignCenter)
        self.sl6 = QSlider(Qt.Horizontal)
        self.sl6.setObjectName('dilate')
        self.sl6.setMinimum(0)
        self.sl6.setMaximum(10)
        self.sl6.setValue(1)
        self.sl6.setTickPosition(QSlider.TicksBelow)
        self.sl6.setTickInterval(1)


        
        grid.addWidget(self.view, 0, 0, -1, 15)
        grid.addWidget(self.drawView, 0, 14, -1, 15)
        grid.addWidget(self.rd, 0, 29, 1, 3)
        grid.addWidget(self.lbl1, 1, 29, 1, 3)
        grid.addWidget(self.sl1, 2, 29, 1, 3)
        grid.addWidget(self.lbl6, 3, 29, 1, 3)
        grid.addWidget(self.sl6, 4, 29, 1, 3)
        grid.addWidget(self.lbl2, 5, 29, 1, 3)
        grid.addWidget(self.sl2, 6, 29, 1, 3)
        grid.addWidget(self.lbl5, 7, 29, 1, 3)
        grid.addWidget(self.sl5, 8, 29, 1, 3)
        grid.addWidget(self.lbl3, 9, 29, 1, 3)
        grid.addWidget(self.sl3, 10, 29, 1, 3)
        grid.addWidget(self.lbl4, 11, 29, 1, 3)
        grid.addWidget(self.sl4, 12, 29, 1, 3)

        self.setLayout(grid)

        self.sl1.valueChanged.connect(self.valuechange)
        self.sl2.valueChanged.connect(self.valuechange)
        self.sl3.valueChanged.connect(self.valuechange)
        self.sl4.valueChanged.connect(self.valuechange)
        self.sl5.valueChanged.connect(self.valuechange)
        self.sl6.valueChanged.connect(self.valuechange)




    def connectRB(self):
        return(self.rd._button_group.checkedId())

    def setImage(self):
        self.view.setImage()
  

    def valuechange(self):

        
        sender = self.sender()

        if sender.objectName() in self.editDict:
            pass
        else:
            self.editDict[sender.objectName()] = []

        self.imageEdit = self.editIm(self.view.cvogImageBW, self.editDict, sender.objectName(), sender.value())
         
        self.imageEdit = QImage(self.imageEdit, self.imageEdit.shape[1], self.imageEdit.shape[0], QImage.Format_Grayscale8)
        
        self.pixmap = QPixmap(self.imageEdit)
        
        width = self.view.imageScaled.width()
        height = self.view.imageScaled.height()
        self.pixmap = self.pixmap.scaled(width, height, Qt.KeepAspectRatio)
        
        self.view.scene().clear()
        self.pixmapItem = QGraphicsPixmapItem()
        self.view.scene().addItem(self.pixmapItem)
        self.pixmapItem.setPixmap(self.pixmap)
  
    
    def updatePixmap(self, pixmap):
        self.view.pixmapItem.setPixmap(pixmap)
