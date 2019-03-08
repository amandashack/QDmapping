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

        self.ogImageScene = GraphicsScene(self)
        self.imageMapScene = GraphicsScene(self)
        self.ogImage.setScene(self.ogImageScene)
        self.imageMap.setScene(self.imageMapScene)
        self.path = QPainterPath()
        
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
        
        #self.ogImageScene.mousePressEvent = self.mousePressEvent
        #self.ogImageScene.mouseMoveEvent = self.mouseMoveEvent
        #self.ogImageScene.mouseReleaseEvent = self.mouseReleaseEvent
        #self.ogImage.mouseReleaseEvent = self.mouseReleaseEvent(self, event)
        #self.ogImage.paintEvent = self.paintEvent(self, event)
        
        self.drawing = False
        self.lastPoint = QPoint()

    #def mousePressEvent(self, event):
        
    # def paintEvent(self, event):
    
    #     painter = QPainter()
    #     painter.begin(self)
    #     painter.fillRect(event.rect(), QBrush(Qt.white))
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.setPen(QPen(QBrush(Qt.red), 1, Qt.DashLine))
    #     painter.drawRect(self.largest_rect)
    #     painter.setPen(QPen(Qt.black))
    #     painter.drawRect(self.clip_rect)
    #     for i in range(4):
    #         painter.drawRect(self.corner(i))
        
    #     painter.setClipRect(self.clip_rect)
    #     painter.drawPolyline(self.polygon)
    #     painter.setBrush(QBrush(Qt.blue))
    #     painter.drawPath(self.path)
    #     painter.end()
    
    # def corner(self, number):
    
    #     if number == 0:
    #         return QRect(self.clip_rect.topLeft() - self.handle_offsets[0], QSize(8, 8))
    #     elif number == 1:
    #         return QRect(self.clip_rect.topRight() - self.handle_offsets[1], QSize(8, 8))
    #     elif number == 2:
    #         return QRect(self.clip_rect.bottomLeft() - self.handle_offsets[2], QSize(8, 8))
    #     elif number == 3:
    #         return QRect(self.clip_rect.bottomRight() - self.handle_offsets[3], QSize(8, 8))
    
    # def mousePressEvent(self, event):
    
    #     position = QPointF(event.pos())
    #     print(str(position.x()) + str(position.y()))

    # def mouseMoveEvent(self, event):
    
    #     if self.dragging is None:
    #         return
        
    #     left = self.largest_rect.left()
    #     right = self.largest_rect.right()
    #     top = self.largest_rect.top()
    #     bottom = self.largest_rect.bottom()
        
    #     point = event.pos() + self.drag_offset + self.handle_offsets[self.dragging]
    #     point.setX(max(left, min(point.x(), right)))
    #     point.setY(max(top, min(point.y(), bottom)))
        
    #     if self.dragging == 0:
    #         self.clip_rect.setTopLeft(point)
    #     elif self.dragging == 1:
    #         self.clip_rect.setTopRight(point)
    #     elif self.dragging == 2:
    #         self.clip_rect.setBottomLeft(point)
    #     elif self.dragging == 3:
    #         self.clip_rect.setBottomRight(point)
        
    #     self.update()
    
    # def mouseReleaseEvent(self, event):
    
    #     self.dragging = None
    
    # def sizeHint(self):
    #     return QSize(500, 500)

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