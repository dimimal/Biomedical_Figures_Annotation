#! /usr/bin/env python3

from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
#import pyqtgraph  as pg
from sklearn.externals import joblib
#from sklearn.cluster import KMeans

import random 
import sys
import pandas as pd
#import glob
import os
import numpy as np
import re

# skimage for image processing 
from skimage.feature import hog
from skimage.io import imread 

class Viewer(QtWidgets.QMainWindow):
    """The main window of the annotator
    """
    def __init__(self):
        super(Viewer, self).__init__()
        # Image extension
        self.imageExt  = '.jpg'
        self.joblibExt = '.pkl'
        self.image     = QtGui.QImage()
        self.folder    = ''
        self.features  = np.array([])

        self.pathIds   = {}
        self.pathCrr   = {}
        
        # Lis of paths of the figures
        self.figures       = []
        
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

    def loadPredictions(self):
        """Load the joblib file which contains the dictionary of 
        predictions
        """

        dir_path     = os.path.dirname(os.path.realpath(__file__))
        #dir_path    = '/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/' # For development purposes only
        message      = 'Select pkl file' 
        folderDialog = QtWidgets.QFileDialog(self, message, dir_path)
        folderDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        #folderDialog.setNameFilter('Pkl files (*.pkl)')
        folderDialog.setNameFilter('CSV files (*.csv)')
        folderDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        fileName   = [] # Returns a list of the directory

        
        # Check
        if folderDialog.exec_():
            fileName = folderDialog.selectedFiles()
            #if self.joblibExt in str(fileName): # if its a pkl file handle it properly
            #    self.feats = joblib.load(str(fileName))
            if '.csv' in str(fileName):
                self.loadCsv(str(fileName[0]))
            else:
                message = 'Only pkl files'
                self.messageBox(message)
        
    def loadCsv(self, file):
        data = pd.read_csv(file, header=None, names=['path', 'id', 'corrected'])

        self.pathIds = data.set_index('path').to_dict()['id']
        self.pathCrr = data.set_index('path').to_dict()['corrected']
    
    def selectFigures(self):
        pass    

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
        

        # Set the text font 
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        
        
        # Set the line figure widget 
        self.lineFigure = QtGui.QImage()
        # The loading should be handled by another method obviously
        self.lineFigure.load('/media/dimitris/TOSHIBA EXT/\
            Image_Document_Classification/PMC-Dataset/PMC1949492/pone.0000796.g002.jpg')
        #self.lineFigure.load('/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/PMC3792043/pone.0077405.g005.jpg')
        self.lineFigureScene   = GraphicsLineScene()
        
        #self.lineFigureScene   = QtWidgets.QGraphicsScene()
        self.displayLineFigure = QtWidgets.QGraphicsView(self.lineFigureScene)
        self.lineFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.lineFigure))  
        self.displayLineFigure.fitInView(self.lineFigureScene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)

        # Set the text item to plot the label of the figure
        self.lineTextItem = QtWidgets.QGraphicsTextItem()
        self.lineTextItem.setFont(font)
        self.lineTextItem.setPlainText('Line Figure')
        self.lineTextItem.setPos(self.lineFigure.width()/2, -100)

        # Set the bar figure widget
        self.barFigure = QtGui.QImage()
        self.barFigure.load('/media/dimitris/TOSHIBA EXT/\
            Image_Document_Classification/PMC-Dataset/PMC3792043/pone.0077405.g005.jpg')        
        #self.barFigureScene   = QtWidgets.QGraphicsScene()
        self.barFigureScene = GraphicsBarScene()
        self.displayBarFigure = QtWidgets.QGraphicsView(self.barFigureScene)
        self.barFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.barFigure))  
        self.displayBarFigure.fitInView(self.barFigureScene.sceneRect(), QtCore.Qt.IgnoreAspectRatio)

        # Set the text item to plot the label of the figure
        self.barTextItem = QtWidgets.QGraphicsTextItem()
        self.barTextItem.setFont(font)
        self.barTextItem.setPlainText('Bar Figure')
        self.barTextItem.setPos(self.barFigure.width()/2, -100)

        # Add items to scene
        self.lineFigureScene.addItem(self.lineTextItem)
        self.barFigureScene.addItem(self.barTextItem)
        
        # Initialize the classification scenes 
        self.lineFigures = LineFigures()
        self.barFigures  = BarFigures()
        self.displayLineFigures = QtWidgets.QGraphicsView(self.lineFigures)
        self.displayBarFigures  = QtWidgets.QGraphicsView(self.barFigures)

        self.lineFigures.setItemIndexMethod(QtWidgets.QGraphicsScene.BspTreeIndex)
        self.barFigures.setItemIndexMethod(QtWidgets.QGraphicsScene.BspTreeIndex)
        
        # Add widgets to grid layout
        gridLayout.addWidget(self.displayLineFigure, 1, 0, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayBarFigure, 2, 0, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayLineFigures, 1, 1, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayBarFigures, 2, 1, QtCore.Qt.AlignLeft)

        gridLayout.setHorizontalSpacing(100)
        gridLayout.setVerticalSpacing(50)

        tmp_1 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.lineFigure))
        tmp_2 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(self.barFigure))

        self.lineFigures.addItem(tmp_1)        
        self.lineFigures.addItem(tmp_2)
        tmp_2.setPos(tmp_1.boundingRect().width(), 0)
        tmp_2.setScale(0.5)
        
        #self.displayLineFigures.fitInView(self.lineFigures.sceneRect(), QtCore.Qt.KeepAspectRatio)


    def savePkl(self):
        """Save using joblib package
        """
        pass
    
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

