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

#  what does using the word "Object" do
# can you reinstantiate self.ogImage

class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)#QtCore.QRectF(-500, -500, 1000, 1000), parent)
        self._start = QtCore.QPointF()
        self._current_rect_item = None

    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QtGui.QTransform()) is None:
            self._current_rect_item = QtWidgets.QGraphicsRectItem()
            self._current_rect_item.setBrush(QtCore.Qt.red)
            self._current_rect_item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_rect_item)
            self._start = event.scenePos()
            r = QtCore.QRectF(self._start, self._start)
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None:
            r = QtCore.QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._current_rect_item = None
        super(GraphicsScene, self).mouseReleaseEvent(event)

class Action(QGraphicsView):
    rectChanged = pyqtSignal(QRect)
    
    def __init__(self, ogImage, ogImageScene): #send in ogImage
        QGraphicsView.__init__(self) # this makes an instance of QGraphicsView
        self.ogImage = ogImage
        self.ogImageScene = ogImageScene
        self.ogImage.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True) #see what happens if this is set to False
        self.origin = QPoint()
        self.changeRubberBand = False
    
    def mousePressEvent(self, event):
        self.ogImage.origin = event.pos()
        self.ogImage.rubberBand = QRubberBand(QRubberBand.rectangle, self)
        self.ogImage.setMouseTracking(True)
        self.ogImage.origin = QPoint()
        self.ogImage.changeRubberBand = False
    def mouseMoveEvent(self, event):
        if self.ogImage.changeRubberBand:
            self.ogImage.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.ogImage.rectChanged.emit(self.ogImage.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)
    def mouseReleaseEvent(self, event):
        self.ogImage.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self, event)
    

class GraphicsView(QGraphicsView):
    rectChanged = pyqtSignal(QRect)

    def __init__(self, *args, **kwargs):
        QGraphicsView.__init__(self, *args, **kwargs)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QtCore.QSize()))
        self.rectChanged.emit(self.ogImage.rubberBand.geometry())
        self.rubberBand.show()
        self.changeRubberBand = True
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self, event)

class photoViewer(object):
    def __init__(self, ogImage, ogImageScene, width, height):
        self.ogImage = ogImage
        self.ogImageScene = ogImageScene
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
        self.ogImageScene.addPixmap(pixmap)
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