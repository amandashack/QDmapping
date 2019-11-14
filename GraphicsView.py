from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, QRect
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QRubberBand
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import *
from GraphicsView import *
from collections import defaultdict
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

    def editIm(self, editim, opDict, cur_mode, value):
        '''
        the problem is that the image is edited to include the previous state of the image AND THEN the current position of the slider is taken into account
        ~ this must be done beforehand so that the current state of the image is created from the slider + the previously moved sliders

        I believe this has been fixed and the below commented out code can be removed - 10/16
        '''

        im = editim
        
        opDict[cur_mode].append(value)

        for key in opDict.keys():
            if key.upper() == "ERODE":

                value = opDict[key][-1]
                
                kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
                editim = cv2.erode(editim, kernal, iterations = value) 

            elif key.upper() == "DILATE":

                value = opDict[key][-1]
                
                kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
                editim = cv2.erode(editim, kernal, iterations = value)

            elif key.upper() in ["OPEN", "CLOSE", "TOPHAT", "BLACKHAT"] and opDict[key]:
                
                key_value = opDict[key][-1]

                str_mode = 'ellipse'
                str_name = f'MORPH_{str_mode.upper()}'
                oper_name = f'MORPH_{key.upper()}'

                st = cv2.getStructuringElement(getattr(cv2, str_name), (2, 2))
                editim = cv2.morphologyEx(editim, getattr(cv2, oper_name), st, iterations = key_value)

            elif key.upper() == "BLUR" and opDict[key]:
                
                key_value = opDict[key][-1]
                editim = cv2.GaussianBlur(editim, (3, 3), key_value)

            elif key.upper() == "THRESHOLD" and opDict[key]:
                
                key_value = opDict[key][-1]
                #### types of thresholding
                #### Threshold binary or binary inverted: if the intensity of the pixel is higher than the thresh, 
                ####        Then the thresh is set to a MaxVal, otherwise the pixels are set to 0
                #### truncate : the maxiumum intensity value for the pixels is thresh, if the intensity of a pixel
                ####        value is greater, then its value is truncated (set to the MaxVal)
                #### threshold to zero or inverted: if the intensity of the pixel value is lower than the thresh,
                ####        then the new pixe value is zero or vice versa - I believe the other possible option is the TOZERO option
                ####        cv2.threshold(src, dst, *150*, 200, cv.THRESH_TOZERO) where the stared entry is the threshold and the value which would be the slider
                #### adaptive thresholding: calculates the threshold for small regions of an image for when there are
                #### different shadows
                editim = cv2.adaptiveThreshold(editim, 255,  cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, key_value - 7)
            
            else: print('you have a wrong key on line 96 in graphicsview.py')
 

        return(editim)

    def zoomByRect(self, editim, areaView): #QRect - x, y, width, height
        
        rect_scene = self.mapToScene(areaView).boundingRect()
        selected = self.scene().items(rect_scene)
