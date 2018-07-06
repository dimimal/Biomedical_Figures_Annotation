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
        
        # should be omitted in the future
        self.loadFigure()

        # Instantiate the window
        self.initUI()

    def loadFigure(self):
        """Loads figure for debug purposes only
        """
        path = '/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/PMC1949492/pone.0000796.e001.jpg'
        self.figure = imread(path)

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

        self.initDocks()
        # Open main window in full screen
        self.showFullScreen()
        # Show
        self.show()

    def loadPredictions(self):
        """Load the joblib file which contains the dictionary of 
        predictions
        """
        dir_path    = os.path.dirname(os.path.realpath(__file__))
        #dir_path     = '/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/' # For development purposes only
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
        
        self.lineFigure = QtGui.QImage()
        #self.lineFigureWidget = QtWidgets.QWidget()
        label = QtGui.QLabel()
        label.setLayout()



        gridLayout.addWidget(self.lineFigureWidget, 0, 0, 1, 1)
        # Initialize the docks to show the figures that will be
        # corrected by the user
        #self.lineFigureDock = QtWidgets.QDockWidget()
        #self.lineFigureDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        #self.lineFigureDock.setFloating(False)
        #self.lineFigureDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        #self.lineFigureDock.setWidget(QtWidgets.QWidget(QtGui.QPixmap(QtGui.QImage(self.figure, self.figure.shape[0], 
        #            self.figure.shape[1], self.figure.shape[1]*3, QtGui.QImage.Format_RGB888))))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.lineFigureDock)        
        #
        self.barFigureDock = QtWidgets.QDockWidget()
        self.barFigureDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.barFigureDock.setFloating(False)
        self.barFigureDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.barFigureDock)
        #
        # The classification docks are initialized below
        self.lineClassificationDock = QtWidgets.QDockWidget()
        self.lineClassificationDock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.lineClassificationDock.setFloating(False)
        self.lineClassificationDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.lineClassificationDock)
        #self.lineClassificationDock.setWidget()
        # 
        self.barClassificationDock = QtWidgets.QDockWidget()
        self.barClassificationDock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.barClassificationDock.setFloating(False)
        self.barClassificationDock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.barClassificationDock)

    def loadFigures(self):
        """load the figures from path to numpy array?
        """
        pass

    def featureExtraction(self):
        """Contains feature extraction techniques selected by the user 
        to use them along with a clustering method
        """

        counter = 0 
        for file in self.figures:
            if counter == 10: break
            image = imread(file)
            feats = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualize=False) 
            break
            counter += 1
            if self.features.size == 0:
                self.features = feats.flatten()
            else:
                self.features.concatenate(feats.flatten(), axis=0)

    '''
    def clustering(self):
        """Contains the clustering algorithms for usage (e.g K-means)
        TODO: Probably will be removed
        """
        kmeans = KMeans(n_clusters=2, random_state=0).fit(self.features)
    '''

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

    def toQImage(self, im, copy=False):
        """Transforms a numpy image to QImage
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

    # Destructor
    def __del__(self):
        return

        

def main():
    """Main function, call the constructor to do the job
    """
    application = QtWidgets.QApplication(sys.argv)
    tool        = Viewer()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
