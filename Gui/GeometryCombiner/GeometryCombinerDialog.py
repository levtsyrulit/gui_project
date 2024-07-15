import os
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from PyQt5 import QtCore
from ...MapTools.FindFeatureMapTool import FindFeatureMapTool
from ...Helpers.MessageBoxHelper import MessageBoxHelper
from qgis.core import QgsWkbTypes

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'GeometryCombinerDialog.ui'))

class GeometryCombinerDialog(QtWidgets.QDialog, FORM_CLASS):
    closingDlg = pyqtSignal()
    def __init__(self, iface, parent=None):
        super(GeometryCombinerDialog, self).__init__(parent)

        self.setupUi(self)
        self.setModal(True)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.mapTool = None
        self.majorLayer = None
        self.minorLayer = None
        self.majorFeature = None
        self.minorFeature = None

        self.__removeSelection()

        self.buttonCenterMajorElement.setEnabled(False)
        self.buttonCenterMinorElement.setEnabled(False)
        self.buttonCombine.setEnabled(False)

        self.buttonChooseMajorElement.clicked.connect(self.__btnChooseMajorElementClicked)
        self.buttonCenterMajorElement.clicked.connect(self.__centerMajorElement)

        self.buttonChoseMinorElement.clicked.connect(self.__btnChooseMinorElementClicked)
        self.buttonCenterMinorElement.clicked.connect(self.__centerMinorElement)

        self.buttonCombine.clicked.connect(self.__combineElements)
        self.buttonCancel.clicked.connect(self.__closeDlg)

        self.show()
    def closeEvent(self, event):
        self.closingDlg.emit()

    def __closeDlg(self):
        self.canvas.unsetMapTool(self.mapTool)
        self.__removeSelection()
        self.close()

    def __removeSelection(self):
        for layer in self.canvas.layers():
            layer.removeSelection()

    def __btnChooseMajorElementClicked(self):
        if self.majorLayer != None:
            self.majorLayer.deselect(self.majorFeature.id())
        self.mapTool = FindFeatureMapTool(self.canvas)
        self.mapTool.finished.connect(self.__chooseMajorElementFinished)
        self.mapTool.canceled.connect(self.__chooseElementCancel)
        self.canvas.setMapTool(self.mapTool)
        self.hide()

    def __chooseMajorElementFinished(self, identifyResult):
        self.canvas.unsetMapTool(self.mapTool)
        self.majorLayer = identifyResult.mLayer
        self.majorFeature = identifyResult.mFeature
        text = "ID: " + str(self.majorFeature.id()) + ". Слой: " + str(self.majorLayer.name())
        self.tbMajorElement.setText(text)
        self.majorLayer.select(self.majorFeature.id())
        self.buttonCenterMajorElement.setEnabled(True)
        self.__enableCombineButtonCheck()
        self.show()

    def __centerMajorElement(self):
        self.__removeSelection()
        self.majorLayer.select(self.majorFeature.id())
        self.canvas.zoomToSelected()
        self.buttonCenterMajorElement.setChecked(False)
        if self.minorLayer != None:
            self.minorLayer.select(self.minorFeature.id())

    def __btnChooseMinorElementClicked(self):
        if self.minorLayer != None:
            self.minorLayer.deselect(self.minorFeature.id())
        self.mapTool = FindFeatureMapTool(self.canvas)
        self.mapTool.finished.connect(self.__chooseMinorElementFinished)
        self.mapTool.canceled.connect(self.__chooseElementCancel)
        self.canvas.setMapTool(self.mapTool)
        self.hide()

    def __chooseMinorElementFinished(self, identifyResult):
        self.canvas.unsetMapTool(self.mapTool)
        self.minorLayer = identifyResult.mLayer
        self.minorFeature = identifyResult.mFeature
        text = "ID: " + str(self.minorFeature.id()) + ". Слой: " + str(self.minorLayer.name())
        self.tbMinorElement.setText(text)
        self.minorLayer.select(self.minorFeature.id())
        self.buttonCenterMinorElement.setEnabled(True)
        self.__enableCombineButtonCheck()
        self.show()

    def __centerMinorElement(self):
        self.__removeSelection()
        self.minorLayer.select(self.minorFeature.id())
        self.canvas.zoomToSelected()
        self.buttonCenterMinorElement.setChecked(False)
        if self.majorLayer != None:
            self.majorLayer.select(self.majorFeature.id())

    def __enableCombineButtonCheck(self):
        if self.majorFeature != None and self.minorFeature != None:
            self.buttonCombine.setEnabled(True)

    def __analyseType(self):
        if self.majorFeature.geometry().type() == 1:
            return 1
        if self.majorFeature.geometry().type() == 2:
            return 2
        return 0

    def __combineElements(self):
        if self.majorFeature.id() == self.minorFeature.id():
            MessageBoxHelper.showTheSameElementsWereChoosenMessageBox(self)
            return
        elif self.majorLayer != self.minorLayer:
            MessageBoxHelper.showChoosenElementsLayerIsDifferentMessageBox(self)
            return

        geometryType = self.__analyseType()

        if geometryType == 1:
            self.__analyseMultiLineCombination()
        elif geometryType == 2:
            self.__analysePolygonCombination()
        else:
            MessageBoxHelper.showThisTypeOfGeometryIsNotSupported(self)

    def __analyseMultiLineCombination(self):
        if not self.__checkIfPolylineElementsEndsMatch(self.majorFeature.geometry().asMultiPolyline(),
                                                       self.minorFeature.geometry().asMultiPolyline()):
            MessageBoxHelper.showChoosenElementsEndsDontMatchMessageBox(self)
            return None
        self.__perfomCombination()

    def __analysePolygonCombination(self):
        if not self.__checkIfPolygonlElementsIntersect(self.majorFeature, self.minorFeature):
            MessageBoxHelper.showChoosenPolygonsDontInstersect(self)
            return None
        self.__perfomCombination()

    def __checkIfPolylineElementsEndsMatch(self, majorFeatureCoordinates, minorFeatureCoordinates):
        if majorFeatureCoordinates[0][0] == minorFeatureCoordinates[0][0] or majorFeatureCoordinates[0][0] == \
                minorFeatureCoordinates[0][-1] or majorFeatureCoordinates[0][-1] == minorFeatureCoordinates[0][0] or \
                majorFeatureCoordinates[0][-1] == minorFeatureCoordinates[0][-1]:
            return True
        return False

    def __checkIfPolygonlElementsIntersect(self, majorFeature, minorFeature):
        if majorFeature.geometry().intersects(minorFeature.geometry()):
            return True
        return False

    def __perfomCombination(self):
        self.iface.setActiveLayer(self.majorLayer)
        self.iface.activeLayer().startEditing()
        newGeometry = self.majorFeature.geometry().combine(self.minorFeature.geometry())
        self.minorLayer.deleteFeatures([self.minorFeature.id()])
        self.majorFeature.setGeometry(newGeometry)
        self.majorLayer.updateFeature(self.majorFeature)
        self.canvas.refresh()
        self.canvas.unsetMapTool(self.mapTool)
        self.iface.activeLayer().commitChanges()
        self.majorLayer.triggerRepaint()
        self.close()

    def __chooseElementCancel(self):
        self.canvas.unsetMapTool(self.mapTool)
        self.mapTool = None


