from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from main import *
from GraphicsView import *
import sys
import time


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        self.ogImageScene = QGraphicsScene(self)
        self.imageMapScene = QGraphicsScene(self)
        self.ogImage.setScene(self.ogImageScene)
        self.imageMap.setScene(self.imageMapScene)
        self.image = QPixmap()
        self.pixmap = QPixmap()
        self.pixmapItem = QGraphicsPixmapItem()
        self.viewer = photoViewer(self.ogImage, self.ogImageScene, self.pixmapItem, 600, 600)
        
        self.actionOpen.triggered.connect(self.setImage)
        self.actionZoom_In.triggered.connect(self.handleZoomIn)
        self.actionZoom_Out.triggered.connect(self.handleZoomOut)
        self.actionNormal_Size.triggered.connect(self.handleNormalSize)
    
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