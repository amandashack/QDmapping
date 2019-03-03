from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import Ui_MainWindow
import sys
import time


class MyApp(QMainWindow, Ui_MainWindow):

    #parse_triggered = pyqtSignal()

    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent=parent)
        self.setupUi(self)
        self.ogImageScene = QGraphicsScene()
        self.imageMapScene = QGraphicsScene()
        # self.image = QPixmap()
        # self.pixmap = QPixmap()
        # #self.editMap = imageMapping(self.pixmap, self.imageMap, self.imageMapScene, self.ogImage, self.ogImageScene)
        
        # #self.action = Action(self.pixmap)
        # self.viewer = photoViewer(self.ogImage, self.ogImageScene)
        
        # self.actionZoom_In.triggered.connect(self.handleZoomIn)
        # self.actionOpen.triggered.connect(self.setImage)
        
        #self.actionUndo.triggered.connect(self.handleUndo)
        
        # self.drawing = False
        # self.lastPoint = QtCore.QPoint()
        
        #self.mousePressEvent(self, event)
        #self.ogImageScene.mouseMoveEvent = self.mouseMoveEvent(self, event)
        #self.ogImageScene.mouseReleaseEvent = self.mouseReleaseEvent(self, event)
        #self.pixmap.paintEvent = self.paintEvent(self, event)    


        self.image = QPixmap()
        self.pixmap = QPixmap()
        self.viewer = photoViewer(self.ogImage, self.ogImageScene, 600, 600)
        self.actionOpen.triggered.connect(self.setImage)
        self.actionZoom_In.triggered.connect(self.handleZoomIn)
        self.actionZoom_Out.triggered.connect(self.handleZoomOut)
        self.actionNormal_Size.triggered.connect(self.handleNormalSize)
        
        #self.ogImage.mousePressEvent = drawingTool.mousePressEvent(self, event)
        #self.ogImage.mouseMoveEvent = drawingTool.mouseMoveEvent(self, event)
        #self.ogImage.mouseReleaseEvent = drawingTool.mouseReleaseEvent(self, event)
        #self.ogImage.paintEvent = drawingTool.paintEvent(self, event)
        
        self.drawing = False
        self.lastPoint = QPoint()
    
    def setImage(self):
         
         fileName, _ = QFileDialog.getOpenFileName(None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp)")
         if fileName:
             self.image = QPixmap(fileName) ###### self.image holds the original image at all times
             self.pixmap = self.viewer.setDefaultImage(self.image)
             
             

    def handleZoomIn(self):
        self.pixmap = self.viewer.zoomIn(self.pixmap)
    
    def handleZoomOut(self):
        self.pixmap = self.viewer.zoomOut(self.pixmap)
    
    def handleNormalSize(self):
        self.pixmap = self.viewer.zeroZoom(self.pixmap)

             
        

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
        self.ogImageScene.setSceneRect(QRectF(0.0, 0.0, pixmap.width(), pixmap.height()))

    def scale(self, width, height):
        if (self.image.isNull()):
            return(QPixmap())
        return(self.image.scaled(width, height, Qt.KeepAspectRatio))

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


import resource

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MyApp()
    MainWindow.show()
    sys.exit(app.exec_())

    