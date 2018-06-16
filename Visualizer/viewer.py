#! /usr/bin/python
from __future__ import print_function

from PyQt4 import QtGui
from PyQt4 import QtCore
import pyqtgraph  as pg
from sklearn.externals import joblib

import random 
import sys
import glob
import os
import numpy as np
import re
# Load Opencv to make resizes 
import cv2 as cv
# matplotlib for colormaps
from matplotlib import pyplot as plt

class Viewer(QtGui.QMainWindow):
    """The main window of the annotator
    """
    def __init__(self):
        super(Viewer, self).__init__()
        # Image extension
        self.imageExt = '.jpg'
        self.image    = QtGui.QImage()
        self.folder   = ''
        # Lis of paths of the figures
        self.figures  = []
        self.pg       = pg.GraphicsLayout()
        #self.w1 = self.pg.addPlot(row=0, col=0, title = 'Data1')
        #self.w2 = self.pg.addPlot(row=1, col=2, title = 'Data2')

        # Instantiate the window
        self.initUI()

    def initUI(self):
        """Initialize the UI 
        """
        self.toolbar = self.addToolBar('Tools')
        
        # Close the application
        exitAction = QtGui.QAction(QtGui.QIcon( os.path.join( os.path.dirname(sys.argv[0]) , 'exit.png' )), '&Tools', self)
        exitAction.setShortcuts(['Esc'])
        #self.setTip( exitAction, 'Exit' )
        exitAction.triggered.connect( self.close )
        self.toolbar.addAction(exitAction)

        # Add the tool buttons
        iconDir = os.path.join( os.path.dirname(sys.argv[0]) , 'icons' )

        # Loading a new city
        loadAction = QtGui.QAction(QtGui.QIcon( os.path.join( iconDir , 'open.png' )), '&Tools', self)
        loadAction.setShortcuts(['o'])
        #
        loadAction.triggered.connect( self.getFigures )
        self.toolbar.addAction(loadAction)

        #self.pg.GraphicsLayout()
        #self.pg       = pg.PlotWidget(np.arange(0,100,1))
        self.pg.addLayout()
        # Open main window in full screen
        self.showFullScreen()
        
        self.show()

    def getFigures(self):
        #dir_path     = os.path.dirname(os.path.realpath(__file__))
        dir_path     = '/media/dimitris/TOSHIBA EXT/Image_Document_Classification/PMC-Dataset/'
        message      = 'Select Folder ' 
        folderDialog = QtGui.QFileDialog(self, message, dir_path)#.(self, message, dir_path, QtGui.QFileDialog.DirectoryOnly )
        folderDialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        folderName   = QtCore.QStringList() # Returns a list of the directory

        if folderDialog.exec_():
            folderName = folderDialog.selectedFiles()

        if folderName.isEmpty():
            message = 'Please, select a directory that includes jpg image files or joblib file'
            self.messageBox(message)
        else:
            directory = str(folderName[0])
            # Iterate the directory and return the paths of the figures
            if os.path.isdir(directory):
                for subdir, dirs, files in os.walk(directory):
                    for file in files:
                        if self.imageExt in file:
                            self.figures.append(os.path.join(subdir,file))
            if not self.figures:
                message = 'jpg image files not found in path: '+ directory
                self.messageBox(message)
            else:
                self.loadFigures()

    def loadFigures(self):
        pass

    def messageBox(self, message):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(message)
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        event.accept()

    def displayHelpMessage(self):
        """Help message box
        """
        QtGui.QMessageBox.about(self, "This is the help message box")
        self.update()

    # Destructor
    def __del__(self):
        return

        

def main():
    """Main function, call the constructor to do the job
    """
    application = QtGui.QApplication(sys.argv)
    tool        = Viewer()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()