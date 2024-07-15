from PyQt5.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint,  QgsRubberBand, QgsMapToolIdentify, QgsMapTool
from qgis.core import QgsPointXY, QgsGeometry, QgsFeature, QgsPoint, QgsWkbTypes
from ..Helpers.MessageBoxHelper import MessageBoxHelper

class SplitPolygonMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal()

    def __init__(self, canvas, featureToSplit, layer):
        self.featureToSplit = featureToSplit
        self.splittingPolylineGeometry = None
        self.canvas = canvas
        self.findIdentity = QgsMapToolIdentify(self.canvas)
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QgsWkbTypes.GeometryType.LineGeometry)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.inProgress = False
        self.points = []
        self.layer = layer
        self.identifyResultList = None

    def reset(self):
        self.points = []
        self.inProgress = False
        self.rubberBand.reset(QgsWkbTypes.GeometryType.LineGeometry)

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = self.toMapCoordinates(e.pos())
            self.inProgress = True
            self.points.append(point)
        elif e.button() == Qt.RightButton:
            points = self.points
            self.reset()
            if len(points) > 1:
                self.splittingPolylineGeometry = QgsGeometry.fromPolylineXY(points)
                self.__splitPolygon(self.featureToSplit, self.layer)
            self.finished.emit()

    def canvasMoveEvent(self, e):
        if not self.inProgress:
            return
        endPoint = self.toMapCoordinates(e.pos())
        self.showPolyline(self.points, endPoint)

    def showPolyline(self, points, endPoint):
        self.rubberBand.reset(QgsWkbTypes.GeometryType.LineGeometry)
        for point in points:
            self.rubberBand.addPoint(point, False)
        self.rubberBand.addPoint(endPoint, True)
        self.rubberBand.show()

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def __splitPolygon(self, feature, layer):
        layer.deselect([feature.id()])
        if feature.geometry().contains(self.splittingPolylineGeometry.asPolyline()[0]) or feature.geometry().contains(self.splittingPolylineGeometry.asPolyline()[-1]) or feature.geometry().intersects(self.splittingPolylineGeometry) == False:
            MessageBoxHelper.showDrawnLineDoesntIntersectPolygonMessageBox(self)
            return

        splittingLinePoints = []
        for point in self.splittingPolylineGeometry.asPolyline():
            splittingLinePoints.append(QgsPointXY(point))

        result, new_geometries, point_xy = feature.geometry().splitGeometry(splitLine=splittingLinePoints,topological=False, splitFeature=False)
        layer.dataProvider().changeGeometryValues({feature.id(): new_geometries[0]})
        new_geometries.pop(0)
        for geometry in new_geometries:
            newFeature = QgsFeature(layer.fields())
            newFeature.setGeometry(geometry)
            newFeature.setAttributes(feature.attributes())
            newFeature.setAttribute("ID", None)
            (created, outFeatures) = layer.dataProvider().addFeatures([newFeature])
            self.layer.reload()
            self.canvas.refresh()





