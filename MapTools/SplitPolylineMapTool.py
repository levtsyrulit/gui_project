import math
from PyQt5.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsMapTool, QgsMapToolIdentify, QgsSnapIndicator, QgsMapMouseEvent
from qgis.core import QgsPointLocator, QgsTolerance, QgsPointXY, QgsGeometry, QgsFeature, QgsPoint, QgsMapLayer, QgsGeometryUtils, QgsSnappingConfig
from ..Helpers.MessageBoxHelper import MessageBoxHelper

class SplitPolylineMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal()

    def __init__(self, canvas):
        self.canvas = canvas
        self.findIdentity = QgsMapToolIdentify(self.canvas)
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.points = []
        self.layer = None
        self.identifyResultList = None
        self.__turnOnSnapping(canvas)

    def __turnOnSnapping(self, canvas):
        self.snapper = self.canvas.snappingUtils()
        self.snapIndicator = QgsSnapIndicator(canvas)
        self.oldConfig = self.snapper.config()
        newConfig = QgsSnappingConfig(self.snapper.config())
        sTypes = QgsSnappingConfig.SnappingTypes(1 and 2)
        newConfig.setTypeFlag(sTypes)
        self.snapper.setConfig(newConfig)
        if not self.oldConfig.enabled():
            self.snapper.toggleEnabled()

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = e.pixelPoint()
            self.identifyResultList = self.findIdentity.identify(point.x(), point.y(), self.canvas.layers())
            if self.identifyResultList != [] and self.identifyResultList[0].mLayer.geometryType() == 1:
                self.layer = self.identifyResultList[0].mLayer
                self.__analyseObjectsList(self.identifyResultList, self.snapIndicator.match().point())
                self.finished.emit()

        elif e.button() == Qt.RightButton:
            self.snapper.setConfig(self.oldConfig)
            self.finished.emit()

    def canvasMoveEvent(self, e):
        snapMatch = self.snapper.snapToMap(e.pos())
        self.snapIndicator.setMatch(snapMatch)

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()

    def __analyseObjectsList(self, objectsList, point):
        amountOfFeatures = 0
        featureToSplit = None
        featurePoints = []
        for object in objectsList:
            if object.mFeature.geometry().type() == 1:
                amountOfFeatures += 1
                if amountOfFeatures > 1:
                    MessageBoxHelper.showThereAreManyPolylinesMessageBox(self)
                    return
                featureToSplit = object.mFeature
                featurePoints = featureToSplit.geometry().asMultiPolyline()[0]

        if self.snapIndicator.match().point() in featurePoints:
            self.__perfomVertexSplit(featureToSplit, point, self.layer)
        else:
            self.__perfomSegmentSplit(featureToSplit, featurePoints, point, self.layer)

        self.snapper.setConfig(self.oldConfig)

    def __perfomVertexSplit(self, featureToSplit, splittingPoint, layer : QgsMapLayer):
        vertices = featureToSplit.geometry().asMultiPolyline()[0]
        pointListFeature1 = []
        pointListFeature2 = []
        splittingPointIsPassed = False

        for point in vertices:
            if point == splittingPoint:
                pointListFeature1.append(point)
                pointListFeature2.append(point)
                splittingPointIsPassed = True
            elif not splittingPointIsPassed:
                pointListFeature1.append(point)
            else:
                pointListFeature2.append(point)

        self.__addNewFeatures(featureToSplit, pointListFeature1, pointListFeature2, layer)

    def __perfomSegmentSplit(self, featureToSplit, featurePoints, point, layer : QgsMapLayer):
        segmentNumber = featureToSplit.geometry().closestSegmentWithContext(point)[2]
        segmentPoint1 = QgsPointXY(featurePoints[segmentNumber - 1].x(), featurePoints[segmentNumber -1].y())

        vertices = featureToSplit.geometry().asMultiPolyline()[0]
        pointListFeature1 = []
        pointListFeature2 = []
        splittingPointIsPassed = False

        for p in vertices:
            if p == segmentPoint1:
                pointListFeature1.append(p)
                pointListFeature1.append(point)
                pointListFeature2.append(point)
                splittingPointIsPassed = True
            elif not splittingPointIsPassed:
                pointListFeature1.append(p)
            else:
                pointListFeature2.append(p)

        self.__addNewFeatures(featureToSplit, pointListFeature1, pointListFeature2, layer)

    def __addNewFeatures(self, featureToSplit, pointListFeature1, pointListFeature2, layer):
        layer.dataProvider().changeGeometryValues({featureToSplit.id(): QgsGeometry.fromPolylineXY(pointListFeature1)})
        newFeature = QgsFeature(layer.fields())
        newFeature.setGeometry(QgsGeometry.fromPolylineXY(pointListFeature2))
        newFeature.setAttributes(featureToSplit.attributes())
        newFeature.setAttribute("ID", None)
        (created, outFeatures) = layer.dataProvider().addFeatures([newFeature])
        self.layer.reload()
        self.canvas.refresh()






