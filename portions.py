from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import sys
import math
import cv2
import qimage2ndarray as qi
from collections import defaultdict

from GraphicsView import *
from fftpop import *

'''

10/28
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NTS - the image editing becomes slower and slower the more you do it because it holds all of
        the previous edited conditions. possible fix - sending the old values to be stored somewhere else
        (undo/redo framework)

- added a confirmation window which will compare the original image to the justCOM image

- add radiobuttons for turning editing morphologies on and off and move this whole window to
        a different file. override group button class again

- bad practice not to include super when overriding - go back and look for this error and fix it

- clean up code and send to github

- make a separate program and make a tiny control

'''


#### used for timing purposes
def nothing(x):
    pass


def drawPoints(colorim, point):
    cv2.circle(colorim, (point[0], point[1]), 5, (0, 255, 255), -1)
    return(colorim)

def COM(editim):
        binary = editim
        _, contours, _ = cv2.findContours(binary.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        centres = []
        #area = []
        imperfections = 0
        for i in range(len(contours)):
            #if cv2.contourArea(contours[i]) > 5:
            M = cv2.moments(contours[i])
            if M['m00'] != 0:
                centres.append((int(M['m10']/M['m00']), int(M['m01']/M['m00'])))
                cv2.circle(binary, centres[-1], 1, (255, 255, 255), 1, -8)
                #area.append(cv2.contourArea(contours[i]))
            #else:
            #    imperfections += 1

        return(binary, centres)

def justCOM(thresh, centres):
        thresh[::] = 0
        #for i in range(thresh.shape[0]):
        #	for j in range(thresh.shape[1]):
	#		thresh.itemset((i, j), 0)

	#print(thresh.shape)
        for i in range(len(centres)):
            if centres[i][1] < thresh.shape[1] and centres[i][0] < thresh.shape[0]:
                #print(centres[i])	
                #com = np.zeros((thresh2.shape[0], thresh2.shape[1]), dtype=np.float32)
                thresh.itemset((centres[i][1], centres[i][0]), 255)
        #cv2.namedWindow('just COM', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('just COM', 700, 700)
        #cv2.imshow('just COM', thresh)
        #cv2.waitKey(0) & 0xFF
        #cv2.destroyAllWindows()
        return(thresh)

###### this is where comass.py ends
'''
PY3 = sys.version_info[0] == 3

if PY3:
    from functools import reduce

import numpy as np
import cv2

# built-in modules
import os
import itertools as it
from contextlib import contextmanager

image_extensions = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.pbm', '.pgm', '.ppm']

class Bunch(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)
    def __str__(self):
        return str(self.__dict__)

def splitfn(fn):
    path, fn = os.path.split(fn)
    name, ext = os.path.splitext(fn)
    return path, name, ext

def anorm2(a):
    return (a*a).sum(-1)
def anorm(a):
    return np.sqrt( anorm2(a) )

def homotrans(H, x, y):
    xs = H[0, 0]*x + H[0, 1]*y + H[0, 2]
    ys = H[1, 0]*x + H[1, 1]*y + H[1, 2]
    s  = H[2, 0]*x + H[2, 1]*y + H[2, 2]
    return xs/s, ys/s

def to_rect(a):
    a = np.ravel(a)
    if len(a) == 2:
        a = (0, 0, a[0], a[1])
    return np.array(a, np.float64).reshape(2, 2)

def rect2rect_mtx(src, dst):
    src, dst = to_rect(src), to_rect(dst)
    cx, cy = (dst[1] - dst[0]) / (src[1] - src[0])
    tx, ty = dst[0] - src[0] * (cx, cy)
    M = np.float64([[ cx,  0, tx],
                    [  0, cy, ty],
                    [  0,  0,  1]])
    return M


def lookat(eye, target, up = (0, 0, 1)):
    fwd = np.asarray(target, np.float64) - eye
    fwd /= anorm(fwd)
    right = np.cross(fwd, up)
    right /= anorm(right)
    down = np.cross(fwd, right)
    R = np.float64([right, down, fwd])
    tvec = -np.dot(R, eye)
    return R, tvec

def mtx2rvec(R):
    w, u, vt = cv2.SVDecomp(R - np.eye(3))
    p = vt[0] + u[:,0]*w[0]    # same as np.dot(R, vt[0])
    c = np.dot(vt[0], p)
    s = np.dot(vt[1], p)
    axis = np.cross(vt[0], vt[1])
    return axis * np.arctan2(s, c)

def draw_str(dst, target, s):
    x, y = target
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

class Sketcher:
    def __init__(self, windowname, dests, colors_func):
        self.prev_pt = None
        self.windowname = windowname
        self.dests = dests
        self.colors_func = colors_func
        self.dirty = False
        self.show()
        cv2.setMouseCallback(self.windowname, self.on_mouse)

    def show(self):
        cv2.imshow(self.windowname, self.dests[0])

    def on_mouse(self, event, x, y, flags, param):
        pt = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.prev_pt = pt
        elif event == cv2.EVENT_LBUTTONUP:
            self.prev_pt = None

        if self.prev_pt and flags & cv2.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.dests, self.colors_func()):
                cv2.line(dst, self.prev_pt, pt, color, 5)
            self.dirty = True
            self.prev_pt = pt
            self.show()


# palette data from matplotlib/_cm.py

_jet_data =   {'red':   ((0., 0, 0), (0.35, 0, 0), (0.66, 1, 1), (0.89,1, 1),
                         (1, 0.5, 0.5)),
               'green': ((0., 0, 0), (0.125,0, 0), (0.375,1, 1), (0.64,1, 1),
                         (0.91,0,0), (1, 0, 0)),
               'blue':  ((0., 0.5, 0.5), (0.11, 1, 1), (0.34, 1, 1), (0.65,0, 0),
                         (1, 0, 0))}

cmap_data = { 'jet' : _jet_data }

def make_cmap(name, n=256):
    data = cmap_data[name]
    xs = np.linspace(0.0, 1.0, n)
    channels = []
    eps = 1e-6
    for ch_name in ['blue', 'green', 'red']:
        ch_data = data[ch_name]
        xp, yp = [], []
        for x, y1, y2 in ch_data:
            xp += [x, x+eps]
            yp += [y1, y2]
        ch = np.interp(xs, xp, yp)
        channels.append(ch)
    return np.uint8(np.array(channels).T*255)

def nothing(*arg, **kw):
    pass

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

@contextmanager
def Timer(msg):
    print(msg, '...',)
    start = clock()
    try:
        yield
    finally:
        print("%.2f ms" % ((clock()-start)*1000))

class StatValue:
    def __init__(self, smooth_coef = 0.5):
        self.value = None
        self.smooth_coef = smooth_coef
    def update(self, v):
        if self.value is None:
            self.value = v
        else:
            c = self.smooth_coef
            self.value = c * self.value + (1.0-c) * v

class RectSelector:
    def __init__(self, win, callback):
        self.win = win
        self.callback = callback
        cv2.setMouseCallback(win, self.onmouse)
        self.drag_start = None
        self.drag_rect = None
    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            return
        if self.drag_start:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                xo, yo = self.drag_start
                x0, y0 = np.minimum([xo, yo], [x, y])
                x1, y1 = np.maximum([xo, yo], [x, y])
                self.drag_rect = None
                if x1-x0 > 0 and y1-y0 > 0:
                    self.drag_rect = (x0, y0, x1, y1)
            else:
                rect = self.drag_rect
                self.drag_start = None
                self.drag_rect = None
                if rect:
                    self.callback(rect)
    def draw(self, vis):
        if not self.drag_rect:
            return False
        x0, y0, x1, y1 = self.drag_rect
        cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 0), 2)
        return True
    @property
    def dragging(self):
        return self.drag_rect is not None


def grouper(n, iterable, fillvalue=None):
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    if PY3:
        output = it.zip_longest(fillvalue=fillvalue, *args)
    else:
        output = it.izip_longest(fillvalue=fillvalue, *args)
    return output

def mosaic(w, imgs):
    #Make a grid from images.
    #w    -- number of grid columns
    #imgs -- images (must have same size and format)
    
    imgs = iter(imgs)
    if PY3:
        img0 = next(imgs)
    else:
        img0 = imgs.next()
    pad = np.zeros_like(img0)
    imgs = it.chain([img0], imgs)
    rows = grouper(w, imgs, pad)
    return np.vstack(map(np.hstack, rows))

def getsize(img):
    h, w = img.shape[:2]
    return w, h

def mdot(*args):
    return reduce(np.dot, args)

def draw_keypoints(vis, keypoints, color = (0, 255, 255)):
    for kp in keypoints:
        x, y = kp.pt
        cv2.circle(vis, (int(x), int(y)), 2, color)


###### this is where file common.py ends

def shift_dft(src, dst=None):
    
    #      Rearrange the quadrants of Fourier image so that the origin is at
    #    the image center. Swaps quadrant 1 with 3, and 2 with 4.
    #    src and dst arrays must be equal size & type
    

    if dst is None:
        dst = np.empty(src.shape, src.dtype)
    elif src.shape != dst.shape:
        raise ValueError("src and dst must have equal sizes")
    elif src.dtype != dst.dtype:
        raise TypeError("src and dst must have equal types")

    if src is dst:
        ret = np.empty(src.shape, src.dtype)
    else:
        ret = dst

    h, w = src.shape[:2]

    cx1 = cx2 = w//2
    cy1 = cy2 = h//2

    # if the size is odd, then adjust the bottom/right quadrants
    if w % 2 != 0:
        cx2 += 1
    if h % 2 != 0:
        cy2 += 1
    ret[h-cy1:, w-cx1:] = src[0:cy1 , 0:cx1 ]   # q1 -> q3
    ret[0:cy2 , 0:cx2 ] = src[h-cy2:, w-cx2:]   # q3 -> q1

    # swap q2 and q4
    ret[0:cy2 , w-cx2:] = src[h-cy2:, 0:cx2 ]   # q2 -> q4
    ret[h-cy1:, 0:cx1 ] = src[0:cy1 , w-cx1:]   # q4 -> q2

    if src is dst:
        dst[:,:] = ret

    return dst



def reciprocal(im):
	h, w = im.shape[:2] #gets only the shape, not the number of channels if that information is present in shape
	realInput = im.astype(np.float64) #change to floats so you don't lose information when doing operations
# perform an optimally sized dft so that array size is a product of 2's, 3's or 5's.. increases performance
	dft_M = cv2.getOptimalDFTSize(w) 
	dft_N = cv2.getOptimalDFTSize(h)

	# copy A to dft_A and pad dft_A with zeros
	dft_A = np.zeros((dft_N, dft_M, 2), dtype=np.float64)
	dft_A[:h, :w, 0] = realInput
	# no need to pad bottom part of dft_A with zeros because of
	# use of nonzeroRows parameter in cv2.dft()
	cv2.dft(dft_A, dst=dft_A, nonzeroRows=h)

	#cv2.imshow("win", im)
	# Split fourier into real and imaginary parts
	image_Re, image_Im = cv2.split(dft_A)

	# Compute the magnitude of the spectrum Mag = sqrt(Re^2 + Im^2)
	magnitude = cv2.sqrt(image_Re**2.0 + image_Im**2.0)

	# Compute log(1 + Mag)
	log_spectrum = cv2.log(1.0 + magnitude)

	# Rearrange the quadrants of Fourier image so that the origin is at
	# the image center
	shift_dft(log_spectrum, log_spectrum)

	# normalize and display the results as rgb
	cv2.normalize(log_spectrum, log_spectrum, 0.0, 1.0, cv2.NORM_MINMAX)
	#cv2.imshow("magnitude", log_spectrum)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	dft_final = (log_spectrum*255).round().astype(np.uint8)
	#log_spectrum = log_spectrum.astype(uint8)
	return(dft_final)

##### this is where reciprocal.py ends



class Reciprocal(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        #self.image = self.image[selected region]
        self.label = QLabel()
        if len(colorIm.shape) == 3:
            if colorIm.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(colorIm, colorIm.shape[1], colorIm.shape[0], colorIm.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        self.pixmap1 = QPixmap("blah")
        self.label.setPixmap(self.pixmap1)
        self.show()
        # self.reciprocalIm = image
        # self.reciprocalIm = self.reciprocalIm
        # bytesPerLine = 3 * width
        # self.reciprocalIm = QImage(self.reciprocalIm, self.width, self.height, bytesPerLine, QImage.Format_Mono)
        # self.reciprocalIm = QPixmap(self.reciprocalIm)
        
        # self.label = QLabel()
        # self.label.setPixmap(self.reciprocalIm)
        
'''


###### radiobutton group box - I think this could be more agnostic 
###### by taking out the explicit names of the radiobuttons

class rdButton(QGroupBox):

    buttonChanged = pyqtSignal(str)

    def __init__(self, view):
        super(rdButton, self).__init__()
        self.view = view

	
        # Create an array of radio buttons
        rdButtons = [QRadioButton("Draw"), QRadioButton("Zoom"), QRadioButton("Pan"), QRadioButton("Reciprocal")]

        # Set a radio button to be checked by default
        rdButtons[0].setChecked(True)   

        # Radio buttons usually are in a vertical layout   
        button_layout = QVBoxLayout()

        # Create a button group for radio buttons
        self._button_group = QButtonGroup()

        for i in range(len(rdButtons)):
            radB = rdButtons[i]
            # Add each radio button to the button layout
            button_layout.addWidget(radB)
            # Add each radio button to the button group & give it an ID of i
            self._button_group.addButton(radB, i)
            # Connect each radio button to a method to run when it's clicked
            radB.clicked.connect(self.radio_button_clicked)

        # Set the layout of the group box to the button layout
        self.setLayout(button_layout)

    #Print out the ID & text of the checked radio button
    def radio_button_clicked(self):
        if self._button_group.checkedId() == 0:
            
            QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))

        if self._button_group.checkedId() == 1:
            
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        if self._button_group.checkedId() == 2:
            
            QApplication.setOverrideCursor(QCursor(Qt.OpenHandCursor))

        if self._button_group.checkedId() == 3:
            
            QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        else: QApplication.setOverrideCursor(QCursor(Qt.ArrowCursor))
		
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
    
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
        
        screenShape = QDesktopWidget().screenGeometry()
        print(screenShape)
        self.setGeometry(300, 300, 250, 150)
        
        self.scene = GraphicsScene(self)
        self.dscene = GraphicsScene(self)
        self.setScene(self.scene)
        self.dView.setScene(self.dscene)
        
        '''
        self.dView.scene().retrieval(self.scene())
        self.pixmapItem = QGraphicsPixmapItem()
        self.dpixmapItem = QGraphicsPixmapItem()
        self.scene().addItem(self.pixmapItem)
        self.dView.scene().addItem(self.dpixmapItem)
        '''
        self.dscene.retrieval(self.scene)
        self.pixmapItem = QGraphicsPixmapItem()
        self.dpixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.dscene.addItem(self.dpixmapItem)
        

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

                # scale the image because it is too zoomed out
                width = self.image.width() * 0.2
                height = self.image.height() * 0.2
                self.imageScaled = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)

                #changed from ARGB which is only used if you want something to have a possible transparancy factor
                self.dimage = QImage(self.imageScaled.width(), self.imageScaled.height(), QImage.Format_RGB32)
                self.dpixmap = QPixmap(self.dimage)
                self.pixmapItem.setPixmap(self.imageScaled)#QtGui.QPixmap(filename))
                self.dpixmapItem.setPixmap(self.dpixmap)

                self.cvImage = cv2.imread(filename)
                self.cvogImage = cv2.imread(filename)
                self.cvogImageBW = cv2.imread(filename, 0)
                self.cvImageBW = cv2.imread(filename, 0)
            
            elif self._empty == False:
                
                
                self.scene.clear()
                self.image = QPixmap(filename) #this should not change unless a new image is selected
                width = self.image.width() * 0.3
                height = self.image.height() * 0.3
                self.imageScaled = self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio)
                
                self.pixmapItem = QGraphicsPixmapItem()
                self.scene.addItem(self.pixmapItem)
                self.dimage = QImage(self.imageScaled.width(), self.imageScaled.height(), \
                                     QImage.Format_RGB32)
                self.dpixmap = QPixmap(self.dimage)
                
                self.pixmapItem.setPixmap(self.imageScaled)
                self.dpixmapItem.setPixmap(self.dpixmap)

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
                self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
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
            sceneRect = self.mapToScene(rubberRect).boundingRect() # maptoScene returns a QPolygonF object and then calls the method boundingRect
            

            self.changeRubberBand = False
            self.rubberBand.hide() #if you would like for the selected region to go away after release

            widthScale = self.imageScaled.width() / rubberRect.width()
            heightScale = self.imageScaled.height() / rubberRect.height()
            

            ##### you can scale the image easily bu scaling the viewport
            ##### however, this significantly blurs the image

            #widthScale = self.imageScaled.width() / rubberRect.height()
            #heightScale = self.imageScaled.height() / rubberRect.height()
            
            self.imageScaled = self.image.scaled(widthScale, heightScale, \
                                     QtCore.Qt.KeepAspectRatio)
            #self.imageScaled = self.image.scaled(.8, .8, QtCore.Qt.KeepAspectRatio)
            #center = [sceneRect.y() + (sceneRect.height() / 2), sceneRect.x() + (sceneRect.width() / 2)]
            #TODO - make it so the viewport is centered on the center of the selection region 
            #self.centerOn(center[1], center[0]) 
            self.scene.clear()
            self.pixmapItem = QGraphicsPixmapItem()
            self.scene.addItem(self.pixmapItem)
            self.pixmapItem.setPixmap(self.imageScaled)
            #self.centerOn(sceneRect.center())
            
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
        self.w.setGeometry(400, 400, 700, 400)
        self.w.show()