class GraphicsLineScene(QtWidgets.QGraphicsScene):
    """class which holds the qgraphics scene widget about line graphs along with 
    its own methods
    """
    def __init__(self, parent=None):
        super(GraphicsLineScene, self).__init__(parent)
        
    def contextMenuEvent(self, event):
        if event.reason() == event.Mouse:
            event.accept()
            menu       = QtWidgets.QMenu()
            okAction   = QtWidgets.QAction('Ok', self)
            barAction  = QtWidgets.QAction('Bar Chart', self)
            lineAction = QtWidgets.QAction('Line Chart', self)            
            voidAction = QtWidgets.QAction('Unlabeled Chart', self)

            okAction.triggered.connect(self.okAction)
            barAction.triggered.connect(self.barAction)
            voidAction.triggered.connect(self.voidAction)
            lineAction.setEnabled(False)

            menu.addAction(okAction)
            menu.addAction(barAction)
            menu.addAction(voidAction)
            menu.addAction(lineAction)
            menu.exec_(event.screenPos())

    def okAction(self):
        pass

    def barAction(self):
        pass

    def voidAction(self):
        pass

class GraphicsBarScene(QtWidgets.QGraphicsScene):
    """GraphicsBarScene class
    """
    def __init__(self, parent=None):
        super(GraphicsBarScene, self).__init__(parent)
    
    def contextMenuEvent(self, event):
        if event.reason() == event.Mouse:
            event.accept()
            menu = QtWidgets.QMenu()
            okAction   = QtWidgets.QAction('Ok', self)
            barAction  = QtWidgets.QAction('Bar Chart', self)
            lineAction = QtWidgets.QAction('Line Chart', self)            
            voidAction = QtWidgets.QAction('Unlabeled Chart', self)

            okAction.triggered.connect(self.okAction)
            lineAction.triggered.connect(self.lineAction)
            voidAction.triggered.connect(self.voidAction)
            barAction.setEnabled(False)

            menu.addAction(okAction)
            menu.addAction(barAction)
            menu.addAction(voidAction)
            menu.addAction(lineAction)
            menu.exec_(event.screenPos()) 

    def okAction(self):
        pass

    def lineAction(self):
        pass   

    def voidAction(self):
        pass

class LineFigures(QtWidgets.QGraphicsScene):
    """docstring for LineFigures"""
    def __init__(self, parent=None):
       super(LineFigures, self).__init__(parent)

    def scale(self, image):
        fx, fy = image.width()/2., image.height()/2.
        scaleMatrix = QtGui.QTransform.fromScale(fx,fy)


class FigureItem(QtWidgets.QGraphicsItem):
    """Object which holds the properties and methods for the figures in the classified 
    section of the widget"""

    def __init__(self, arg):
        super(FigureItem, self).__init__()
        #self.scale()

    def scale(self):
        pass
    

                      
class BarFigures(QtWidgets.QGraphicsScene):
    """docstring for BarFigures"""
    def __init__(self, parent=None):
        super(BarFigures, self).__init__(parent)
    

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    tool        = Viewer()
    sys.exit(application.exec_())
