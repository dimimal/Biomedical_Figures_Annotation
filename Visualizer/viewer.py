#! /usr/bin/env python3

from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

from sklearn.externals import joblib

from Utils.utils import (GraphicsLineScene, 
                         GraphicsBarScene, 
                         LineFigures, 
                         BarFigures, 
                         FigureItem)

import random 
import sys
import pandas as pd
import os
import numpy as np
import re

class Viewer(QtWidgets.QMainWindow):
    """The main window of the annotator
    """
    def __init__(self):
        super(Viewer, self).__init__()
        # Image extension
        self.imageExt  = '.jpg'
        self.joblibExt = '.pkl'
        self.csvExt    = '.csv'

        self.pathIds   = {}
        self.pathCrr   = {}
        
        # Set the figgures 
        self.lineFigure = QtGui.QImage()
        self.barFigure  = QtGui.QImage() 
        
        # Hold the path for each figure frame      
        self.barFigurePath  = None
        self.lineFigurePath = None        

        # Instantiate the window
        self.initUI()

    def initUI(self):
        """Initialize the UI 
        """
        self.toolbar = self.addToolBar('Tools')
        self.toolbar.setMovable(False)

        # Add the tool buttons
        iconDir = os.path.join( os.path.dirname(sys.argv[0]) , 'icons' )
        #
        loadAction = QtWidgets.QAction(QtGui.QIcon( os.path.join( iconDir , 'open.png' )), '&Tools', self)
        loadAction.setShortcuts(['o'])
        #
        loadAction.triggered.connect( self.loadPredictions )
        self.toolbar.addAction(loadAction)
        loadAction.setToolTip('Open file')

        # Close the application
        exitAction = QtWidgets.QAction(QtGui.QIcon( os.path.join( iconDir , 'exit.png' )), '&Tools', self)
        exitAction.setShortcuts(['Esc'])
        exitAction.triggered.connect( self.close )
        self.toolbar.addAction(exitAction)
        exitAction.setToolTip('Exit')           

        # Init docked widgets
        self.initDocks()

        # Enable mouse move events
        self.setMouseTracking(True)
        self.toolbar.setMouseTracking(True)
        
        # Open main window in full screen
        self.showFullScreen()
        
        # Show
        self.show()

    def initDocks(self):
        """Initialize the docks inside the Main window
        """
        # Define the grid of widgets
        gridLayout = QtWidgets.QGridLayout()      
        gridLayout.setOriginCorner(QtCore.Qt.TopLeftCorner)
        
        # Set QWidget object as main window in order to develop the 
        # appropriate functions
        widget = QtWidgets.QWidget(self)
        widget.setLayout(gridLayout)
        self.setCentralWidget(widget)
        
        gridLayout.setColumnMinimumWidth(1, 200) 
        gridLayout.setRowMinimumHeight(2, 200)
        gridLayout.setRowMinimumHeight(4, 200)

        # Set the text font 
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)        
        
        # Add figure widget scenes
        self.lineFigureScene = GraphicsLineScene()
        self.barFigureScene  = GraphicsBarScene()

        # Init view windows
        self.displayLineFigure = QtWidgets.QGraphicsView()
        self.displayBarFigure  = QtWidgets.QGraphicsView()
        
        self.displayLineFigure.setScene(self.lineFigureScene)
        self.displayBarFigure.setScene(self.barFigureScene)

        # Initialize the classification scenes 
        self.lineFigures = LineFigures()
        self.barFigures  = BarFigures()
        self.displayLineFigures = QtWidgets.QGraphicsView(self.lineFigures)
        self.displayBarFigures  = QtWidgets.QGraphicsView(self.barFigures)

        self.lineFigures.setItemIndexMethod(QtWidgets.QGraphicsScene.BspTreeIndex)
        self.barFigures.setItemIndexMethod(QtWidgets.QGraphicsScene.BspTreeIndex)
        
        # Define text widgets 
        lineText = QtWidgets.QLabel()
        lineText.setFont(font)
        lineText.setText('Line Figure')
        #
        barText = QtWidgets.QLabel()
        barText.setFont(font)
        barText.setText('Bar Figure')        
        
        # Add widgets to grid layout
        gridLayout.addWidget(lineText, 1, 0, 1, -1, QtCore.Qt.AlignHCenter)
        gridLayout.addWidget(barText, 3, 0, 1, -1, QtCore.Qt.AlignHCenter)
        #
        gridLayout.addWidget(self.displayLineFigure, 2, 0, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayBarFigure, 4, 0, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayLineFigures, 2, 1, 1, -1, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayBarFigures, 4, 1, 1, -1, QtCore.Qt.AlignLeft)

        gridLayout.setHorizontalSpacing(70)
        gridLayout.setVerticalSpacing(15)

        # Usefull to arrange the size of each widget
        print(QtWidgets.QDesktopWidget().screenGeometry())

        """
        tmp_1 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.lineFigure))
        tmp_2 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.barFigure))

        self.lineFigures.addItem(tmp_1)        
        self.lineFigures.addItem(tmp_2)
        tmp_2.setPos(tmp_1.boundingRect().width(), 0)
        tmp_2.setScale(0.5)
        """
        #self.displayLineFigures.fitInView(self.lineFigures.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def loadPredictions(self):
        """Load the joblib file which contains the dictionary of 
        predictions
        """

        dir_path     = os.path.dirname(os.path.realpath(__file__))
        message      = 'Select csv file' 
        folderDialog = QtWidgets.QFileDialog(self, message, dir_path)
        folderDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        #folderDialog.setNameFilter('Pkl files (*.pkl)')
        folderDialog.setNameFilter('CSV files (*.csv)')
        folderDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        fileName   = [] # Returns a list of the directory
        
        # Plot the window to select the csv file
        if folderDialog.exec_():
            fileName = folderDialog.selectedFiles()
            if self.csvExt in str(fileName):
                self.loadCsv(str(fileName[0]))
            else:
                message = 'Only csv files'
                self.messageBox(message)
                return

        self.selectFigures()
        
    def loadCsv(self, file):
        data = pd.read_csv(file, header=None, names=['path', 'id', 'corrected'])
        self.pathIds = data.set_index('path').to_dict()['id']
        self.pathCrr = data.set_index('path').to_dict()['corrected']
    
    def nextLineFigure(self):
        for path, cid in self.pathCrr.items():
            if cid == 0 and self.pathIds[path] == 0:
                self.plotFigures(path)
                break
            elif cid == 0 and self.pathIds[path] == 2:
                self.plotFigures(path)
                break


    def nextBarFigure(self):
        for path, cid in self.pathCrr.items():
            if cid == 0 and self.pathIds[path] == 1:
                self.plotFigures(path)
                break 
            elif cid == 0 and self.pathIds[path] == 2:
                self.plotFigures(path)
                break

    def selectFigures(self):
        # Go through figures that they have not been
        # classified manually 
        for path, cid in self.pathCrr.items():
            if cid == 0 and self.pathIds[path] == 0:
                self.plotFigures(path)
                break
            elif cid == 0 and self.pathIds[path] == 2:
                self.plotFigures(path)
                break
        for path, cid in self.pathCrr.items():
            if cid == 0 and self.pathIds[path] == 1:
                self.plotFigures(path)
                break
            elif cid == 0 and self.pathIds[path] == 2:
                self.plotFigures(path)
                break

    def getWidgetPos(self, widget):
        return widget.x(), widget.y() 

    def getWidgetDims(self, widget):
        return widget.width(), widget.height()

    def createPixItem(self, figure):
        self.figureItem = FigureItem(figure)
        self.lineFigures.addPixmap(self.figureItem.figure) # Wtf??

    def plotFigures(self, path):
        if self.pathIds[path] == 0:
            self.lineFigurePath = path
            self.lineFigure.load(path)
            self.lineFigure = self.lineFigure.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            # TODO:: ### handle low resolution images ######
            self.lineFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.lineFigure))
            x, y = self.getWidgetPos(self.displayLineFigure)
            w, h = self.getWidgetDims(self.lineFigure) 
            self.displayLineFigure.setGeometry(QtCore.QRect(x,y,w,h))
            self.displayLineFigure.fitInView(x,y,w,h, QtCore.Qt.KeepAspectRatio)
        elif self.pathIds[path] == 1:
            self.barFigurePath = path
            self.barFigure.load(path)
            self.barFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.barFigure))
            self.barFigure = self.barFigure.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
            x, y = self.getWidgetPos(self.displayBarFigure)
            w, h = self.getWidgetDims(self.barFigure)
            self.displayBarFigure.setGeometry(QtCore.QRect(x,y,w,h))  
            self.displayBarFigure.fitInView(self.barFigureScene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)
        else:
            if self.barFigurePath is None:
                self.barFigurePath = path
                self.barFigure.load(path)
                self.barFigure = self.barFigure.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                self.barFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.barFigure))
                x, y = self.getWidgetPos(self.displayBarFigure)
                w, h = self.getWidgetDims(self.barFigure)
                self.displayBarFigure.setGeometry(QtCore.QRect(x,y,w,h))    
                self.displayBarFigure.fitInView(self.barFigureScene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)
            elif self.lineFigurePath is None:
                self.lineFigurePath = path
                self.lineFigure.load(path)
                self.lineFigure = self.lineFigure.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                self.lineFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.lineFigure))
                x, y = self.getWidgetPos(self.displayLineFigure)
                w, h = self.getWidgetDims(self.lineFigure)
                self.displayLineFigure.setGeometry(QtCore.QRect(x,y,w,h))  
                self.displayLineFigure.fitInView(self.lineFigureScene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)

    def messageBox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        event.accept()

    def displayHelpMessage(self):
        """Help message box
        """
        QtWidgets.QMessageBox.about(self, "This is the help message box")
        self.update()

    # Destructor
    def __del__(self):
        return

                         
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    view        = Viewer()
    sys.exit(application.exec_())