def uint8Convert(frames): # use this function to scale a 3D numpy array of floats to 0-255 so it plays well with Qt methods

    # convert float array to uint8 array
    if np.min(frames)<0:
        frames_uint8 = [np.uint8((np.array(frames[i]) - np.min(frames[i]))/np.max(frames[i])*255) for i in range(np.shape(frames)[0])]
    else:
        frames_uint8 = [np.uint8(np.array(frames[i])/np.max(frames[i])*255) for i in range(np.shape(frames)[0])]

    return frames_uint8



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.myApp = myApp2(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.myApp)
        self.setCentralWidget(_widget)
        self.setGeometry(100, 100, 1300, 750)

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

class myPopup(QWidget):
    def __init__(self, image, COM):
        super(myPopup, self).__init__()

        grid = QGridLayout()

        self.image = image
        self.COM = QPixmap(COM)
        self.view = QGraphicsView()
        self.viewCOM = QGraphicsView()
        self.scene = QGraphicsScene()
        self.sceneCOM = QGraphicsScene()
        self.scene.addPixmap(self.image)
        self.sceneCOM.addPixmap(self.COM)
        self.view.setScene(self.scene)
        self.viewCOM.setScene(self.sceneCOM)

        self.words = QLabel()
        self.words.setText("If the centers of mass look correct, press accept. Otherwise, decline.")
        self.words.setAlignment(Qt.AlignCenter)
        
        self.accept = QPushButton()
        self.decline = QPushButton()
        self.accept.setText("accept")
        self.decline.setText("decline")

        grid.addWidget(self.view, 0, 0, 1, 2)
        grid.addWidget(self.viewCOM, 0, 2, 1, 2)
        grid.addWidget(self.words, 2, 0, 1, -1)
        grid.addWidget(self.accept, 3, 2)
        grid.addWidget(self.decline, 3, 3)
        self.setLayout(grid)

        self.decline.pressed.connect(self.declinePressed)
        self.accept.pressed.connect(self.acceptPressed)

    def acceptPressed(self):
        print('accept was pressed')


    def declinePressed(self):
        print('decline was pressed')

