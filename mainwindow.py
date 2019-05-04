import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time

import toolLabeler
from mainWidget import mainWidget

class Signals(QObject):

    autoUpdateTool = pyqtSignal([int])
    updateTool = pyqtSignal([int])
        

class MainWindow(QMainWindow):

    def __init__(self, signals):

        super(MainWindow, self).__init__()

        self.signals = signals

        self.resize(800,480)
        self.setWindowTitle("Materials Mapper")
	
        self.statusBar = self.statusBar()
        self.menuBar = self.createMenuBar()
        self.toolBar = self.createToolBar()
        self.createDockWidgets()

        self.ctrlPressed = False

        self.mainWidget = MainWidget(signals, self)
        self.setCentralWidget(self.mainWidget)

        self.imagePosLabel = QLabel() #this may need to be changed if this is where the image is going
        self.imagePosLabel.setObjectName("ImagePosLabel")

        self.signals.autoUpdateTool.connect(self.setCurrentTool)
        self.signals.enterCanvas.connect(self.showImagePosition)
        self.signals.leaveCanvas.connect(self.hideImagePosition)
        self.signals.overCanvas.connect(self.setImagePosition)

    def createToolBar(self):

        toolbar = QToolbar()
        l = self.createToolBarActions()
    
    def createToolBarActions(self):

        l = []

        self.tools = QActionGroup(self)
        tools = ["reciprocal selector", "zoom selector", "drawing", "ruler"]
        # #connects = [lambda: self.context.changeCurrentTool(toolLabeler.Tools.recip),
        #                     lambda: self.context.changeCurrentTool(toolLabeler.Tools.zoom),
        #                     lambda: self.context.changeCurrentTool(toolLabeler.Tools.drawing),
        #                     lambda: self.context.changeCurrentTool(toolLabeler.Tools.ruler)]
        #shortcuts = ['z', 'x', 'c', 'a']
        return(l)
    
    def setCurrentTool(self, index):

        self.tools.actions()[0].setChecked(True) #returns the list of this groups actions
        self.signals.updateTool.emit(0)
    
    def createFileActions(self):

        ids = ["new", "open", "save", "saveas", "exit"]
        #This is where you would add icons in a list
        shortcuts = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl+Shift+S', 'Ctrl+Q']
        connects = [self.newFile, self.openFile, self.saveFile, self.saveFileAs, self.close]

        l = []

        for i in range(len(ids)):
            a = QAction(ids[i], self)
            a.setShortcut(shortcuts[i])
            a.triggered.connect(self.restoreFocus) ###### ask developer about this
            a.setStatusTip(ids[i])
            if connects[i] != 0: a.triggered.connect(connects[i])
            l.append(a)
        
        l.insert(4, 0)

        return(l)


    def createMenuBar(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("Menu", "File")#self.context.getText("menu", "file")) #This is because of language setting
        editMenu = menubar.addMenu("Menu", "Edit")
        viewMenu = menubar.addMenu("Menu", "View")
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
        
    def restoreFocus(self):
        print("Restoring Focus")
        self.ctrlPressed = False
        self.releaseMouse()
        self.releaseKeyboard()
        QCoreApplication.instance().restoreOverrideCursor()
        #### here is where you would connect the tools to an icon once you have those selected

if __name__ == "main":
    app = QApplication(sys.argv)

    signals = Signals()

    w = MainWindow(signals)
    w.show()
    sys.exit(app.exec_())