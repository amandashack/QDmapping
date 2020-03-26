#### model 
####    the central component of the pattern. it is the applications dynamic data structure, independent of the user interface. It directly manages the data, logic and rules of the application
#### responsible for managing the data of the application. recieves user input from the controller

#### view
####    any representation of information such as a chart, diagram, or table. multiple views of the same information are possible, such as a bar chart for management and a tabular view for accounts
####    presentation of the model in a particular format

#### controller 
####    accepts input and converts it to commands for the model view
####    responds to user input and performs interactions on the data model objects. recieves input, optionally validates it and then passes the input to the model


#### VIEW

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

from palette import Palette
from imageEditTools import ieTools


class MainWindow(QMainWindow):
    def __init__(self, signals, context):
        
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Materials Mapper")
        
        
        self.signals = signals
        self.context = context
        
        #self.myApp = myApp2(self)
        _widget = QWidget()#MainWidget ##### underscore indicates a private or protected variable or method which is intended to be overridden by subclasses
        _layout = QVBoxLayout(_widget)
        
        #_layout.addWidget(self.myApp)
        self.setCentralWidget(_widget)
        self.setGeometry(100, 100, 1300, 750)

        #self.status = self.statusBar()
        self.menuBar = self.createMenuBar()
        self.toolBar = self.createToolBar()
        self.statusBar = self.statusBar()
        self.createDockWidgets()
        
    def newFile(self):
        pass
    
    def openFile(self):
        #self.myApp.setImage()
        pass
        
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

        return(l)
    
    def createViewActions(self):

        ids = ["Zoom_In", "Zoom_Out", "Normal_Size", "Fit_to_Window"]
        #This is where you would add icons in a list
        shortcuts = ['Ctrl+Shift+=', 'Ctrl+Shift+-', 'Ctrl+N', 'Ctrl+Shift+N']
        connects = [self.zoomIn, self.zoomOut, self.normalSize, self.fitToWindow]

        l = []

        for i in range(len(ids)):
            a = QAction(ids[i], self)
            a.setShortcut(shortcuts[i])
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

        return(menubar)

    def createToolBar(self):
        ### this is where icons and actions would be added for drawing, selection and such
        
        toolBar = QToolBar()
        
        
        return(toolBar) 
        
    def createDockWidgets(self):
        
        #Palette widget
        
        self.palette = QDockWidget(self)
        self.palette.setAllowedAreas(Qt.RightDockWidgetArea)
        self.palette.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        
        palette = Palette(self.context, self.signals)
        
        self.palette.setWidget(paletteWidget)
        self.palette.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        
        self.addDockWidget(Qt.RightDockWidgetArea, self.palette)
        
        # image editing widget
        self.ieTools = ieTools(self.context, self.signals)
        self.addDockWidget(Qt.RightDockWidgetArea, self.ieTools)
        self.ieTools.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)