class editWindow(QWidget, photoManager):

    def __init__(self, pixmap, editImage, rect, scale, parent=None):
        super(editWindow, self).__init__(parent)
        self.setWindowTitle("Reciprical space edit")
        self.og_pixmap = pixmap # NTS - the cropped selected region
        self.og_ImageEdit = editImage # NTS - the full original black and white image in cv2 format
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``
        # maybe just crop the image here so that anything done doesnt require changing its shape
        self.ImageEdit = editImage
        self.scale = scale
        self.rect = rect

        #self.ImageEdit = cv2.resize(self.ImageEdit, (self.scale[0], self.scale[1]), cv2.INTER_CUBIC)
        #self.ImageEdit = self.ImageEdit[self.rect.x(): self.rect.x() + self.rect.width()-1, self.rect.y(): self.rect.y() + self.height()-1]
        #self.ogImageEdit = cv2.resize(self.ogImageEdit, (self.scale[0], self.scale[1]), cv2.INTER_CUBIC)
        #self.ogImageEdit = self.ogImageEdit[self.rect.x(): self.rect.x() + self.rect.width()-1, self.rect.y(): self.rect.y() + self.height()-1]
 
        
        self.initUI()
    
    def initUI(self):
        self.view = QGraphicsView()
        self.view.setScene(QGraphicsScene())
        self.pixmapItem = QGraphicsPixmapItem() #check if everytime you open a new image the old image is still an item
        self.pixmapItem.setPixmap(self.og_pixmap)
        self.view.scene().addItem(self.pixmapItem)

        self.opDict = defaultdict(list)

        self.sl1 = QSlider(Qt.Horizontal)
        self.lbl1 = QLabel()
        self.lbl1.setText("erode")
        self.sl1.setObjectName("erode")
        self.sl1.setMinimum(0)
        self.sl1.setMaximum(10)
        self.sl1.setValue(1)
        self.sl1.setTickPosition(QSlider.TicksBelow)
        self.sl1.setTickInterval(1)

        self.sl2 = QSlider(Qt.Horizontal)
        self.lbl2 = QLabel()
        self.lbl2.setText("dilate")
        self.sl2.setObjectName("dilate")
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(10)
        self.sl2.setValue(1)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(1)

        self.sl3 = QSlider(Qt.Horizontal)
        self.lbl3 = QLabel()
        self.lbl3.setText("open")
        self.sl3.setObjectName('open')
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(10)
        self.sl3.setValue(0)
        self.sl3.setTickPosition(QSlider.TicksBelow)
        self.sl3.setTickInterval(1)

        self.sl4 = QSlider(Qt.Horizontal)
        self.sl4.setObjectName("close")
        self.lbl4 = QLabel()
        self.lbl4.setText("close")
        self.sl4.setMinimum(0)
        self.sl4.setMaximum(5)
        self.sl4.setValue(1)
        self.sl4.setTickPosition(QSlider.TicksBelow)
        self.sl4.setTickInterval(1)
        

        self.sl5 = QSlider(Qt.Horizontal)
        self.lbl5 = QLabel()
        self.lbl5.setText("blackhat")
        self.sl5.setObjectName('blackhat')
        self.sl5.setMinimum(0)
        self.sl5.setMaximum(30)
        self.sl5.setValue(10)
        self.sl5.setTickPosition(QSlider.TicksBelow)
        self.sl5.setTickInterval(2)


        self.sl6 = QSlider(Qt.Horizontal)
        self.lbl6 = QLabel()
        self.lbl6.setText("blur")
        self.sl6.setObjectName("blur")
        self.sl6.setMinimum(0)
        self.sl6.setMaximum(10)
        self.sl6.setValue(1)
        self.sl6.setTickPosition(QSlider.TicksBelow)
        self.sl6.setTickInterval(1)


        self.sl7 = QSlider(Qt.Horizontal)
        self.sl7.setObjectName("Threshold")
        self.lbl7 = QLabel()
        self.lbl7.setText("Threshold")
        self.sl7.setMinimum(0)
        self.sl7.setMaximum(10)
        self.sl7.setTickPosition(QSlider.TicksBelow)
        self.sl7.setTickInterval(1)

 
        self.sl8 = QSlider(Qt.Horizontal)
        self.sl8.setObjectName("tophat")
        self.lbl8 = QLabel()
        self.lbl8.setText("tophat")
        self.sl8.setMinimum(0)
        self.sl8.setMaximum(10)
        self.sl8.setTickPosition(QSlider.TicksBelow)
        self.sl8.setTickInterval(1)

       

        buttons = QButtonGroup()
        self.cancel = QPushButton()
        self.cancel.setText("Cancel")
        self.cancel.setCheckable(True)
        self.cancel.toggle()
        self.accept = QPushButton()
        self.accept = QPushButton("Accept")
        self.accept.setCheckable(True)
        self.accept.toggle()
        buttons.addButton(self.cancel)
        buttons.addButton(self.accept)

        grid = QGridLayout()

        grid.addWidget(self.view, 0, 0, -1, 2)

        grid.addWidget(self.lbl1, 0, 2, 1, -1)
        grid.addWidget(self.sl1, 1, 2, 1, -1)
        grid.addWidget(self.lbl2, 2, 2, 1, -1)
        grid.addWidget(self.sl2, 3, 2, 1, -1)
        grid.addWidget(self.lbl3, 4, 2, 1, -1)
        grid.addWidget(self.sl3, 5, 2, 1, -1)
        grid.addWidget(self.lbl4, 6, 2, 1, -1)
        grid.addWidget(self.sl4, 7, 2, 1, -1)
        grid.addWidget(self.lbl8, 8, 2, 1, -1)
        grid.addWidget(self.sl8, 9, 2, 1, -1)
        grid.addWidget(self.lbl5, 10, 2, 1, -1)
        grid.addWidget(self.sl5, 11, 2, 1, -1)
        grid.addWidget(self.lbl6, 12, 2, 1, -1)
        grid.addWidget(self.sl6, 13, 2, 1, -1)
        grid.addWidget(self.lbl7, 14, 2, 1, -1)
        grid.addWidget(self.sl7, 15, 2, 1, -1)

        grid.addWidget(self.cancel, 16, 2, 1, 1)
        grid.addWidget(self.accept, 16, 3, 1, -1)

        '''
        frame1 = QFrame() #frame around right side layout
        frame2 = QFrame() #frame around buttons

        frame2.setLayout(hbox2)
        vbox.addWidget(frame2)
        frame1.setLayout(vbox)

        hbox1.addWidget(self.view)
        hbox1.addWidget(frame1)
        '''
        self.setLayout(grid)

        self.sl1.valueChanged.connect(self.valuechange)
        self.sl2.valueChanged.connect(self.valuechange)
        self.sl3.valueChanged.connect(self.valuechange) ######### you're copying and pasting -- we can overwrite the slider class and make a value change/edit area
        self.sl4.valueChanged.connect(self.valuechange)
        self.sl5.valueChanged.connect(self.valuechange)
        self.sl6.valueChanged.connect(self.valuechange)
        self.sl7.valueChanged.connect(self.valuechange)
        self.sl8.valueChanged.connect(self.valuechange)

        self.cancel.clicked.connect(self.close)
        self.accept.clicked.connect(self.acceptButton)

    def acceptButton(self):

        editim = self.ImageEdit
        editim = cv2.resize(self.ImageEdit, (self.scale[0], self.scale[1]), cv2.INTER_CUBIC)
        
        x = self.rect.x() 
        width = self.rect.x() + self.rect.width() 
        width = int(2 * round(width / 2.))
        y = self.rect.y() 
        height = self.rect.y() + self.rect.height()
        
        ##### this step was giving an error staying QImage: Too many arguments. This is because "you need an object that supports the buffer protocol"
        ##### if Qt expects a signed char * or an unsigned char * then PyQt4 will accept bytes. A numpy array satisfies both of these but
        ##### apparently a numpy view does not - in order to return to an array after completing an operation that greats a numpy view, do .copy()
        editim = editim[y:height, x:width].copy()
        
        editim, centres = COM(editim) 
        #editim = justCOM(editim, centres)

        ##### the problem now is the fact that QImage needs to know how many bytesperline the array is, otherwise it will just guess and it may guess wrong
        #### see stack overflow - QImage skews some images but not others
        #### the work around was to make sure that the width was a factor of 2. however, does this always work? if this comes up as a bug later on, look back at 
        #### stackoverflow page
        print(editim.shape, self.rect.width(), self.rect.height())
        #dataUint8 = uint8Convert(editim)
        #height, width = np.shape(dataUint8)
        #totalBytes = dataUint8[0].nbytes
        #bytesperline = int(totalBytes/height) #this is the line I don't understand
        #### not sure if this whole precuress is necessary or if you can just use the width straight from the image?
        #width = self.rect.width()
        image = QImage(editim, editim.shape[1], editim.shape[0], QImage.Format_Grayscale8)
        self.w = myPopup(self.og_pixmap, image)
        self.w.setGeometry(400, 400, 700, 400)
        self.w.show()

        ### you can always use drawPoints function to see where the circles are

        # TODO - fix the accept button and make it so that the distances and angles are found and printed in the terminal (eventually a database is created with this information)
  
        #TODO have a new window pop up which shows the reciprocal space image

    def valuechange(self):

        
        sender = self.sender()

        if sender.objectName() in self.opDict:
            pass
        else:
            self.opDict[sender.objectName()] = []

        # TODO - BUG - sometimes when you do thresholding, and then go back and change any of the other morphological transformations
        #              it gets rid of the thresholding
        self.ImageEdit = self.editIm(self.og_ImageEdit, self.opDict, sender.objectName(), sender.value())
        width = self.ImageEdit.shape[1]
        image = QImage(self.ImageEdit, self.ImageEdit.shape[1], self.ImageEdit.shape[0], width, QImage.Format_Grayscale8)
                        #self.imageEdit.shape[1] * 3, QImage.Format_Grayscale16)
        self.pixmap = QPixmap(image)
        width = self.scale[0]
        height = self.scale[1]
        self.pixmap = self.pixmap.scaled(width, height, Qt.KeepAspectRatio)
        self.pixmap = self.pixmap.copy(self.rect)
        
        self.view.scene().clear()
        self.pixmapItem = QGraphicsPixmapItem()
        self.view.scene().addItem(self.pixmapItem)
        self.pixmapItem.setPixmap(self.pixmap)

    
    def updatePixmap(self, pixmap):
        self.pixmapItem.setPixmap(pixmap)
        self.view.scene().addItem(self.pixmapItem)



        

