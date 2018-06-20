#! /usr/bin/python
#from __future__ import print_function

from PyQt5 import QtWidgets, QtGui#QMainWindow, QApplication, QAction, QFileDialog
from PyQt5 import QtCore
#import pyqtgraph  as pg
from sklearn.externals import joblib
from sklearn.cluster import KMeans

import random 
import sys
import glob
import os
import numpy as np
import re
# Load Opencv to make resizes 
from skimage.feature import hog
from skimage.io import imread 

#import cv2 as cv
# matplotlib for colormaps
#from matplotlib import pyplot as plt

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

        # Loading a new city
        loadAction = QtWidgets.QAction(QtGui.QIcon( os.path.join( iconDir , 'open.png' )), '&Tools', self)
        loadAction.setShortcuts(['o'])
        #
        loadAction.triggered.connect( self.getFigures )
        self.toolbar.addAction(loadAction)
        loadAction.setToolTip('Open file')

        # Select feature extraction method 
        selectFeatures = QtWidgets.QAction(QtGui.QIcon( os.path.join( iconDir , 'feats.png' )), '&Tools', self)

        # Close the application
        exitAction = QtWidgets.QAction(QtGui.QIcon( os.path.join( iconDir , 'exit.png' )), '&Tools', self)
        exitAction.setShortcuts(['Esc'])
        exitAction.triggered.connect( self.close )
        self.toolbar.addAction(exitAction)
        exitAction.setToolTip('Exit')           

        # Open main window in full screen
        self.showFullScreen()
        self.show()
        
    def initDocks(self):
    	# Inititalize Dock window( move into method!)
        self.dock       = QtWidgets.QDockWidget()
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.dock.setWidget(self.plotWidget)
        self.dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dock.setFloating(False)
        self.dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)

    def getFigures(self):
        #dir_path     = os.path.dirname(os.path.realpath(__file__))
        dir_path     = '/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/'
        message      = 'Select Folder or pkl file' 
        folderDialog = QtWidgets.QFileDialog(self, message, dir_path)#.(self, message, dir_path, QtGui.QFileDialog.DirectoryOnly )
        folderDialog.setFileMode(QtWidgets.QFileDialog.Directory)
        folderDialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        folderName   = [] # Returns a list of the directory

        # If the folderdialog enabled 
        if folderDialog.exec_():
            folderName = folderDialog.selectedFiles()

        if not folderName:
            message = 'Please, select a directory that includes jpg image files or joblib file'
            self.messageBox(message)
        else:
            if self.joblibExt in str(folderName): # if it is a pkl file handle it properly
                self.data = joblib.load(str(folderName))

            else:
                directory = str(folderName[0])
                # Iterate the directory and return the paths of the figures
                if os.path.isdir(directory):
                    for subdir, dirs, files in os.walk(directory):
                        for file in files:
                            if self.imageExt in file:
                                self.figures.append(os.path.join(subdir,file))
                    self.featureExtraction()# Debug only
                if not self.figures:
                    message = 'jpg image files not found in path: '+ directory
                    self.messageBox(message)
                else:
                    self.loadFigures()#directory)

    def loadFigures(self):
        """load the figures from path to an numpy array?
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

        '''For pyqtGraph only
        self.plotWidget.addItem(self.features)
        self.plotWidget.addPlot(row=1, col=0)
        self.plotWidget.plotItem(self.features)
		'''
    def clustering(self):
        """Contains the clustering algorithms for usage (e.g K-means)
        TODO: Add more Clustering options
        """
        kmeans = KMeans(n_clusters=2, random_state=0).fit(self.features)


    def savePkl(self):
        pass
    
    def messageBox(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        #
        event.accept()

    def displayHelpMessage(self):
        """Help message box
        """
        QtWidgets.QMessageBox.about(self, "This is the help message box")
        self.update()

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