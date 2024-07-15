from qgis.PyQt.QtCore import Qt
from qgis.core import QgsRectangle, QgsPointXY, QgsWkbTypes, QgsVectorLayer, QgsFeatureRequest, QgsProject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapToolIdentify, QgsMapTool

class ViewDataSourceMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(dict)
    canceled = pyqtSignal()

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.startPoint = None
        self.endPoint = None
        self.rubberband = QgsRubberBand(self.canvas, QgsWkbTypes.PolygonGeometry)
        self.rubberband.setColor(QColor(255, 218, 185, 120))
        self.rubberband.setWidth(1)
        self.selectedFeatures = {}
        self.iface.messageBar().pushMessage("Выберите объекты полигоном")

    def __del__(self):
        self.deactivate()

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if not self.startPoint:
                self.startPoint = self.toMapCoordinates(e.pos())
            elif not self.endPoint:
                self.endPoint = self.toMapCoordinates(e.pos())
                self.__selectFeatures()
                self.__resetRubberBand()
                self.finished.emit(self.selectedFeatures)
        elif e.button() == Qt.RightButton:
            self.__resetRubberBand()
            self.canceled.emit()

    def canvasMoveEvent(self, e):
        if self.startPoint and not self.endPoint:
            self.tmpEndPoint = self.toMapCoordinates(e.pos())
            self.__showRect(self.startPoint, self.tmpEndPoint)

    def __showRect(self, startPoint, endPoint):
        self.rubberband.reset(QgsWkbTypes.PolygonGeometry)
        self.rubberband.addPoint(QgsPointXY(startPoint), False)
        self.rubberband.addPoint(QgsPointXY(startPoint.x(), endPoint.y()), False)
        self.rubberband.addPoint(QgsPointXY(endPoint), False)
        self.rubberband.addPoint(QgsPointXY(endPoint.x(), startPoint.y()), True)
        self.rubberband.show()

    def __resetRubberBand(self):
        self.rubberband.reset(QgsWkbTypes.GeometryType.PolygonGeometry)

    def __selectFeatures(self):
        rectGeom = self.rubberband.asGeometry()
        for layer in QgsProject.instance().mapLayers().values():
            selectedFeatures = [f for f in layer.getFeatures() if rectGeom.intersects(f.geometry()) ]
            if selectedFeatures != []:
                self.selectedFeatures[layer] = selectedFeatures

    def deactivate(self):
        self.__resetRubberBand()
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

