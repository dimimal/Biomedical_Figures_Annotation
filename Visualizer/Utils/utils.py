from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
import sys

class GraphicsLineScene(QtWidgets.QGraphicsScene):
    """class which holds the qgraphics scene widget about line graphs along with 
    its own methods
    """
    def __init__(self, parent=None):
        super(GraphicsLineScene, self).__init__(parent)
        self.view = parent

    def contextMenuEvent(self, event):
        if event.reason() == event.Mouse and self.view.lineFigurePath is not None:
            event.accept()
            menu       = QtWidgets.QMenu()
            okAction   = QtWidgets.QAction('Ok', self)
            barAction  = QtWidgets.QAction('Bar Chart', self)
            lineAction = QtWidgets.QAction('Line Chart', self)            
            voidAction = QtWidgets.QAction('Unlabeled Chart', self)

            okAction.triggered.connect(self.okAction)
            barAction.triggered.connect(self.barAction)
            voidAction.triggered.connect(self.voidAction)
            lineAction.triggered.connect(self.lineAction)
            
            lineAction.setEnabled(False)
            
            if self.view.pathIds[self.view.lineFigurePath] == 2:
                lineAction.setEnabled(True)

            menu.addAction(okAction)
            menu.addAction(barAction)
            menu.addAction(voidAction)
            menu.addAction(lineAction)
            menu.exec_(event.screenPos())

    def okAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.lineFigures.createItem(self.view.lineFigurePath)
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()

    def lineAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.pathIds[self.view.lineFigurePath] = 0
        self.view.lineFigures.createItem(self.view.lineFigurePath)
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()

    def barAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.pathIds[self.view.lineFigurePath] = 1
        self.view.barFigures.createItem(self.view.lineFigurePath)       
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()

    def voidAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.pathIds[self.view.lineFigurePath] = 2
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()


class GraphicsBarScene(QtWidgets.QGraphicsScene):
    """GraphicsBarScene class
    """
    def __init__(self, parent=None):
        super(GraphicsBarScene, self).__init__(parent)
        self.view = parent

    def contextMenuEvent(self, event):
        if event.reason() == event.Mouse and self.view.barFigurePath is not None:
            event.accept()
            menu = QtWidgets.QMenu()
            okAction   = QtWidgets.QAction('Ok', self)
            barAction  = QtWidgets.QAction('Bar Chart', self)
            lineAction = QtWidgets.QAction('Line Chart', self)            
            voidAction = QtWidgets.QAction('Unlabeled Chart', self)

            okAction.triggered.connect(self.okAction)
            lineAction.triggered.connect(self.lineAction)
            voidAction.triggered.connect(self.voidAction)
            barAction.triggered.connect(self.barAction)
            
            barAction.setEnabled(False)

            # if the figure is unlabeled, enable the bar action
            if self.view.pathIds[self.view.barFigurePath] == 2:
                barAction.setEnabled(True)

            menu.addAction(okAction)
            menu.addAction(barAction)
            menu.addAction(voidAction)
            menu.addAction(lineAction)
            menu.exec_(event.screenPos()) 

    def okAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        self.view.barFigures.createItem(self.view.barFigurePath)
        self.view.barFigurePath = None
        self.view.barFigureScene.clear()
        self.view.nextBarFigure()

    def lineAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        self.view.pathIds[self.view.barFigurePath] = 0
        self.view.lineFigures.createItem(self.view.barFigurePath)       
        self.view.barFigurePath = None
        self.view.barFigureScene.clear()
        self.view.nextBarFigure()

    def barAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        self.view.pathIds[self.view.barFigurePath] = 1
        self.view.barFigures.createItem(self.view.barFigurePath)
        self.view.barFigurePath = None
        self.view.barFigureScene.clear()
        self.view.nextBarFigure()   

    def voidAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        self.view.pathIds[self.view.barFigurePath] = 2
        self.view.barFigurePath = None
        self.view.barFigureScene.clear()
        self.view.nextBarFigure()