class myApp2(QWidget, photoManager):
    def __init__(self, parent=None):
        super(myApp2, self).__init__(parent)
        
        self.setWindowTitle("selecting")
        self.initUI()
    
    def initUI(self):
        # TODO - add reset button

        grid = QGridLayout()
        grid.setVerticalSpacing(20)
        grid.setHorizontalSpacing(50)
        

        
        self.drawView = QGraphicsView(self)
        self.view = GraphicsView(self.drawView, self)
        self.drawView.setMouseTracking(True)
        self.view.setMouseTracking(True)
        self.rd = rdButton(self.view)
        

        self.editDict = defaultdict(list)

        # TODO - add a radiobutton to have a slider turned on and off
        self.lbl1 = QLabel()
        self.lbl1.setText("erode")
        self.lbl1.setAlignment(Qt.AlignCenter)
        self.sl1 = QSlider(Qt.Horizontal)
        self.sl1.setObjectName("erode")
        self.sl1.setMinimum(0)
        self.sl1.setMaximum(10)
        self.sl1.setValue(1)
        self.sl1.setTickPosition(QSlider.TicksBelow)
        self.sl1.setTickInterval(1)

        self.lbl2 = QLabel()
        self.lbl2.setText("open")
        self.lbl2.setAlignment(Qt.AlignCenter)
        self.sl2 = QSlider(Qt.Horizontal)
        self.sl2.setObjectName('open')
        self.sl2.setMinimum(0)
        self.sl2.setMaximum(10)
        self.sl2.setValue(1)
        self.sl2.setTickPosition(QSlider.TicksBelow)
        self.sl2.setTickInterval(1)

        self.lbl3 = QLabel()
        self.lbl3.setText("blackhat")
        self.lbl3.setAlignment(Qt.AlignCenter)
        self.sl3 = QSlider(Qt.Horizontal)
        self.sl3.setObjectName('blackhat')
        self.sl3.setMinimum(0)
        self.sl3.setMaximum(10)
        self.sl3.setValue(1)
        self.sl3.setTickPosition(QSlider.TicksBelow)
        self.sl3.setTickInterval(1)

        self.lbl4 = QLabel()
        self.lbl4.setText("tophat")
        self.lbl4.setAlignment(Qt.AlignCenter)
        self.sl4 = QSlider(Qt.Horizontal)
        self.sl4.setObjectName('tophat')
        self.sl4.setMinimum(0)
        self.sl4.setMaximum(10)
        self.sl4.setValue(1)
        self.sl4.setTickPosition(QSlider.TicksBelow)
        self.sl4.setTickInterval(1)


        self.lbl5 = QLabel()
        self.lbl5.setText("close")
        self.lbl5.setAlignment(Qt.AlignCenter)
        self.sl5 = QSlider(Qt.Horizontal)
        self.sl5.setObjectName('close')
        self.sl5.setMinimum(0)
        self.sl5.setMaximum(10)
        self.sl5.setValue(1)
        self.sl5.setTickPosition(QSlider.TicksBelow)
        self.sl5.setTickInterval(1)


        self.lbl6 = QLabel()
        self.lbl6.setText("dilate")
        self.lbl6.setAlignment(Qt.AlignCenter)
        self.sl6 = QSlider(Qt.Horizontal)
        self.sl6.setObjectName('dilate')
        self.sl6.setMinimum(0)
        self.sl6.setMaximum(10)
        self.sl6.setValue(1)
        self.sl6.setTickPosition(QSlider.TicksBelow)
        self.sl6.setTickInterval(1)


        
        grid.addWidget(self.view, 0, 0, -1, 15)
        grid.addWidget(self.drawView, 0, 14, -1, 15)
        grid.addWidget(self.rd, 0, 29, 1, 3)
        grid.addWidget(self.lbl1, 1, 29, 1, 3)
        grid.addWidget(self.sl1, 2, 29, 1, 3)
        grid.addWidget(self.lbl6, 3, 29, 1, 3)
        grid.addWidget(self.sl6, 4, 29, 1, 3)
        grid.addWidget(self.lbl2, 5, 29, 1, 3)
        grid.addWidget(self.sl2, 6, 29, 1, 3)
        grid.addWidget(self.lbl5, 7, 29, 1, 3)
        grid.addWidget(self.sl5, 8, 29, 1, 3)
        grid.addWidget(self.lbl3, 9, 29, 1, 3)
        grid.addWidget(self.sl3, 10, 29, 1, 3)
        grid.addWidget(self.lbl4, 11, 29, 1, 3)
        grid.addWidget(self.sl4, 12, 29, 1, 3)

        self.setLayout(grid)

        self.sl1.valueChanged.connect(self.valuechange)
        self.sl2.valueChanged.connect(self.valuechange)
        self.sl3.valueChanged.connect(self.valuechange)
        self.sl4.valueChanged.connect(self.valuechange)
        self.sl5.valueChanged.connect(self.valuechange)
        self.sl6.valueChanged.connect(self.valuechange)




    def connectRB(self):
        return(self.rd._button_group.checkedId())

    def setImage(self):
        self.view.setImage()
  

    def valuechange(self):

        
        sender = self.sender()

        if sender.objectName() in self.editDict:
            pass
        else:
            self.editDict[sender.objectName()] = []

        self.imageEdit = self.editIm(self.view.cvogImageBW, self.editDict, sender.objectName(), sender.value())
         
        self.imageEdit = QImage(self.imageEdit, self.imageEdit.shape[1], self.imageEdit.shape[0], QImage.Format_Grayscale8)
        
        self.pixmap = QPixmap(self.imageEdit)
        
        width = self.view.imageScaled.width()
        height = self.view.imageScaled.height()
        self.pixmap = self.pixmap.scaled(width, height, Qt.KeepAspectRatio)
        
        self.view.scene().clear()
        self.pixmapItem = QGraphicsPixmapItem()
        self.view.scene().addItem(self.pixmapItem)
        self.pixmapItem.setPixmap(self.pixmap)
  
    
    def updatePixmap(self, pixmap):
        self.view.pixmapItem.setPixmap(pixmap)

