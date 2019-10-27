from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import math
from GraphicsView import *

'''
10/16
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- drawing works in test.py and would like to integrate it back over here
- work like to fix the editing part - threshold needs to get the image as 
  its edited by the other 4 morphological transformations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.cs = [[0 for i in range(2)] for j in range(100)]
        self.image = QImage("blah")
        self.count = 0
        self.rotate = 1
        self.pos_x = 8
        self.pos_y = 8
        self.radius = 60
        self.delta = [1, 1]
        self.timerId = self.startTimer(15)
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('clipping')
        self.show()
    
    def drawImage(self, painter):
        painter.drawImage(0, 0, self.image.scaled(500, 500, Qt.KeepAspectRatio))

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        self.drawImage(painter)
        self.drawLines(painter)
        #self.drawDonut(painter)
        #self.drawShapes(painter)
        #self.drawRectangles(painter)
        #self.drawObjects(painter)
        painter.end()

    # def mousePressEvent(self, e):
    #     if e.button() == Qt.LeftButton:

            
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:

            x = e.x()
            y = e.y()
            
            self.cs[self.count][0] = x
            self.cs[self.count][1] = y
            self.count = self.count + 1
        
        if e.button() == Qt.RightButton:
            self.repaint() #calls paintEvent()
            self.count = 0
        
    def drawLines(self, painter):

        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        #painter.eraseRect(0, 0, w, h)

        for i in range(self.count):
            for j in range(self.count):
                painter.drawLine(self.cs[i][0], self.cs[i][1],
                                self.cs[j][0], self.cs[j][1])
    def drawDonut(self, painter):
        brush = QBrush(QColor("#535353"))
        painter.setPen(QPen(brush, 0.5))
        painter.setRenderHint(QPainter.Antialiasing)

        h = self.height()
        w = self.width()
        painter.translate(QPoint(w/2, h/2))

        rot = 0
        while rot < 360.0:
            painter.drawEllipse(-125, -40, 250, 80)
            painter.rotate(5.0)
            rot += 5.0
    def drawShapes(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#888888")))

        path1 = QPainterPath()

        path1.moveTo(5, 5) #sets the start point of path1
        path1.cubicTo(40, 5, 50, 50, 99, 99) #makes a bezier curve from the start point to the end point with c1 and c2 as additional points between
        path1.cubicTo(5, 99, 50, 50, 5, 5) # these c points are also added in the path
        painter.drawPath(path1)
    def drawRectangles(self, painter):
        for i in range(1, 11):
            painter.setOpacity(i*0.1)
            painter.fillRect(50*i, 20, 40, 40, Qt.darkGray)
    def drawObjects(self, painter):
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        rect = QRect(-100, -40, 200, 80)

        painter.translate(w/2, h/2)
        painter.rotate(self.rotate)
        painter.drawRect(rect)

        brush = QBrush(QColor(110, 110, 110))
        painter.setBrush(brush)

        painter.setClipRect(rect)

        painter.resetTransform()
        painter.drawEllipse(self.pos_x, self.pos_y, self.radius, self.radius)

        painter.setBrush(Qt.NoBrush)

        painter.setClipping(False)
        painter.drawEllipse(self.pos_x, self.pos_y, self.radius, self.radius)

    def timerEvent(self, event):

        self.step()
        self.repaint()

    def step(self):
        w = self.width()
        h = self.height()
        if self.pos_x < 0:
            self.delta[0] = 1
        
        elif self.pos_x > w - self.radius:
            self.delta[0] = -1
        
        if self.pos_y < 0:
            self.delta[1] = 1
        elif self.pos_y > h - self.radius:
            self.delta[1] = -1
        self.pos_x += self.delta[0]
        self.pos_y += self.delta[1]

        self.rotate = self.rotate + 1

class Item(QGraphicsRectItem):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setCursor(Qt.SizeAllCursor)
        self.setBrush(QColor(250, 100, 0))
        self.setPen(QPen(Qt.NoPen))



class ViewExample(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("custom item")
        self.init()

    def init(self, *args, **kwargs):
        QGraphicsView.__init__(self, *args, **kwargs)
        self.scene = QGraphicsScene()
        self.item = Item(0, 0, 100, 100)
        self.scene.addItem(self.item)
        
        self.setScene(self.scene)

class Rectangle(QGraphicsRectItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

        self.setBrush(QColor(250, 50, 0))
        self.setPen(QColor(250, 50, 0))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setCursor(Qt.SizeAllCursor)

        self.tx = 200
        self.ty = 200
    
    def doRotate(self, alfa):
        tr = QTransform()
        tr.translate(self.tx, self.ty)
        tr.rotate(alfa)
        tr.translate(-self.tx, -self.ty)

        self.setTransform(tr)

class View(QGraphicsView):
    def __init__(self):
        super(View, self).__init__()

        self.setRenderHint(QPainter.Antialiasing)

        self.initScene()
    
    def initScene(self):

        self.scene = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.setSceneRect(0, 0, 1000, 400)
        self.rect = Rectangle(150, 150, 100, 100)
        self.scene.addItem(self.rect)
        self.setScene(self.scene)

class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rotation")
        self.setGeometry(150, 150, 1000, 400)

        self.initUI()
    
    def initUI(self):
        vbox = QVBoxLayout()

        self.view = View()
        sld = QSlider(Qt.Horizontal, self)
        sld.setRange(-180, 180)
        sld.valueChanged[int].connect(self.changeValue)

        vbox.addWidget(self.view)
        vbox.addWidget(sld)
        self.setLayout(vbox)
    
    def changeValue(self, value):
        self.view.rect.doRotate(value)

TIME = 3000

class Ball(QObject):
    def __init__(self):
        super().__init__()
        self.image = QImage('blah')
        self.image = self.image.scaled(300, 300, Qt.KeepAspectRatio)
        self.pixmap = QPixmap(self.image)
        self.pixmap_item = QGraphicsPixmapItem(self.pixmap)

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)
    
    pos = pyqtProperty(QPointF, fset = _set_pos)

class myView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.initView()
    
    def initView(self):
        
        self.ball = Ball()
        self.ball.pos = QPointF(5, 50)

        self.animation = QPropertyAnimation(self.ball, b'pos')
        self.animation.setDuration(5000);
        self.animation.setStartValue(QPointF(5, 80))

        for i in range(20):
            self.animation.setKeyValueAt(i/20,
                            QPointF(i, math.sin(i)*30))
        
        self.animation.setEndValue(QPointF(570, 5))
        
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(120, -50, 250, 150)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.setWindowTitle("Sine wave animation")
        self.setRenderHint(QPainter.Antialiasing)
        self.setGeometry(300, 300, 700, 200)

        self.animation.start()

            
class view(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)

class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.initScene()
    
    def initScene(self):
        for i in range(5):
            e = self.addEllipse(20*i, 40*i, 50, 50)
            flag1 = QGraphicsItem.ItemIsMovable
            flag2 = QGraphicsItem.ItemIsSelectable

            e.setFlag(flag1, True)
            e.setFlag(flag2, True)

class Ex(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(150, 150, 350, 300)
        self.setWindowTitle("Selection")
        self.initUI()
    
    def initUI(self):
        hbox = QHBoxLayout()

        self.view = view()
        self.scene = Scene()
        self.view.setScene(self.scene)

        hbox.addWidget(self.view)

        frame = QFrame()

        self.delete = QPushButton("Delete", frame)
        self.delete.setEnabled(False)
        vbox = QVBoxLayout()
        vbox.addWidget(self.delete)
        vbox.addStretch(1)

        frame.setLayout(vbox)
        hbox.addWidget(frame)
        self.setLayout(hbox)

        self.delete.clicked.connect(self.onClick)
        self.scene.selectionChanged.connect(self.selChanged)
    
    def onClick(self):
        selectedItems = self.scene.selectedItems()

        if len(selectedItems) > 0:
            for item in selectedItems:
                self.scene.removeItem(item)
    
    def selChanged(self):
        selectedItems = self.scene.selectedItems()

        if len(selectedItems):
            self.delete.setEnabled(True)
        else:
            self.delete.setEnabled(False)

class View2(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(300, 300, 300, 300)
        self.setRenderHint(QPainter.Antialiasing)

        self.init()
    
    def init(self):
        self.scene = QGraphicsScene()

        r1 = self.scene.addRect(150, 40, 100, 100)
        r1.setBrush(QColor(250, 50, 0))
        r1.setPen(QColor(250, 50, 0))

        e1 = self.scene.addEllipse(40, 70, 80, 80)
        e1.setBrush(QColor(0, 50, 250))
        e1.setPen(QColor(0, 50, 250))

        r2 = self.scene.addRect(60, 180, 150, 70)
        r2.setBrush(QColor(0, 250, 50))
        r2.setPen(QColor(0, 250, 50))

        self.setScene(self.scene)

class Example3(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        vbox = QVBoxLayout()

        self.view = View2()

        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(1, 500)
        slider.setValue(100)
        slider.valueChanged[int].connect(self.onZoom)

        vbox.addWidget(self.view)
        vbox.addWidget(slider)

        self.setLayout(vbox)
        self.setWindowTitle("Zoom")
        self.setGeometry(150, 150, 300, 300)
    
    def onZoom(self, value):
        val = value / 100
        self.view.resetTransform()
        self.view.scale(val, val)

class MyGroup(QGraphicsItemGroup):

    def __init__(self):
        super().__init__()

        self.setCursor(Qt.OpenHandCursor)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)

    def paint(self, painter, option, widget):

        painter.setRenderHint(QPainter.Antialiasing)

        brush = QBrush(QColor("#333333"))
        pen = QPen(brush, 0.5)
        pen.setStyle(Qt.DotLine)
        painter.setPen(pen)

        if self.isSelected():
            boundRect = self.boundingRect()
            painter.drawRect(boundRect)

class Scene(QGraphicsScene):

    def __init__(self):
        super().__init__()

        self.initScene()
    def initScene(self):

        self.r1 = self.addRect(20, 50, 120, 50)
        self.r1.setFlag(QGraphicsItem.ItemIsMovable)
        self.r1.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.r2 = self.addRect(150, 100, 50, 50)
        self.r2.setFlag(QGraphicsItem.ItemIsMovable)
        self.r2.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.c = self.addEllipse(30, 150, 60, 60)
        self.c.setFlag(QGraphicsItem.ItemIsMovable)
        self.c.setFlag(QGraphicsItem.ItemIsSelectable, True)

class View3(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)

        policy = Qt.ScrollBarAlwaysOff

        self.setVerticalScrollBarPolicy(policy)
        self.setHorizontalScrollBarPolicy(policy)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.init()
    
    def init(self):
        self.group = None
        self.scene = Scene()
        self.setSceneRect(0, 0, 300, 300)
        self.setScene(self.scene)
    
    def keyPressEvent(self, e):
        key = e.key()

        if key == Qt.Key_U:
            if self.group != None and self.group.isSelected():
                items = self.group.childItems()
                self.scene.destroyItemGroup(self.group)
                self.group = None
                for item in items:
                    item.setSelected(False)
        if key == Qt.Key_G:
            if self.group:
                return
            selectedItems = self.scene.selectedItems()

            if len(selectedItems) > 0:
                self.group = MyGroup()
                for item in selectedItems:
                    self.group.addToGroup(item)
                self.scene.addItem(self.group)

class  Example4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        hbox = QHBoxLayout()

        self.view = View3()
        hbox.addWidget(self.view)

        self.setLayout(hbox)
        self.setWindowTitle("Grouping")
        self.setGeometry(250, 150, 300, 300)

class View4(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 300, 300)

        policy = Qt.ScrollBarAlwaysOff

        self.setVerticalScrollBarPolicy(policy)
        self.setHorizontalScrollBarPolicy(policy)
        self.setRenderHint(QPainter.Antialiasing)
        self.initView()
    def initView(self):
        self.scene = self.Scene4()
        self.setSceneRect(0, 0, 300, 300)
        self.setScene(self.scene)

class Scene4(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.initScene()
    #def initScene(self):
    #    self.image =

class pixmapItem(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        
        self.image = QImage("blah")
        self.image = self.image.scaled(300, 300, Qt.KeepAspectRatio)
        self.pixmap = QPixmap(self.image)
        self.initItem()

    #def initItem(self):
        

class attempt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        hbox = QHBoxLayout()

        self.view = View4()
        hbox.addWidget(self.view)

        self.setGeometry(250, 150, 300, 300)
   

class rdButton(QGroupBox):

    buttonChanged = pyqtSignal(str)

    def __init__(self, view):
        super(rdButton, self).__init__()
        self.view = view


        rdButtons = [QRadioButton("Draw"), QRadioButton("Zoom"), QRadioButton("Pan"), QRadioButton("Reciprocal")]

        rdButtons[0].setChecked(True)   
 
        button_layout = QVBoxLayout()

        self._button_group = QButtonGroup()

        for i in range(len(rdButtons)):
            radB = rdButtons[i]
            button_layout.addWidget(radB)
            self._button_group.addButton(radB, i)
            radB.clicked.connect(self.radio_button_clicked)

        self.setLayout(button_layout)

    def radio_button_clicked(self):
        if self._button_group.checkedId() == 0:
            
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        if self._button_group.checkedId() == 1:
            
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        if self._button_group.checkedId() == 2:
            
            QApplication.setOverrideCursor(QCursor(Qt.OpenHandCursor))

        if self._button_group.checkedId() == 3:
            
            QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))


class GraphicsScene2(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene2, self).__init__(parent)
    
    def retrieval(self, scene):
        self.scene = scene

    def addPath2(self, path, pen=None, brush=None):

        pen = QtGui.QPen(QtGui.QColor("green"), 4, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap)
        self.item = graphicsPathItem(self, self.scene)
        self.item.setPen(pen)
        self.item.setPath(path)
        self.addItem(self.item)
        return(self.item)
            
class graphicsPathItem(QGraphicsPathItem):
    def __init__(self, dscene, scene, parent = None):
        super(QGraphicsPathItem, self).__init__(parent)
        self.dscene = dscene
        self.scene = scene

    def mouseDoubleClickEvent(self, e):
        pen = QtGui.QPen(QtGui.QColor("black"), 2, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap)
        self.scene.addPath(self.shape(), pen)
    
    def keyPressEvent(self, e):
        
        items = self.dscene.selectedItems()
        key = e.key()
        if key == QtCore.Qt.Key_Delete or key == QtCore.Qt.Key_Backspace: #the Delete button doesnt seem to work here, only the backspace. 

            for item in items:

                self.dscene.removeItem(item)
                self.dscene.update()



class GraphicsView(QGraphicsView, photoManager):
    rectChanged = pyqtSignal(QRect)

    def __init__(self, dView, parent = None):
        super(GraphicsView, self).__init__(parent)
        self.parent = parent
        self.dView = dView
        self.button = 0
        self.setGeometry(300, 300, 250, 150)
        self.setScene(GraphicsScene2(self))
        self.dView.setScene(GraphicsScene2(self))
        self.dView.scene().retrieval(self.scene())
        self.pixmapItem = QGraphicsPixmapItem()
        self.dpixmapItem = QGraphicsPixmapItem()
        self.scene().addItem(self.pixmapItem)
        self.dView.scene().addItem(self.dpixmapItem)
        self._empty = True
        self._path_item = None

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.dView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.dView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.origin = QPoint()
        self.changeRubberBand = False
        self.initial_path()

    def whichButton(self):
        self.button = self.parent.connectRB()
        
        
    def hasPhoto(self):
        return not self._empty
        
    def initial_path(self):
        self._path = QtGui.QPainterPath()
        pen = QtGui.QPen(QtGui.QColor("green"), 4, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap)
        self._path_item = self.dView.scene().addPath2(self._path, pen)

    def setImage(self):
        filename, _ = QFileDialog.getOpenFileName(
            None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp *.tif)"
        )
        if filename:
            if self._empty == True:

                self._empty = False
                self.image = QPixmap(filename)
                width = self.image.width() * 0.7
                height = self.image.height() * 0.7
                self.imageScaled = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)
                self.dimage = QImage(self.imageScaled.width(), self.imageScaled.height(), QImage.Format_ARGB32)
                self.dpixmap = QPixmap(self.dimage)
                self.pixmapItem.setPixmap(self.imageScaled)#QtGui.QPixmap(filename))
                self.dpixmapItem.setPixmap(self.dpixmap)

                self.cvImage = cv2.imread(filename)
                self.cvogImage = cv2.imread(filename)
                self.cvogImageBW = cv2.imread(filename, 0)
                self.cvImageBW = cv2.imread(filename, 0)
            
            elif self._empty == False:
                
                self.scene().clear()
                self.image = QPixmap(filename) #this should not change unless a new image is selected
                width = self.image.width() * 0.3
                height = self.image.height() * 0.3
                self.imageScaled = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)
                self.pixmapItem = QGraphicsPixmapItem()
                self.scene().addItem(self.pixmapItem)
                self.pixmapItem.setPixmap(self.imageScaled)#QtGui.QPixmap(filename))

                self.cvImage = cv2.imread(filename)
                self.cvogImage = cv2.imread(filename)
                self.cvogImageBW = cv2.imread(filename, 0)
                self.cvImageBW = cv2.imread(filename, 0)

    def mousePressEvent(self, event):

        self.whichButton()



        if self.button == 0:

            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

            start = event.pos()
            if (
                not self.pixmapItem.pixmap().isNull()
                and event.buttons() & Qt.LeftButton
            ):
                self.initial_path()
                self._path.moveTo(self.mapToScene(event.pos()))
                self._path_item.setPath(self._path)
            super(GraphicsView, self).mousePressEvent(event)

        elif self.button == 1:

            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

            if self.hasPhoto():
                self.origin = event.pos()
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rectChanged.emit(self.rubberBand.geometry())
                self.rubberBand.show()
                self.changeRubberBand = True
            QGraphicsView.mousePressEvent(self, event)
           
            #TODO - make zoom and pan radiobuttons work
        elif self.button == 2:

            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        elif self.button == 3:

            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            if self.hasPhoto():
                self.origin = event.pos()
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rectChanged.emit(self.rubberBand.geometry())
                self.rubberBand.show()
                self.changeRubberBand = True
            QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):

        if self.button == 0:

            if (
                not self.pixmapItem.pixmap().isNull()
                and event.buttons() & Qt.LeftButton
                and self._path_item is not None
            ):
                self._path.lineTo(self.mapToScene(event.pos()))
                self._path_item.setPath(self._path)
            super(GraphicsView, self).mousePressEvent(event)
        
        elif self.button == 1:
            if self.changeRubberBand:
                self.rubberBand.setG3eometry(QRect(self.origin, event.pos()).normalized())
                self.rectChanged.emit(self.rubberBand.geometry())
            QGraphicsView.mouseMoveEvent(self, event)

        elif self.button == 3:
            if self.changeRubberBand:
                self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
                self.rectChanged.emit(self.rubberBand.geometry())
            QGraphicsView.mouseMoveEvent(self, event)
        
        

    def mouseReleaseEvent(self, event):
        end = event.pos()

        if self.button == 0:
            if (
                not self.pixmapItem.pixmap().isNull()
                and self._path_item is not None
            ):
                self._path.lineTo(self.mapToScene(end))
                self._path.closeSubpath()
                self._path_item.setPath(self._path)
                self._path_item.setBrush(QBrush(QColor("red")))
                self._path_item.setFlag(
                    QGraphicsItem.ItemIsSelectable, True
                )
                self._path_item.setFlag(
                    QGraphicsItem.ItemIsFocusable, True
                )
                self._path_item = None
            super(GraphicsView, self).mouseReleaseEvent(event)

        elif self.button == 1:
            rubberRect = self.rubberBand.geometry()
            viewRect = self.viewport().rect()
            sceneRect = self.mapToScene(rubberRect).boundingRect()#QRectF(self.pixmapItem.pixmap().rect())
            
            self.changeRubberBand = False
            self.rubberBand.hide() #if you would like for the selected region to go away after release

            width = self.imageScaled.width() / rubberRect.height()
            height = self.imageScaled.height() / rubberRect.height()
            
            self.imageScaled = self.image.scaled(width * self.imageScaled.width(), height * self.imageScaled.height(), QtCore.Qt.KeepAspectRatio)
          
            #center = [sceneRect.y() + (sceneRect.height() / 2), sceneRect.x() + (sceneRect.width() / 2)]
            #TODO - make it so the viewport is centered on the center of the selection region 
            #self.centerOn(center[1], center[0])
            self.pixmapItem.setPixmap(self.imageScaled)
            
            QGraphicsView.mouseReleaseEvent(self, event)

        
        elif self.button == 3:
            rubberRect = self.rubberBand.geometry()
            viewRect = self.viewport().rect()
            sceneRect = QRectF(self.pixmapItem.pixmap().rect())
            
            self.changeRubberBand = False
            self.rubberBand.hide() #if you would like for the selected region to go away after release

            self.editWindowtoRecip(rubberRect)
            QGraphicsView.mouseReleaseEvent(self, event)
        
    def editWindowtoRecip(self, rubberRect):
        editim = self.pixmapItem.pixmap().copy(rubberRect)
        scale = [self.imageScaled.width(), self.imageScaled.height()]
        self.w = editWindow(editim, self.cvImageBW, rubberRect, scale)
        self.w.setGeometry(500, 500, 300, 300)
        self.w.show()







class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.myApp = myApp2(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.myApp)
        self.setCentralWidget(_widget)
        self.setGeometry(200, 200, 1000, 600)

        #self.status = self.statusBar()
        self.menuBar = self.createMenuBar()
    
    def newFile(self):
        pass
    
    def openFile(self):
        self.myApp.setImage()
    
    def saveFile(self):
        pass
    
    def saveFileAs(self):
        pass
    
    def close(self):
        pass
    
    def undo(self):
        pass
    
    def redo(self):
        pass
    
    def clearSelected(self):
        pass

    def zoomIn(self):
        pass
    
    def zoomOut(self):
        pass
    
    def normalSize(self):
        pass
    
    def fitToWindow(self):
        pass
    
    def createFileActions(self):

        ids = ["new", "open", "save", "saveas", "exit"]
        #This is where you would add icons in a list
        shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
        connects = [self.newFile, self.openFile, self.saveFile, self.saveFileAs, self.close]

        l = []

        for i in range(len(ids)):
            a = QAction(ids[i], self)
            a.setShortcut(shortcuts[i])
            #a.triggered.connect(self.restoreFocus) ###### ask developer about this
            a.setStatusTip(ids[i])
            if connects[i] != 0: a.triggered.connect(connects[i])
            l.append(a)
        
        l.insert(4, 0)

        return(l)
    
    def createEditActions(self):
        """
        could add a select all of a certain color and have it also highlight those in
        the file which holds all of the distances and angles for that group
        also could add a preferences or settings section
        """ 
        ids = ["undo", "redo", "clear_selected"]
		#icons = ["edit-undo.png", "edit-redo.png", "document-properties.png"]
        shortcuts = ['Ctrl+Z', 'Ctrl+Y', 'Del']
        connects = [self.undo, self.redo, self.clearSelected]

        l = []

        for i in range(len(ids)):
            a = QAction(ids[i], self)
            a.setShortcut(shortcuts[i])
            #a.triggered.connect(self.restoreFocus)
            a.setStatusTip(ids[i])
            if connects[i] != 0: a.triggered.connect(connects[i])
            l.append(a)
        
        l.insert(2,0)
        l.insert(5,0)
        l.insert(10,0)

        return l
    
    def createViewActions(self):

        ids = ["Zoom_In", "Zoom_Out", "Normal_Size", "Fit_to_Window"]
        #This is where you would add icons in a list
        shortcuts = ['Ctrl+Shift+=', 'Ctrl+Shift+-', 'Ctrl+N', 'Ctrl+Shift+N']
        connects = [self.zoomIn, self.zoomOut, self.normalSize, self.fitToWindow]

        l = []

        for i in range(len(ids)):
            a = QAction(ids[i], self)
            a.setShortcut(shortcuts[i])
            #a.triggered.connect(self.restoreFocus) ###### ask developer about this
            a.setStatusTip(ids[i])
            if connects[i] != 0: a.triggered.connect(connects[i])
            l.append(a)
        
        l.insert(4, 0)

        return(l)

    def createMenuBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File")
        editMenu = menubar.addMenu("Edit")
        viewMenu = menubar.addMenu("View")
        fileActions = self.createFileActions()
        editActions = self.createEditActions()
        viewActions = self.createViewActions()
        
        for i in fileActions:
            if i == 0: fileMenu.addSeparator()
            else: fileMenu.addAction(i)
        for i in editActions:
            if i == 0: editMenu.addSeparator()
            else: editMenu.addAction(i)
        for i in viewActions:
            if i == 0: viewMenu.addSeparator()
            else: viewMenu.addAction(i)

        return menubar







class myApp2(QWidget, photoManager):
    def __init__(self, parent=None):
        super(myApp2, self).__init__(parent)
        
        self.setWindowTitle("selecting")
        self.initUI()
    
    def initUI(self):

        hbox = QHBoxLayout()
        

        self.drawView = QGraphicsView(self)
        self.view = GraphicsView(self.drawView, self)
        self.drawView.setMouseTracking(True)
        self.view.setMouseTracking(True)
        self.rd = rdButton(self.view)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.rd)
        
        vbox.addStretch(1)

        hbox.addWidget(self.view)
        hbox.addWidget(self.drawView)



        frame = QFrame()
        frame.setLayout(vbox)
        hbox.addWidget(frame)
        self.setLayout(hbox)
        
        #self.view.mouseHoverEvent()
        #self.drawView.mouseHoverEvent()

    def mouseHoverEvent(self, e):
        print("hovering")

        
    def connectRB(self):
        return(self.rd._button_group.checkedId())

    def setImage(self):
        self.view.setImage()
    
    def valuechange(self):
        sender = self.sender()
        self.cvImage = self.editIm(self.view.cvogImage, sender.objectName(), sender.value())

        image = QImage(self.cvImage, self.cvImage.shape[1], self.cvImage.shape[0],
                        self.cvImage.shape[1] * 3, QImage.Format_RGB888)
        self.pixmap = QPixmap(image)
        self.pixmap = self.pixmap.scaled(self.view.imageScaled.width(), self.view.imageScaled.height(), Qt.KeepAspectRatio)

        self.updatePixmap(self.pixmap)
    
    def updatePixmap(self, pixmap):
        self.view.pixmapItem.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #w = Example()
    #w = ViewExample()
    #w = Example2()
    #w = myView()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
