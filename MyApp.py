from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import *
from GraphicsView import *
import sys
import time

# class Action(object):
#     def __init__(self):


#     def paintEvent(self, event):
#         painter = QtGui.QPainter(self.ogImage)
#         painter.drawPixmap(self.ogImage.rect(), self.image)

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.drawing = True
#             self.lastPoint = event.pos()

#     def mouseMoveEvent(self, event):
#         if event.buttons() and Qt.LeftButton and self.drawing:
#             painter = QPainter(self.image)
#             painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
#             painter.drawLine(self.lastPoint, event.pos())
#             self.lastPoint = event.pos()
#             self.ogImage.update()

#     def mouseReleaseEvent(self, event):
#         if event.button == Qt.LeftButton:
#             self.drawing = False


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)

        self.ogImageScene = QGraphicsScene()
        self.imageMapScene = QGraphicsScene()
        self.ogImage.setScene(self.ogImageScene)
        self.imageMap.setScene(self.imageMapScene)
        # self.image = QPixmap()
        # self.pixmap = QPixmap()
        # #self.editMap = imageMapping(self.pixmap, self.imageMap, self.imageMapScene, self.ogImage, self.ogImageScene)
        
        #self.action = Action(self.pixmap)
        
        #self.actionUndo.triggered.connect(self.handleUndo)
        
        
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
        
        # self.ogImage.mousePressEvent = drawingTool.mousePressEvent(self, event)
        # self.ogImage.mouseMoveEvent = drawingTool.mouseMoveEvent(self, event)
        # self.ogImage.mouseReleaseEvent = drawingTool.mouseReleaseEvent(self, event)
        # self.ogImage.paintEvent = drawingTool.paintEvent(self, event)
        
        self.drawing = False
        self.lastPoint = QPoint()

    def setImage(self):
        fileName, _  = QFileDialog.getOpenFileName(None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp)")
        if fileName:
            self.image = QPixmap(fileName) ###### self.image holds the original image at all times
            self.pixmap = self.viewer.setDefaultImage(self.image)

    def handleZoomIn(self):
        self.pixmap = self.viewer.zoomIn(self.pixmap)
    
    def handleZoomOut(self):
        self.pixmap = self.viewer.zoomOut(self.pixmap)

    def handleNormalSize(self):
        self.pixmap = self.viewer.zeroZoom(self.pixmap)


import resource

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_())