if __name__ == "__main__":
    # image = cv2.imread("qds.tif", 0)
    # image = image[0:500, 0:500]
    # editim = image
    # sizeset = dict() #a dictionary of size of image and the settings for that size area
    
    # editim, sizeset = edit(editim, sizeset)
    # editim, centres2 = COM(editim)
    # editim = justCOM(editim, centres2)
    # image = reciprocal(editim)

    # editim = image
    # sizeset = dict()
    # editim, sizeset = edit(editim, sizeset)
    # editim, centres = COM(editim)
    # #editim = justCOM(editim, centres)
    # image = editim
    # cv2.namedWindow('final', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('final', 700, 700)
    # cv2.imshow('final', image)

    # k = cv2.waitKey(0) & 0xFF
    # if k == 27:
    #     cv2.destroyAllWindows()
    # if k == ord("s"):
    #     cv2.imwrite("fft.png", image)
    #     cv2.destroyAllWindows()
    # image = cv2.imread("fft.png", 0)
    # colorIm = cv2.imread("fft.png")
    # editim = image
    # editim, centres = COM(image)
    # for i, j in centres:
    #     colorIm = drawPoints(colorIm, (i, j))
    # cv2.namedWindow('final', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('final', 700, 700)
    # cv2.imshow('final', colorIm)
    # cv2.waitKey(0) & 0xFF
    # cv2.destroyAllWindows()


    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
