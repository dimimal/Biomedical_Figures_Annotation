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
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()

    def lineAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.pathIds[self.view.lineFigurePath] = 0
        self.view.lineFigurePath = None
        self.view.lineFigureScene.clear()
        self.view.nextLineFigure()

    def barAction(self):
        self.view.pathCrr[self.view.lineFigurePath] = 1
        self.view.pathIds[self.view.lineFigurePath] = 1
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

            # if the figure is unlabeled, enable the line action
            if self.view.pathIds[self.view.barFigurePath] == 2:
                barAction.setEnabled(True)

            menu.addAction(okAction)
            menu.addAction(barAction)
            menu.addAction(voidAction)
            menu.addAction(lineAction)
            menu.exec_(event.screenPos()) 

    def okAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        #self.view.createPixItem(self.view.barFigurePath)
        self.view.barFigurePath = None
        self.view.barFigureScene.clear()
        self.view.nextBarFigure()

    def lineAction(self):
        self.view.pathCrr[self.view.barFigurePath] = 1
        self.view.pathIds[self.view.barFigurePath] = 0
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
    """docstring for LineFigures"""
    def __init__(self, parent=None):
       super(LineFigures, self).__init__(parent)
       self.view        = parent
       self.figuresList = []

    def scale(self, image):
        fx, fy = image.width()/2., image.height()/2.
        scaleMatrix = QtGui.QTransform.fromScale(fx, fy)

    def create(self):
        pass


class BarFigures(QtWidgets.QGraphicsScene):
    """docstring for BarFigures
    """
    def __init__(self, parent=None):
        super(BarFigures, self).__init__(parent)
        self.view        = parent
        self.figuresList = []

    def createItem(self, figurePath):
        self.figureItem = QtWidgets.QGraphicsPixmapItem()
        self.figure = QtGui.QPixmap(figurePath)
        self.scale()
        #self.paint()
        self.figureItem.setPixmap(self.figure)
        self.figuresList.append(self.figureItem)
               
        x, y = self.view.getWidgetPos(self.view.displayBarFigures)
        w, h = self.view.getWidgetDims(self.figure)
        if len(self.figuresList) == 1:
            self.view.displayBarFigures.setGeometry(QtCore.QRect(x,y,w,h))
            self.view.displayBarFigures.fitInView(self.view.barFigures.sceneRect(), QtCore.Qt.IgnoreAspectRatio)
            # set geometry
            self.view.barFigures.addItem(self.figureItem)
        else:
            offset = len(self.figuresList)
            self.view.displayBarFigures.setGeometry(QtCore.QRect(x,y,offset*w,h))
            #self.view.displayBarFigures.fitInView(self.view.barFigures.sceneRect(), QtCore.Qt.IgnoreAspectRatio)
            self.seperator(x,y,w,h)
            self.view.barFigures.addItem(self.figureItem)
            self.figureItem.setPos((offset-1)*w,0)
        #print(self.figuresList)

    def seperator(self, x, y, w, h):
            offset = len(self.figuresList)
            line = QtWidgets.QGraphicsLineItem(x+w,y,x+w,y+h)
            self.view.barFigures.addItem(line)
            self.figureItem.setPos((offset-1)*w,0)    

    def scale(self):
        self.figure = self.figure.scaled(250, 250, 
                            QtCore.Qt.IgnoreAspectRatio, 
                            QtCore.Qt.SmoothTransformation) 
    '''
    def paint(self):
        # Add bounding rectangle here
        picture = QtGui.QPixmap(253,253)
        paint   = QtGui.QPainter(picture)
        #paint.begin()
        paint.setPen(QtGui.QColor(255,34,255))
        paint.drawRect(0,0,253, 253)
        paint.drawPixmap(3,3, self.figure)
        #self.figure = picture #LOLLL       
        paint.end()
    '''
    def deleteItem(self):
        pass

"""
Obsolete, use methods inside scenes!
class FigureItem(QtWidgets.QGraphicsPixmapItem):
    '''Object which holds the properties and methods for each figure in the widget  
    which shows the corrected figures which classified by hand.
    '''

    def __init__(self, figurePath, parent=None):
        print(figurePath, parent)
        super(FigureItem, self).__init__(figurePath, parent)
        self.path   = figurePath
        self.figure = QtGui.QPixmap().load(self.path)
        self.scale()
        self.paint()

    def scale(self):
        self.figure = self.figure.scaled(250, 250, 
                            QtCore.Qt.IgnoreAspectRatio, 
                            QtCore.Qt.SmoothTransformation) 

    def paint(self):
        picture = QtGui.QPixmap(253,253)
        paint   = QtGui.QPainter(picture)
        paint.setPen(QtGui.QColor(255,34,255,255), 3)
        paint.drawRect(0,0,253, 253)
        paint.drawPixmap(3,3, self.figure)
        self.figure = picture #LOLLL
"""

if __name__ == '__main__':
    raise Exception('This module is not executable')
    sys.exit(-1)