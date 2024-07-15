from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMapMouseEvent
from qgis.core import QgsWkbTypes, QgsPointXY
from PyQt5.QtCore import pyqtSignal

class OldPolygonMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(list)
    canceled = pyqtSignal()

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.PolygonGeometry)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.points = []
        self.inProgress = False
        self.reset()

    def reset(self):
        self.points = []
        self.inProgress = False        
        self.rubberBand.reset(QgsWkbTypes.GeometryType.PolygonGeometry)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.inProgress = True
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            points = self.points
            self.reset()        
            if len(points) > 1:        
                self.finished.emit(points)
            else:
                self.canceled.emit()

    def canvasMoveEvent(self, e):
        if not self.inProgress:
            return

        endPoint = self.toMapCoordinates(e.pos())
        self.showPolyline(self.points, endPoint)

    def showPolyline(self, points, endPoint):
        self.rubberBand.reset(QgsWkbTypes.GeometryType.PolygonGeometry)

        for point in points:
            self.rubberBand.addPoint(point, False)
            
        self.rubberBand.addPoint(endPoint, True)    # true to update canvas
        self.rubberBand.show()

    def deactivate(self):
        self.rubberBand.reset(QgsWkbTypes.GeometryType.PolygonGeometry)
        QgsMapTool.deactivate(self)
        self.deactivated.emit()