from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMapMouseEvent
from qgis.core import QgsWkbTypes, QgsPointXY
from PyQt5.QtCore import pyqtSignal

class OldPointMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(list)
    canceled = pyqtSignal()

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)  
        self.points = []

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.points.append(point)
            self.finished.emit(self.points)
        elif e.button() == Qt.RightButton:
            self.canceled.emit()    

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()