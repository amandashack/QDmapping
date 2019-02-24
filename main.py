# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\proxi\OneDrive\Desktop\project\QDmap\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QPainter, QPen
#from tools.py import drawingTool


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(997, 750)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.realSpace = QtWidgets.QWidget()
        self.realSpace.setObjectName("realSpace")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.realSpace)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(self.realSpace)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.scrollArea = QtWidgets.QScrollArea(self.splitter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 904, 138))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ogImageScene = QGraphicsScene()
        self.ogImage = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents_2)
        self.ogImage.setObjectName("ogImage")
        self.horizontalLayout.addWidget(self.ogImage)
        self.ogImage.setScene(self.ogImageScene)
        self.imageMapScene = QGraphicsScene()
        self.imageMap = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents_2)
        self.imageMap.setObjectName("imageMap")
        self.horizontalLayout.addWidget(self.imageMap)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.tabWidget_2 = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(240)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setFixedHeight(200)
        self.classifyTab = QtWidgets.QWidget()
        self.classifyTab.setObjectName("classifyTab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.classifyTab)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(self.classifyTab)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.pushButton = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_4 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter_3 = QtWidgets.QSplitter(self.classifyTab)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.splitter_3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_8 = QtWidgets.QPushButton(self.splitter_3)
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout.addWidget(self.splitter_3)
        self.splitter_4 = QtWidgets.QSplitter(self.classifyTab)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.splitter_4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_6 = QtWidgets.QPushButton(self.splitter_4)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_9 = QtWidgets.QPushButton(self.splitter_4)
        self.pushButton_9.setObjectName("pushButton_9")
        self.verticalLayout.addWidget(self.splitter_4)
        self.tabWidget_2.addTab(self.classifyTab, "")
        self.configTab = QtWidgets.QWidget()
        self.configTab.setObjectName("configTab")
        self.tabWidget_2.addTab(self.configTab, "")
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.tabWidget.addTab(self.realSpace, "")
        self.reciprocalSpace = QtWidgets.QWidget()
        self.reciprocalSpace.setObjectName("reciprocalSpace")
        self.tabWidget.addTab(self.reciprocalSpace, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 997, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuedit = QtWidgets.QMenu(self.menuBar)
        self.menuedit.setObjectName("menuedit")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_As.setIcon(icon)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionPrint = QtWidgets.QAction(MainWindow)
        self.actionPrint.setObjectName("actionPrint")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionZoom_In = QtWidgets.QAction(MainWindow)
        self.actionZoom_In.setObjectName("actionZoom_In")
        self.actionZoom_Out = QtWidgets.QAction(MainWindow)
        self.actionZoom_Out.setObjectName("actionZoom_Out")
        self.actionNormal_Size = QtWidgets.QAction(MainWindow)
        self.actionNormal_Size.setObjectName("actionNormal_Size")
        self.actionFit_to_Window = QtWidgets.QAction(MainWindow)
        self.actionFit_to_Window.setObjectName("actionFit_to_Window")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionLasso = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/iconfinder_select_lasso_64630.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLasso.setIcon(icon1)
        self.actionLasso.setObjectName("actionLasso")
        self.actioncircle = QtWidgets.QAction(MainWindow)
        self.actioncircle.setObjectName("actioncircle")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuedit.addAction(self.actionZoom_In)
        self.menuedit.addAction(self.actionZoom_Out)
        self.menuedit.addAction(self.actionNormal_Size)
        self.menuedit.addSeparator()
        self.menuedit.addAction(self.actionFit_to_Window)
        self.menuView.addAction(self.actionCopy)
        self.menuView.addAction(self.actionPaste)
        self.menuHelp.addAction(self.actionAbout)
        self.menuTools.addAction(self.actionLasso)
        self.menuTools.addAction(self.actioncircle)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuedit.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.mainToolBar.addAction(self.actionSave_As)
        self.mainToolBar.addAction(self.actionLasso)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.image = QPixmap()
        self.pixmap = QPixmap()
        self.viewer = photoViewer(self.ogImage, self.ogImageScene, 600, 600)
        
        self.actionZoom_In.triggered.connect(self.handleZoomIn)
        self.actionZoom_Out.triggered.connect(self.handleZoomOut)
        self.actionNormal_Size.triggered.connect(self.handleNormalSize)
        self.actionOpen.triggered.connect(self.setImage)
        
        #self.ogImage.mousePressEvent = drawingTool.mousePressEvent(self, event)
        #self.ogImage.mouseMoveEvent = drawingTool.mouseMoveEvent(self, event)
        #self.ogImage.mouseReleaseEvent = drawingTool.mouseReleaseEvent(self, event)
        #self.ogImage.paintEvent = drawingTool.paintEvent(self, event)
        
        self.drawing = False
        self.lastPoint = QtCore.QPoint()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_4.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_7.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_8.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_9.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.classifyTab), _translate("MainWindow", "classify"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.configTab), _translate("MainWindow", "configure"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.realSpace), _translate("MainWindow", "Real"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.reciprocalSpace), _translate("MainWindow", "Reciprocal"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuedit.setTitle(_translate("MainWindow", "View"))
        self.menuView.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionOpen.setText(_translate("MainWindow", "Open.."))
        self.actionSave_As.setText(_translate("MainWindow", "Save As.."))
        self.actionPrint.setText(_translate("MainWindow", "Print.."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_Out.setText(_translate("MainWindow", "Zoom Out"))
        self.actionNormal_Size.setText(_translate("MainWindow", "Normal Size"))
        self.actionFit_to_Window.setText(_translate("MainWindow", "Fit to Window"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionLasso.setText(_translate("MainWindow", "Lasso"))
        self.actioncircle.setText(_translate("MainWindow", "circle"))
    
    def setImage(self):
         
         fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "select Image", "", "Image Files (*.png *.jpg *jpg *.bmp)")
         if fileName:
             self.image = QPixmap(fileName) ###### self.image holds the original image at all times
             self.pixmap = self.viewer.setDefaultImage(self.image)
             
             

    def handleZoomIn(self):
        self.pixmap = self.viewer.zoomIn(self.pixmap)
    
    def handleZoomOut(self):
        self.pixmap = self.viewer.zoomOut(self.pixmap)
    
    def handleNormalSize(self):
        self.pixmap = self.viewer.zeroZoom(self.pixmap)

             
        

class photoViewer(object):
    def __init__(self, ogImage, ogImageScene, width, height):
        self.ogImage = ogImage
        self.ogImageScene = ogImageScene
        self._zoom = 0
        self._width = width
        self._height = height

    def setDefaultImage(self, image):
        self.image = image
        pixmap = self.scale(self._width, self._height)
        self.updatePixmap(pixmap)
        return(pixmap)

    def updatePixmap(self, pixmap):
        self.ogImageScene.clear()
        self.ogImageScene.addPixmap(pixmap)
        self.ogImageScene.setSceneRect(QtCore.QRectF(0.0, 0.0, pixmap.width(), pixmap.height()))

    def scale(self, width, height):
        if (self.image.isNull()):
            return(QPixmap())
        return(self.image.scaled(width, height, QtCore.Qt.KeepAspectRatio))

    def zoom(self, pixmap, factor):
        pixmap = self.scale(pixmap.width()*factor, pixmap.height()*factor)
        self.updatePixmap(pixmap)
        return(pixmap)
        
    def zoomIn(self, pixmap):
        self._zoom += 1
        factor = 1.25
        return(self.zoom(pixmap, factor))
    
    def zoomOut(self, pixmap):
        if self._zoom == 0:
            return(pixmap)
        self._zoom -= 1
        factor = 0.75
        return(self.zoom(pixmap, factor))
    
    def zeroZoom(self, pixmap):
        if self._zoom == 0:
            return(pixmap)
        pixmap = self.scale(self._width, self._height) #### self.pixmap is used for scaling and anything else
        self.updatePixmap(pixmap)
        return (pixmap)

        


import resource

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
