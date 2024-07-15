from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMapMouseEvent, QgsSnapIndicator
from qgis.core import QgsWkbTypes, QgsPointXY
from PyQt5.QtCore import pyqtSignal

class PointMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(list)
    canceled = pyqtSignal()

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapper = self.canvas.snappingUtils()
        self.points = []

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.snapIndicator.match().type():
                point = self.snapIndicator.match().point()
            else:
                point = self.toMapCoordinates(e.pos())
            self.points.append(point)
            self.finished.emit(self.points)
        elif e.button() == Qt.RightButton:
            self.canceled.emit()

    def canvasMoveEvent(self, e):
        snapMatch = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snapMatch)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()