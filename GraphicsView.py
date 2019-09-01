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
import cv2

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

class photoManager():
    def __init__(self):
        pass

    def editIm(self, editim, cur_mode, value):

        im = editim
        
        if cur_mode.upper() in ["DILATE", "CLOSE", "TOPHAT"]:

            str_mode = 'ellipse'
            # sz, iters, op = trackbar(im, cur_mode, str_mode) #send in im so you can deal with a smaller size image
            str_name = 'MORPH_' + str_mode.upper()
            oper_name = 'MORPH_' + cur_mode.upper()
            st = cv2.getStructuringElement(getattr(cv2, str_name), (2, 2))
            #im = cv2.morphologyEx(im, getattr(cv2, oper_name), st, iterations=value)
            editim = cv2.morphologyEx(editim, getattr(cv2, oper_name), st, iterations = value) #actually change full size image
            

        elif cur_mode.upper() == "BLUR":

            editim = cv2.GaussianBlur(im, (3, 3), value)

            
        elif cur_mode.upper() == "THRESHOLD":
            print("I am here")
            editim = cv2.adaptiveThreshold(im, 255,  cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, value-7)
            
        return(editim)

    def zoomByRect(self, editim, areaView): #QRect - x, y, width, height
        
        rect_scene = self.mapToScene(areaView).boundingRect()
        selected = self.scene().items(rect_scene)
