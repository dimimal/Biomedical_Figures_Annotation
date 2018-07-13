#! /usr/bin/env python3

from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
#import pyqtgraph  as pg
from sklearn.externals import joblib
#from sklearn.cluster import KMeans

import random 
import sys
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
        
        # Feature Extraction selected by the user
        self.featExtMethod = ''

        self.clusterMethod = ''
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
        folderDialog.setNameFilter('Pkl files (*.pkl)')
        folderDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        fileName   = [] # Returns a list of the directory

        # Check
        if folderDialog.exec_():
            fileName = folderDialog.selectedFiles()
            if self.joblibExt in str(fileName): # if it is a pkl file handle it properly
                self.feats = joblib.load(str(fileName))
            else:
                message = 'Only pkl files'
                self.messageBox(message)

    def initDocks(self):
        """Initialize the docks inside the Main window
        """

        # Define the grid of widgets
        gridLayout = QtWidgets.QGridLayout()      
        #gridLayout.setSpacing(0)
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
        self.lineFigure.load('/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/PMC2585806/pone.0003847.g002.jpg')

        self.lineFigureScene   = QtWidgets.QGraphicsScene()
        self.displayLineFigure = QtWidgets.QGraphicsView(self.lineFigureScene)
        self.lineFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.lineFigure))  

        # Set the text item to plot the label of the figure
        self.lineTextItem = QtWidgets.QGraphicsTextItem()
        self.lineTextItem.setFont(font)
        self.lineTextItem.setPlainText('Line Figure')
        self.lineTextItem.setPos(self.lineFigure.height()/2, -100)

        self.lineFigureScene.addItem(self.lineTextItem)

        # Set the bar figure widget
        self.barFigure = QtGui.QImage()
        self.barFigure.load('/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/PMC2585806/pone.0003847.g002.jpg')
        
        self.barFigureScene   = QtWidgets.QGraphicsScene()
        self.displayBarFigure = QtWidgets.QGraphicsView(self.barFigureScene)
        self.barFigureScene.addPixmap(QtGui.QPixmap.fromImage(self.barFigure))  
        self.barFigureScene.setSceneRect(0,0,256,256)
        #self.displayBarFigure.setSceneRect(0,0,256,256)
        #self.barFigureScene.addText('Bar figure', font)

        # Set the text item to plot the label of the figure
        self.barTextItem = QtWidgets.QGraphicsTextItem()
        self.barTextItem.setFont(font)
        self.barTextItem.setPlainText('Bar Figure')
        self.barTextItem.setPos(self.barFigure.height()/2, -100)

        self.barFigureScene.addItem(self.barTextItem)
        # Add widgets to grid layout        
        gridLayout.addWidget(self.displayLineFigure, 1, 0, QtCore.Qt.AlignLeft)
        gridLayout.addWidget(self.displayBarFigure, 2, 0, QtCore.Qt.AlignLeft)

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

    def paintEvent(self, event):
        """Draw Contour
        """
        """
        qp_1 = QtGui.QPainter()
        qp_1.begin(self.displayLineFigure)
        qp_1.setPen(QtCore.Qt.blue)
        qp_1.setFont(QtGui.QFont('Arial', 30))
        qp_1.drawText(self.displayLineFigure.rect(), QtCore.Qt.AlignCenter, 'Line Figure')
        qp_1.end()
        """
    ''' 
    def toQImage(self, im, copy=False):
        """Transforms a numpy array image to QImage
        """
        if im is None:
            return QtGui.QImage()
        
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                gray_color_table = [qRgb(i, i, i) for i in range(256)]
                qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QtGui.QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QtGui.QImage.Format_ARGB32)
                    return qim.copy() if copy else qim
        
        # Show Error message
        message = 'Inconsistent data type {}'.format(im.dtype)
        self.messageBox(message)
    '''

    # Destructor
    def __del__(self):
        return

if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    tool        = Viewer()
    sys.exit(application.exec_())
