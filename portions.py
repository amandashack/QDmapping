from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import sys
import math

"""
add buttons which activate 
"""
import numpy as np
import cv2


def COM(binary):
	_, contours, _ = cv2.findContours(binary.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
	centres = []
	area = []
	imperfections = 0
	for i in range(len(contours)):
		#if cv2.contourArea(contours[i]) > 5:
		M = cv2.moments(contours[i])
		if M['m00'] != 0:
			centres.append((int(M['m10']/M['m00']), int(M['m01']/M['m00'])))
			cv2.circle(binary, centres[-1], 1, (0, 100, 0), 1, -8)
			area.append(cv2.contourArea(contours[i]))
  	 	#elif:
  	 	#   imperfections += 1
	return(binary, centres)

def justCOM(thresh, centres):
	for i in range(thresh.shape[0]):
		for j in range(thresh.shape[1]):
			thresh.itemset((i, j), 0)
 
	#print(thresh.shape)
	for i in range(len(centres)):
	#	#print(centres[i])	
	#	com = np.zeros((thresh2.shape[0], thresh2.shape[1]), dtype=np.float32)
		thresh.itemset((centres[i][1], centres[i][0]), 255)
	cv2.namedWindow('just COM', cv2.WINDOW_NORMAL)
	cv2.resizeWindow('just COM', 700, 700)
	cv2.imshow('just COM', thresh)
	cv2.waitKey(0) & 0xFF
	cv2.destroyAllWindows()
	return(thresh)

###### this is where comass.py ends

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
    '''grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx'''
    args = [iter(iterable)] * n
    if PY3:
        output = it.zip_longest(fillvalue=fillvalue, *args)
    else:
        output = it.izip_longest(fillvalue=fillvalue, *args)
    return output

def mosaic(w, imgs):
    '''Make a grid from images.
    w    -- number of grid columns
    imgs -- images (must have same size and format)
    '''
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

def nothing(x):
    pass

def trackbar(img, cur_mode, str_mode):
    cv2.namedWindow('edit')
    cv2.createTrackbar('op/size', 'edit', 12, 20, nothing)
    cv2.createTrackbar('iters', 'edit', 1, 10, nothing) 
    res = img.copy()
    while(1):
        cv2.imshow('edit', res)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            return(sz, iters, op)
            break
        sz = cv2.getTrackbarPos('op/size', 'edit')
        iters = cv2.getTrackbarPos('iters', 'edit')
        opers = cur_mode.split('/')
        if len(opers) > 1:
            sz = sz - 10
            op = opers[sz > 0]
            sz = abs(sz)
        else:
            op = opers[0]
        sz = sz*2+1
        if str_mode == 'ellipse':
            str_name = 'MORPH_' + str_mode.upper()
            oper_name = 'MORPH_' + op.upper()
            st = cv2.getStructuringElement(getattr(cv2, str_name), (sz, sz))
            res = cv2.morphologyEx(img, getattr(cv2, oper_name), st, iterations=iters)

            draw_str(res, (10, 20), 'mode: ' + cur_mode)
            draw_str(res, (10, 40), 'operation: ' + oper_name)
            draw_str(res, (10, 60), 'structure: ' + str_name)
            draw_str(res, (10, 80), 'ksize: %d  iters: %d' % (sz, iters))
        else:
            if op == 'GaussianBlur':
                res = cv2.GaussianBlur(img, (sz, sz), iters)
                #res = cv2.bilateralFilter(img, iters, sz, sz)
                draw_str(res, (10, 20), 'mode: Gaussian Blur')
            if op == 'adaptiveThreshold':
                res = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, sz, iters - 7)
                draw_str(res, (10, 20), 'mode: Adaptive Threshold')
    cv2.destroyAllWindows()

'''def draw(colorim, unorderbounds):
    for key in unorderbounds.keys():
        for i in list(unorderbounds[key]):
            colorim[key, i] = [0, 0, 255]
    ##cv2.rectangle(colorim, pt1, pt2, (0, 255, 0), 1)
    return(colorim)
'''


