from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QRubberBand
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import *
from GraphicsView import *
import sys
import time

class photoViewer(object):
    def __init__(self, ogImage, ogImageScene, pixmapItem, width, height):
        self.ogImage = ogImage
        self.ogImageScene = ogImageScene
        self.pixmapItem = pixmapItem
        self._zoom = 0
        self._width = width
        self._height = height

    def setDefaultImage(self, image):
        self.image = image
        pixmap = self.scale(self._width, self._height)
        self.updatePixmap(pixmap)
        return(pixmap)

    def updatePixmap(self, pixmap):
        self.ogImageScene.clear()
        self.pixmapItem = QGraphicsPixmapItem()
        self.pixmapItem.setPixmap(pixmap)
        self.ogImageScene.addItem(self.pixmapItem)
        self.ogImageScene.setSceneRect(QtCore.QRectF(0.0, 0.0, pixmap.width(), pixmap.height()))

    def scale(self, width, height):
        if (self.image.isNull()):
            return(QPixmap())
        return(self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def zoom(self, pixmap, factor):
        pixmap = self.scale(pixmap.width()*factor, pixmap.height()*factor)
        self.updatePixmap(pixmap)
        return(pixmap)
        
    def zoomIn(self, pixmap):
        self._zoom += 1
        factor = 1.25
        return(self.zoom(pixmap, factor))
    
    def zoomOut(self, pixmap):
        if self._zoom == 0:
            return(pixmap)
        self._zoom -= 1
        factor = 0.75
        return(self.zoom(pixmap, factor))
    
    def zeroZoom(self, pixmap):
        if self._zoom == 0:
            return(pixmap)
        pixmap = self.scale(self._width, self._height) #### self.pixmap is used for scaling and anything else
        self.updatePixmap(pixmap)
        return (pixmap)

