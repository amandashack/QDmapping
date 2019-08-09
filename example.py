# import sys
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import *

# class Window(QApplication):

#     def __init__(self, parent = None):
    
        
#         self.label = QLabel()
        
#         self.lineEdit = QLineEdit("ABCDE")
#         self.fontComboBox = QFontComboBox()
#         self.sizeSpinBox = QDoubleSpinBox()
#         self.sizeSpinBox.setMinimum(1.0)
#         self.sizeSpinBox.setValue(12.0)
#         saveButton = QPushButton(self.tr("Save"))
        
#         self.lineEdit.textChanged.connect(self.updateImage)
#         self.fontComboBox.currentFontChanged.connect(self.updateImage)
#         self.sizeSpinBox.valueChanged.connect(self.updateImage)
#         saveButton.clicked.connect(self.saveImage)
        
#         formLayout = QFormLayout()
#         formLayout.addRow(self.tr("&Text:"), self.lineEdit)
#         formLayout.addRow(self.tr("&Font:"), self.fontComboBox)
#         formLayout.addRow(self.tr("Font &Size:"), self.sizeSpinBox)
        
#         layout = QGridLayout()
#         layout.addWidget(self.label, 0, 0, 1, 3, Qt.AlignCenter)
#         layout.addLayout(formLayout, 1, 0, 1, 3)
#         layout.addWidget(saveButton, 2, 1)
#         self.setLayout(layout)
        
#         self.updateImage()
#         self.setWindowTitle(self.tr("Paint Text"))
    
#     def updateImage(self):
    
#         font = QFont(self.fontComboBox.currentFont())
#         font.setPointSizeF(self.sizeSpinBox.value())
#         metrics = QFontMetricsF(font)
        
#         text = unicode(self.lineEdit.text())
#         if not text:
#             return
        
#         rect = metrics.boundingRect(text)
#         position = -rect.topLeft()
        
#         pixmap = QPixmap(rect.width(), rect.height())
#         pixmap.fill(Qt.white)
        
#         painter = QPainter()
#         painter.begin(pixmap)
#         painter.setFont(font)
#         painter.drawText(position, text)
#         painter.end()
        
#         self.label.setPixmap(pixmap)
    
#     def saveImage(self):
    
#         formats = QImageWriter.supportedImageFormats()
#         formats = map(lambda suffix: u"*."+unicode(suffix), formats)
#         path = unicode(QFileDialog.getSaveFileName(self, self.tr("Save Image"),
#             "", self.tr("Image files (%1)").arg(u" ".join(formats))))
        
#         if path:
#             if not self.label.pixmap().save(path):
#                 QMessageBox.warning(self, self.tr("Save Image"),
#                     self.tr("Failed to save file at the specified location."))


# if __name__ == "__main__":

#     app = QApplication(sys.argv)
#     window = Window()
#     window.show()
#     sys.exit(app.exec_())

# import sys
# from PyQt5.QtCore import Qt, QPoint
# from PyQt5.QtWidgets import QMainWindow, QApplication
# from PyQt5.QtGui import QPixmap, QPainter, QPen


# class Menu(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.drawing = False
#         self.lastPoint = QPoint()
#         self.image = QPixmap("blah.jpg")
#         self.setGeometry(100, 100, 500, 300)
#         self.resize(self.image.width(), self.image.height())
#         self.show()

#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.drawPixmap(self.rect(), self.image)

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
#             self.update()

#     def mouseReleaseEvent(self, event):
#         if event.button == Qt.LeftButton:
#             self.drawing = False


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mainMenu = Menu()
#     sys.exit(app.exec_())


import random, sys
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import *

class Window(QLabel):

    def __init__(self, parent = None):
    
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
    
    def mousePressEvent(self, event):
    
        if event.button() == Qt.LeftButton:
        
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
    
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
    
    def mouseReleaseEvent(self, event):
    
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()


def create_pixmap():

    def color():
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        return QColor(r, g, b)
    
    def point():
        return QPoint(random.randrange(0, 400), random.randrange(0, 300))
    
    pixmap = QPixmap(400, 300)
    pixmap.fill(color())
    painter = QPainter()
    painter.begin(pixmap)
    i = 0
    while i < 1000:
        painter.setBrush(color())
        painter.drawPolygon(QPolygon([point(), point(), point()]))
        i += 1
    
    painter.end()
    return pixmap


if __name__ == "__main__":

    app = QApplication(sys.argv)
    random.seed()
    
    window = Window()
    window.setPixmap(create_pixmap())
    window.resize(400, 300)
    window.show()
    
    sys.exit(app.exec_())