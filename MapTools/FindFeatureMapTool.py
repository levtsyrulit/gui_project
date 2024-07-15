from PyQt5.QtCore import pyqtSignal
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsMapToolEmitPoint, QgsMapTool, QgsMapToolIdentify

class FindFeatureMapTool(QgsMapToolEmitPoint):
    finished = pyqtSignal(QgsMapToolIdentify.IdentifyResult)
    canceled = pyqtSignal()

    def __init__(self, canvas):
        self.canvas = canvas
        self.findIdentity = QgsMapToolIdentify(self.canvas)
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.points = []
        self.identifyResultList = None
        self.identifyResultObject = None

    def canvasPressEvent(self, e):
        if e.button() == Qt.LeftButton:
            point = e.pixelPoint()

            self.identifyResultList = self.findIdentity.identify(point.x(), point.y(), self.canvas.layers())
            if (len(self.identifyResultList) > 0):
                self.finished.emit(self.identifyResultList[0])

        elif e.button() == Qt.RightButton:
            self.canceled.emit()

    def deactivate(self):
        QgsMapTool.deactivate(self)
        self.deactivated.emit()



