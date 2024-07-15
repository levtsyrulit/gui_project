import math
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool, QgsMapMouseEvent, QgsSnapIndicator
from qgis.core import QgsWkbTypes
from PyQt5.QtCore import pyqtSignal, QPoint

class RotationPointMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(list, int)
    canceled = pyqtSignal()

    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.snapper = self.canvas.snappingUtils()
        self.points = []
        self.iface.messageBar().pushMessage("Укажите точку вставки")
        self.endPoint = None

        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.LineGeometry)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.rubberBand.setLineStyle(Qt.DashLine)

        self.rubberBandStart = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.LineGeometry)
        self.rubberBandStart.setColor(Qt.red)
        self.rubberBandStart.setWidth(3)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.points == []:
                if self.snapIndicator.match().type():
                    point = self.snapIndicator.match().point()
                else:
                    point = self.toMapCoordinates(e.pos())
                self.points.append(point)
                self.iface.messageBar().pushMessage("Укажите угол поворота для объекта")
            else:
                self.finished.emit([self.points[0]], self.__getAngle(e))
                self.__resetRubberBands()
        elif e.button() == Qt.RightButton:
            self.__resetRubberBands()
            self.canceled.emit()

    def __getAngle(self, e):
        anglePoint = self.toMapCoordinates(e.pos())
        angleParam = math.degrees(math.atan2(anglePoint.y() - self.points[0].y(), anglePoint.x() - self.points[0].x())) * (-1)
        return angleParam if angleParam > 0 else 180 + (180 + angleParam)

    def canvasMoveEvent(self, e):
        snapMatch = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snapMatch)
        self.endPoint = self.toMapCoordinates(e.pos())
        self.__showRubberBand(self.points, self.endPoint)
        if self.points != []:
            self.__showRubberBandStart(e)

    def __showRubberBandStart(self, e):
        objectLength = 20

        mousePoint = e.pos()
        insertPoint = self.toCanvasCoordinates(self.points[0])

        dx = mousePoint.x() - insertPoint.x()
        dy = mousePoint.y() - insertPoint.y()

        lineLength = math.sqrt(dx ** 2 + dy ** 2)            

        x = 0 if lineLength == 0 else (objectLength * dy / lineLength)
        y = objectLength if lineLength == 0 else (-1 * objectLength * dx / lineLength)

        point1 = self.toMapCoordinates(QPoint(insertPoint.x() + x, insertPoint.y() + y))
        point2 = self.toMapCoordinates(QPoint(insertPoint.x() - x, insertPoint.y() - y))

        self.rubberBandStart.reset(QgsWkbTypes.GeometryType.LineGeometry)
        self.rubberBandStart.addPoint(point1, False)
        self.rubberBandStart.addPoint(point2, True)
        self.rubberBandStart.show()

    def __showRubberBand(self, points, endPoint):
        self.rubberBand.reset(QgsWkbTypes.GeometryType.LineGeometry)
        for point in points:
            self.rubberBand.addPoint(point, False)
        self.rubberBand.addPoint(endPoint, True)
        self.rubberBand.show()

    def __resetRubberBands(self):
        self.rubberBand.reset(QgsWkbTypes.GeometryType.LineGeometry)
        self.rubberBandStart.reset(QgsWkbTypes.GeometryType.LineGeometry)

    def deactivate(self):
        self.__resetRubberBands()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()