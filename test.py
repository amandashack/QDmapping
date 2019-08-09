from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import math

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
    def initScene(self):
        self.image = 

class pixmapItem(QGraphicsPixmapItem):
    def __init__(self):
        super().__init__()
        
        self.image = QImage("blah")
        self.image = self.image.scaled(300, 300, Qt.KeepAspectRatio)
        self.pixmap = QPixmap(self.image)
        self.initItem()

    def initItem(self):
        

class attempt(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        hbox = QHBoxLayout()

        self.view = View4()
        hbox.addWidget(self.view)

        self.setGeometry(250, 150, 300, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #w = Example()
    #w = ViewExample()
    #w = Example2()
    #w = myView()
    w = Example4()
    w.show()
    sys.exit(app.exec_())