def edit(editim, sizeset):
    h = editim.shape[0]
    if h > 600:
        im = editim[0:600, 0:600]
    else:
        im = editim
    if h in sizeset.keys():
        for i in sizeset[h].keys():
            if i in ['erode/dilate', 'open/close', 'blackhat/tophat']:
                str_mode = 'ellipse'
                (op, sz, iters) = sizeset[h][i]
                str_name = 'MORPH_' + str_mode.upper()
                oper_name = 'MORPH_' + op.upper()
                st = cv2.getStructuringElement(getattr(cv2, str_name), (sz, sz))
                editim = cv2.morphologyEx(editim, getattr(cv2, oper_name), st, iterations=iters) #actually change full size image
            elif i == 'GaussianBlur':
                str_mode = None
                (op, sz, iters) = sizeset[h][i]
                editim = cv2.GaussianBlur(editim, (sz, sz), iters)
                #editim = cv2.bilateralFilter(editim, iters, sz, sz)
            else:
                mode = 'adaptiveThreshold'
                str_mode = None
                (op, sz, iters) = sizeset[h][i]
                editim = cv2.adaptiveThreshold(editim, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, sz, iters - 7)
        return(editim, sizeset)
    else:
        sizeset[h] = {}
        modes = ['erode/dilate', 'open/close', 'blackhat/tophat']
        str_mode = 'ellipse'
        for cur_mode in modes:
            sz, iters, op = trackbar(im, cur_mode, str_mode) #send in im so you can deal with a smaller size image
            str_name = 'MORPH_' + str_mode.upper()
            oper_name = 'MORPH_' + op.upper()
            st = cv2.getStructuringElement(getattr(cv2, str_name), (sz, sz))
            im = cv2.morphologyEx(im, getattr(cv2, oper_name), st, iterations=iters)
            editim = cv2.morphologyEx(editim, getattr(cv2, oper_name), st, iterations=iters) #actually change full size image
            sizeset[h][cur_mode] = (op, sz, iters)

        mode = 'GaussianBlur'
        str_mode = None
        sz, iters, op = trackbar(im, mode, str_mode)
        im = cv2.GaussianBlur(im, (sz, sz), iters)
        #im = cv2.bilateralFilter(im, iters, sz, sz)
        editim = cv2.GaussianBlur(editim, (sz, sz), iters)
        sizeset[h]['GaussianBlur'] = ('GaussianBlur', sz, iters) 

        mode = 'adaptiveThreshold'
        str_mode = None
        sz, iters, op = trackbar(im, mode, str_mode)
        im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, sz, iters - 7)
        editim = cv2.adaptiveThreshold(editim, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, sz, iters - 7)
        sizeset[h]['adaptiveThreshold'] = ('adaptiveThreshold', sz, iters)
        return(editim, sizeset)

###### this is where trackbar.py ends

def shift_dft(src, dst=None):
    '''
          Rearrange the quadrants of Fourier image so that the origin is at
        the image center. Swaps quadrant 1 with 3, and 2 with 4.
        src and dst arrays must be equal size & type
    '''

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
    def __init__(self, width, height, parent = None):
        super().__init__(parent)

        self.width = width
        self.height = height
        
        #self.image = self.image[selected region]
        self.reciprocalIm = image
        self.reciprocalIm = self.reciprocalIm.tolist()
        bytesPerLine = 3 * width
        self.reciprocalIm = QImage(self.reciprocalIm, self.width, self.height, bytesPerLine, QImage.Format_Mono)
        self.reciprocalIm = QPixmap(self.reciprocalIm)
        
        self.label = QLabel()
        self.label.setPixmap(self.reciprocalIm)
        

        

class myApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 350, 300) #sets top left corner of 
        #location on a screen and then the width and height of the box
        self.setWindowTitle("Reciprocal")

        self.initUI()
    
    def initUI(self):
        hbox = QHBoxLayout()
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        
        self.pixmap = QPixmap("qds")
        self.pixmap = self.pixmap.scaled(500, 500, Qt.KeepAspectRatio)
        self.scene.addPixmap(self.pixmap)
        self.view.setScene(self.scene)

        hbox.addWidget(self.view)

        frame = QFrame()

        self.recip = QPushButton("Reciprocal", frame)
        self.recip.setEnabled(True)
        
        self.draw = QPushButton("Select", frame)
        self.draw.setEnabled(False)

        vbox = QVBoxLayout()
        vbox.addWidget(self.recip)
        
        vbox.addWidget(self.draw)

        vbox.addStretch(1)

        frame.setLayout(vbox)
        hbox.addWidget(frame)
        self.setLayout(hbox)

        self.recip.clicked.connect(self.onClick)
        
    def onClick(self):
        self.w = Reciprocal(self.pixmap.width(), self.pixmap.height())
        self.w.setGeometry(200, 200, 500, 500)
        self.w.show()

if __name__ == "__main__":
    image = cv2.imread("qds.tif", 0)
    image = image[0:500, 0:500]
    editim = image
    sizeset = dict() #a dictionary of size of image and the settings for that size area
    
    # editim, sizeset = edit(editim, sizeset)
    # editim, centres2 = COM(editim)
    # editim = justCOM(editi(editim, centres2)
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

    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()

    app = QApplication(sys.argv)
    w = myApp()
    w.show()
    sys.exit(app.exec())