class LineFigures(QtWidgets.QGraphicsScene):
    """docstring for LineFigures
    """
    def __init__(self, parent=None):
        super(LineFigures, self).__init__(parent)
        self.view        = parent
        self.figuresList = []
        
        # The fixed size of single figure scene
        self.scaleX     = 280
        self.scaleY     = 400

    def createItem(self, figurePath):
        self.figureItem = QtWidgets.QGraphicsPixmapItem()
        self.figure = QtGui.QPixmap(figurePath)
        self.scale()
        self.paint()
        self.figureItem.setPixmap(self.figure)
        self.figuresList.append(self.figureItem)
               
        x, y = self.view.getWidgetPos(self.view.displayLineFigures)
        w, h = self.view.getWidgetDims(self.figure)
        if len(self.figuresList) == 1:
            # Set scene geometry
            self.view.displayLineFigures.setGeometry(QtCore.QRect(x,y,w,h))
            self.view.lineFigures.addItem(self.figureItem)
        else:
            offset = len(self.figuresList)
            self.arrangeScene(x, y, w, h, offset)
            self.view.lineFigures.addItem(self.figureItem)
            self.figureItem.setPos((offset-1)*w,0)
    
    def arrangeScene(self, x, y, w, h, offset):
        if x+offset*w > self.view.screenWidth:
            self.view.displayLineFigures.translate(w,0)
        else:
            self.view.displayLineFigures.setGeometry(QtCore.QRect(x,y,offset*w,h))

    def scale(self):
        self.figure = self.figure.scaled(self.scaleX, self.scaleY, 
                            QtCore.Qt.IgnoreAspectRatio, 
                            QtCore.Qt.SmoothTransformation) 
    
    def paint(self):
        # Add bounding frame here
        color   = (182,182,182)
        width   = 3
        picture = QtGui.QPixmap(
                    self.figure.width()+2*width,
                    self.figure.height()+2*width)

        paint   = QtGui.QPainter(picture)
        pen     = QtGui.QPen(QtGui.QColor(*color))
        pen.setWidth(width)
        paint.setPen(pen)
        paint.drawRect(0, 0, self.figure.width()+1, self.figure.height()+1)
        paint.drawPixmap(width-1,width-1, self.figure)
        self.figure = picture
        paint.end()

class BarFigures(QtWidgets.QGraphicsScene):
    """docstring for BarFigures scene
    """
    def __init__(self, parent=None):
        super(BarFigures, self).__init__(parent)
        self.view        = parent
        self.figuresList = []
        
        # The fixed size of single figure scene
        self.scaleX     = 280
        self.scaleY     = 400

    def createItem(self, figurePath):
        self.figureItem = QtWidgets.QGraphicsPixmapItem()
        self.figure = QtGui.QPixmap(figurePath)
        self.scale()
        self.paint()
        self.figureItem.setPixmap(self.figure)
        self.figuresList.append(self.figureItem)
               
        x, y = self.view.getWidgetPos(self.view.displayBarFigures)
        w, h = self.view.getWidgetDims(self.figure)
        if len(self.figuresList) == 1:
            # Set scene geometry
            self.view.displayBarFigures.setGeometry(QtCore.QRect(x,y,w,h))
            self.view.barFigures.addItem(self.figureItem)
        else:
            offset = len(self.figuresList)
            self.arrangeScene(x, y, w, h, offset)
            self.view.barFigures.addItem(self.figureItem)
            self.figureItem.setPos((offset-1)*w,0)
    
    def arrangeScene(self, x, y, w, h, offset):
        if x+offset*w > self.view.screenWidth:
            self.view.displayBarFigures.translate(w,0)
        else:
            self.view.displayBarFigures.setGeometry(
                QtCore.QRect(x,y,offset*w,h))

    def scale(self):
        self.figure = self.figure.scaled(self.scaleX, self.scaleY, 
                            QtCore.Qt.IgnoreAspectRatio, 
                            QtCore.Qt.SmoothTransformation) 
    
    def paint(self):
        # Add bounding frame here
        color  = (182,182,182)
        width   = 3
        picture = QtGui.QPixmap(
                    self.figure.width()+2*width,
                    self.figure.height()+2*width)

        paint   = QtGui.QPainter(picture)
        pen     = QtGui.QPen(QtGui.QColor(*color))
        pen.setWidth(width)
        paint.setPen(pen)
        paint.drawRect(0, 0, self.figure.width()+1, self.figure.height()+1)
        paint.drawPixmap(width-1,width-1, self.figure)
        self.figure = picture        
        paint.end()

if __name__ == '__main__':
    raise Exception('This module is not executable')
    sys.exit(-1)