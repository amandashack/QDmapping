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
        self.image = QPixmap()
        self.pixmap = QPixmap()
        #self.editMap = imageMapping(self.pixmap, self.imageMap, self.imageMapScene, self.ogImage, self.ogImageScene)
        
        #self.action = Action(self.pixmap)
        self.viewer = photoViewer(self.ogImage, self.ogImageScene)
        
        self.actionZoom_In.triggered.connect(self.handleZoomIn)
        self.actionOpen.triggered.connect(self.setImage)
        
        #self.actionUndo.triggered.connect(self.handleUndo)
        
        # self.drawing = False
        # self.lastPoint = QtCore.QPoint()
        
        #self.mousePressEvent(self, event)
        #self.ogImageScene.mouseMoveEvent = self.mouseMoveEvent(self, event)
        #self.ogImageScene.mouseReleaseEvent = self.mouseReleaseEvent(self, event)
        #self.pixmap.paintEvent = self.paintEvent(self, event)    
    def setImage(self):
         self.imageMapScene.clear()
         self.ogImageScene.clear()
         fileName, _ = QFileDialog.getOpenFileName(None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp)")
         if fileName:
             self.image = QPixmap(fileName) ###### self.image holds the original image at all times
             self.viewer.setImage(self.image)

             self.pixmap = self.viewer.scale(600, 600) #### self.pixmap is used for scaling and anything else
             self.drawMap = QPixmap(self.pixmap.width(), self.pixmap.height())
             self.drawMap.fill(QColor(Qt.white))

             self.ogImageScene.addPixmap(self.pixmap)
             self.imageMapScene.addPixmap(self.drawMap)

             self.ogImage.setScene(self.ogImageScene)
             self.imageMap.setScene(self.imageMapScene)
             

    def handleZoomIn(self):
        self.pixmap = self.viewer.zoomIn(self.pixmap)


class photoViewer(object):
    def __init__(self, ogImage, ogImageScene):
        self.ogImage = ogImage
        self.ogImageScene = ogImageScene
        self._zoom = 0

    def setImage(self, image):
        self.image = image

    def scale(self, width, height):
        if (self.image.isNull()):
            return(QPixmap())
        return(self.image.scaled(width, height, Qt.KeepAspectRatio))
        
    def zoomIn(self, pixmap):
        self._zoom += 1
        factor = 1.25
        pixmap = self.scale(pixmap.width()*factor, pixmap.height()*factor)
        self.ogImageScene.addPixmap(pixmap)
        return(pixmap)
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
    # def fitInView(self, scale=True):
    #     rect = QtCore.QRectF(self.ogImage.pixmap().rect())
    #     if not rect.isNull():
    #         self.setSceneRect(rect)
    #         if self.


#     def mouseReleaseEvent(self, event):
#        self.begin = event.pos()
#        self.end = event.pos()
#        QGraphicsPixmapItem.mouseReleaseEvent(self, event)
#        self.update()   
    
# class imageMapping(object):
#     def __init__(self, pixmap, imageMap, imageMapScene, ogImage, ogImageScene):
#         self.pixmap = pixmap
#         self.imageMap = imageMap
#         self.imageMapScene = imageMapScene
#         self.ogImage = ogImage
#         self.ogImageScene = ogImageScene
    
#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self.pixmap)
#         painter.drawPixmap(self.pixmap.rect(), self.pixmap)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drawing = True
#             self.lastPoint = event.pos()

#     def mouseMoveEvent(self, event):
#         if event.buttons() and Qt.LeftButton and self.drawing:
#             painter = QPainter(self.pixmap)
#             painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
#             painter.drawLine(self.lastPoint, event.pos())
#             self.lastPoint = event.pos()
#             self.ogImage.update()

#     def mouseReleaseEvent(self, event):
#         if event.button == Qt.LeftButton:
#             self.drawing = False

#class selectorTools(object):
    #https://stackoverflow.com/questions/15058621/python-interactive-selection-tools-like-in-matlab
    #https://stackoverflow.com/questions/5047325/region-of-interest-drawing-tool-for-image-analysis-in-python






import resource

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MyApp()
    MainWindow.show()
    sys.exit(app.exec_())