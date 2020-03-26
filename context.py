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


class Context:
    
    def __init__(self, signals):
        
        self.signals = signals
        
        self.palette = []
		self.defaultPalette = [[14, 53, 75], [0, 76, 115], [18, 121, 174], [49, 162, 238], [136, 199, 234], [27, 52, 43],
							  [30, 85, 55], [69, 145, 26], [121, 191, 29], [190, 222, 44], [69, 18, 18], [113, 31, 31],
							  [184, 37, 53], [220, 81, 115], [255, 159, 182], [39, 20, 67], [105, 28, 99], [173, 81, 185],
							  [184, 152, 208], [53, 48, 36], [89, 66, 40], [140, 92, 77], [208, 128, 112], [229, 145, 49],
							  [247, 176, 114], [252, 215, 142], [0, 0, 0], [33, 33, 33], [79, 79, 79], [179, 179, 179],
							  [255, 255, 255], [37, 42, 46], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
							  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
							  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
							  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
							  [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
	
	def loadDefaults(self):
	    self.loadDefaultPalete()
	
	def loadDefaultPalette(self):
	    
        
    

