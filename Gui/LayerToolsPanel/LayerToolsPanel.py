# -*- coding: utf-8 -*-
"""
/***************************************************************************
 HelloWorldDockWidget
                                 A QGIS plugin
 Test description
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-06-23
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Comptentit
        email                : info@competentit.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys

from PyQt5.QtWidgets import QDialog, QPushButton
from qgis.PyQt import QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSignal
from qgis.gui import QgsMapToolIdentify
from qgis.core import QgsProject

from ...Helpers.LayerNames import LayerNames
from ..GeometryCombiner.GeometryCombinerDialog import GeometryCombinerDialog

from ...MapTools.FindFeatureMapTool import FindFeatureMapTool
from ...MapTools.SplitPolylineMapTool import SplitPolylineMapTool
from ...MapTools.SplitPolygonMapTool import SplitPolygonMapTool
from ..GasNetwork.GasNetworkMainDialog import GasNetworkMainDialog
from ..GasSupplyObjects.GasSupplyObjectsMainDialog import GasSupplyObjectsMainDialog
from ..GasSupplyPoints.GasSupplyPointsMainDialog import GasSupplyPointsMainDialog
from ..WastewaterNetworks.WastewaterNetworksMainDialog import WastewaterNetworksMainDialog
from ..WastewaterObjects.WastewaterObjectMainDialog import WastewaterObjectMainDialog
from ..WastewaterPoints.WastewaterPointsMainDialog import WastewaterPointsMainDialog
from ..WaterSupplyNetworks.WaterSupplyNetworksMainDialog import WaterSupplyNetworksMainDialog
from ..WaterSupplyPoints.WaterSupplyPointsMainDialog import WaterSupplyPointsMainDialog
from ..WaterSupplyObjects.WaterSupplyObjectsMainDialog import WaterSupplyObjectsMainDialog
from ..ElectricitySupplyNetworks.ElectricitySupplyNetworksMainDialog import ElectricitySupplyNetworksMainDialog
from ..ElectricitySupplyPoints.ElectricitySupplyPointsMainDialog import ElectricitySupplyPointsMainDialog
from ..ElectricitySupplyObjects.ElectricitySupplyObjectsMainDialog import ElectricitySupplyObjectsMainDialog
from ..HeatSupplyNetworks.HeatSupplyNetworksMainDialog import HeatSupplyNetworksMainDialog
from ..HeatSupplyObjects.HeatSupplyObjectsMainDialog import HeatSupplyObjectsMainDialog
from ..HeatSupplyPoints.HeatSupplyPointsMainDialog import HeatSupplyPointsMainDialog
from ..CommunicationNetworks.CommunicationNetworksMainDialog import CommunicationNetworksMainDialog
from ..CommunicationObjects.CommunicationObjectsMainDialog import CommunicationObjectsMainDialog
from ..CommunicationPoints.CommunicationPointsMainDialog import CommunicationPointsMainDialog
from ..MagistralPipelinesNetworks.MagistralPipelinesNetworksMainDialog import MagistralPipelinesNetworksMainDialog
from ..LiquidHydrocarbonsNetworks.LiquidHydrocarbonsNetworksMainDialog import LiquidHydrocarbonsNetworksMainDialog
from ..LiquidHydrocarbonsObjects.LiquidHydrocarbonsObjectsMainDialog import LiquidHydrocarbonsObjectsMainDialog
from ..LiquidHydrocarbonsPoints.LiquidHydrocarbonsPointsMainDialog import LiquidHydrocarbonsPointsMainDialog
from ..ConnectionPoints.ConnectionPointsMainDialog import ConnectionPointsMainDialog
from ..ViewDatasource.ViewDatasourceDialog import ViewDatasourceDialog

from ...Enums.DlgMode import DlgMode

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'LayerToolsPanel.ui'), resource_suffix='')

class LayerToolsPanel(QtWidgets.QDockWidget, FORM_CLASS):
    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(LayerToolsPanel, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://doc.qt.io/qt-5/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.mapTool = None
        self.layer = None
        self.currentDlg = None
        self.toggleGroup = [
            self.btnInsertWastewaterNetwork, self.btnEditWastewaterNetwork, 
            self.btnInsertWastewaterObject, self.btnEditWastewaterObject,
            self.btnInsertWastewaterPoint, self.btnEditWastewaterPoint,
            self.btnInsertWaterSupplyNetwork, self.btnEditWaterSupplyNetwork,
            self.btnInsertWaterSupplyPoints, self.btnEditWaterSupplyPoints,
            self.btnInsertGasNetwork, self.btnEditGasNetwork, 
            self.btnInsertGasObject, self.btnEditGasObject, 
            self.btnInsertGasSupplyPoints, self.btnEditGasSupplyPoints,
            self.btnInsertPowerSupplyNetwork, self.btnEditPowerSupplyNetwork,
            self.btnInsertHeatSupplyNetwork, self.btnEditHeatSupplyNetwork,
            self.btnInsertHeatSupplyPoints, self.btnEditHeatSupplyPoints,
            self.btnInsertHeatSupplyObject, self.btnEditHeatSupplyObject,
            self.btnInsertCommunicationNetwork, self.btnEditCommunicationNetwork,
            self.btnInsertCommunicationObject, self.btnEditCommunicationObject,
            self.btnInsertCommunicationPoint, self.btnEditCommunicationPoint,
            self.btnInsertWaterSupplyObjects, self.btnEditWaterSupplyObjects,
            self.btnInsertPowerSupplyPoints, self.btnEditPowerSupplyPoints,
            self.btnInsertPowerSupplyObjects, self.btnEditPowerSupplyObjects,
            self.btnInsertMagistralPipelinesNetworks, self.btnEditMagistralPipelinesNetworks,
            self.btnInsertLiquidHydrocarbonsNetworks, self.btnEditLiquidHydrocarbonsNetworks,
            self.btnInsertLiquidHydrocarbonsObjects, self.btnEditLiquidHydrocarbonsObjects,
            self.btnInsertLiquidHydrocarbonsPoints, self.btnEditLiquidHydrocarbonsPoints,
            self.btnInsertConnectionPoint, self.btnEditConnectionPoint,
            self.btnEditAny, self.btnCombine, self.btnDataSourceInfo #, self.btnSplitLine, self.btnSplitPolygons
        ]

        #Кнпока редактирования любого элемента
        self.btnEditAny.clicked.connect(self.__btnEditAnyClicked)

        #Кнопка объединения элементов
        self.btnCombine.clicked.connect(self.__btnCombineClicked)

        #Кнопка разделения элементов polyline
        #self.btnSplitLine.clicked.connect(self.__btnSplitLineClicked)

        # Кнопка разделения полигонов
        #self.btnSplitPolygons.clicked.connect(self.__btnSplitPolygonsClicked)

        #Кнопка сведения об источнике данных
        self.btnDataSourceInfo.clicked.connect(self.__btnDataSourceInfoClicked)

        # Кнопки газоснабжения
        self.btnInsertGasNetwork.clicked.connect(self.__btnInsertGasNetworkClicked)
        self.btnEditGasNetwork.clicked.connect(self.__btnEditGasNetworkClicked)
        self.btnInsertGasObject.clicked.connect(self.__btnInsertGasObjectClicked)
        self.btnEditGasObject.clicked.connect(self.__btnEditGasObjectClicked)
        self.btnInsertGasSupplyPoints.clicked.connect(self.__btnInsertGasSupplyPointsClicked)
        self.btnEditGasSupplyPoints.clicked.connect(self.__btnEditGasSupplyPointsClicked)

        # Кнопки водоотведения
        self.btnInsertWastewaterNetwork.clicked.connect(self.__btnInsertWastewaterNetworkClicked)
        self.btnEditWastewaterNetwork.clicked.connect(self.__btnEditWastewaterNetworkClicked)
        self.btnInsertWastewaterObject.clicked.connect(self.__btnInsertWastewaterObjectClicked)
        self.btnEditWastewaterObject.clicked.connect(self.__btnEditWastewaterObjectClicked)
        self.btnInsertWastewaterPoint.clicked.connect(self.__btnInsertWastewaterPointsClicked)
        self.btnEditWastewaterPoint.clicked.connect(self.__btnEditWastewaterPointsClicked)

        # Кнопки водоснабжения
        self.btnInsertWaterSupplyNetwork.clicked.connect(self.__btnInsertWaterSupplyNetworkClicked)
        self.btnEditWaterSupplyNetwork.clicked.connect(self.__btnEditWaterSupplyNetworkClicked)
        self.btnInsertWaterSupplyObjects.clicked.connect(self.__btnInsertWaterSupplyObjectsClicked)
        self.btnEditWaterSupplyObjects.clicked.connect(self.__btnEditWaterSupplyObjectsClicked)
        self.btnInsertWaterSupplyPoints.clicked.connect(self.__btnInsertWaterSupplyPointsClicked)
        self.btnEditWaterSupplyPoints.clicked.connect(self.__btnEditWaterSupplyPointsClicked)

        #Кнопки энергоснабжения
        self.btnInsertPowerSupplyNetwork.clicked.connect(self.__btnInsertPowerSupplyNetworkClicked)
        self.btnEditPowerSupplyNetwork.clicked.connect(self.__btnEditPowerSupplyNetworkClicked)
        self.btnInsertPowerSupplyPoints.clicked.connect(self.__btnInsertPowerSupplyPointsClicked)
        self.btnEditPowerSupplyPoints.clicked.connect(self.__btnEditPowerSupplyPointsClicked)
        self.btnInsertPowerSupplyObjects.clicked.connect(self.__btnInsertPowerSupplyObjectsClicked)
        self.btnEditPowerSupplyObjects.clicked.connect(self.__btnEditPowerSupplyObjectsClicked)

        #Кнопки теплоснабжения
        self.btnInsertHeatSupplyNetwork.clicked.connect(self.__btnInsertHeatSupplyNetworkClicked)
        self.btnEditHeatSupplyNetwork.clicked.connect(self.__btnEditHeatSupplyNetworkClicked)
        self.btnInsertHeatSupplyPoints.clicked.connect(self.__btnInsertHeatSupplyPointsClicked)
        self.btnEditHeatSupplyPoints.clicked.connect(self.__btnEditHeatSupplyPointsClicked)
        self.btnInsertHeatSupplyObject.clicked.connect(self.__btnInsertHeatSupplyObjectClicked)
        self.btnEditHeatSupplyObject.clicked.connect(self.__btnEditHeatSupplyObjectClicked)

        # Кнопки связи
        self.btnInsertCommunicationNetwork.clicked.connect(self.__btnInsertCommunicationNetworkClicked)
        self.btnEditCommunicationNetwork.clicked.connect(self.__btnEditCommunicationNetworkClicked)
        self.btnInsertCommunicationObject.clicked.connect(self.__btnInsertCommunicationObjectClicked)
        self.btnEditCommunicationObject.clicked.connect(self.__btnEditCommunicationObjectClicked)
        self.btnInsertCommunicationPoint.clicked.connect(self.__btnInsertCommunicationPointClicked)
        self.btnEditCommunicationPoint.clicked.connect(self.__btnEditCommunicationPointClicked)

        #Кнопки магистрального трубопровода
        self.btnInsertMagistralPipelinesNetworks.clicked.connect(self.__btnInsertMagistralPipelinesNetworksClicked)
        self.btnEditMagistralPipelinesNetworks.clicked.connect(self.__btnEditMagistralPipelinesNetworksClicked)

        #Кнпоки трубопровода
        self.btnInsertLiquidHydrocarbonsNetworks.clicked.connect(self.__btnInsertLiquidHydrocarbonsNetworksClicked)
        self.btnEditLiquidHydrocarbonsNetworks.clicked.connect(self.__btnEditLiquidHydrocarbonsNetworksClicked)
        self.btnInsertLiquidHydrocarbonsObjects.clicked.connect(self.__btnInsertLiquidHydrocarbonsObjectsClicked)
        self.btnEditLiquidHydrocarbonsObjects.clicked.connect(self.__btnEditLiquidHydrocarbonsObjectsClicked)
        self.btnInsertLiquidHydrocarbonsPoints.clicked.connect(self.__btnInsertLiquidHydrocarbonsPointsClicked)
        self.btnEditLiquidHydrocarbonsPoints.clicked.connect(self.__btnEditLiquidHydrocarbonsPointsClicked)

        #Кнопки точек подключения
        self.btnInsertConnectionPoint.clicked.connect(self.__btnInsertConnectionPointClicked)
        self.btnEditConnectionPoint.clicked.connect(self.__btnEditConnectionPointClicked)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def __btnSplitPolygonsClicked(self):
        self.mapTool = FindFeatureMapTool(self.iface.mapCanvas())
        self.mapTool.finished.connect(self.__findingPolygonToSplitFinished)
        self.mapTool.canceled.connect(self.__mapToolFinished)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def __findingPolygonToSplitFinished(self, identifyResult):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.mapTool = SplitPolygonMapTool(self.iface.mapCanvas(), identifyResult.mFeature, identifyResult.mLayer)
        self.mapTool.finished.connect(self.__mapToolFinished)
        identifyResult.mLayer.select([identifyResult.mFeature.id()])
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def __mapToolFinished(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.mapTool = None
        self.__uncheckAll()

    def __btnEditAnyClicked(self):
        self.__uncheckAll(self.btnEditAny)
        self.mapTool = FindFeatureMapTool(self.iface.mapCanvas())
        self.mapTool.finished.connect(self.__editAnyFinished)
        self.mapTool.canceled.connect(self.__editAnyCanceled) 
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def __editAnyCanceled(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.mapTool = None
        self.__uncheckAll()

    def __editAnyFinished(self, objectToAnalyse):        
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.mapTool = None

        isChecked = True
        layerName = objectToAnalyse.mLayer.name()
        feature = objectToAnalyse.mFeature
        parent = self.iface.mainWindow()

        if layerName == LayerNames.GasNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: GasNetworkMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.GasSupplyObjects:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: GasSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.GasSupplyPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda : GasSupplyPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.ElectricitySupplyNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: ElectricitySupplyNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.ElectricitySupplyObjects:
            self.__groupedBtnClicked(self.__btnEditAnyClicked, isChecked, lambda: ElectricitySupplyObjectsMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.ElectricitySupplyPoints:
            self.__groupedBtnClicked(self.__btnEditAnyClicked, isChecked, lambda: ElectricitySupplyPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.HeatSupplyNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: HeatSupplyNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.HeatSupplyObjects:
            self.__groupedBtnClicked(self.__btnEditAnyClicked, isChecked, lambda: HeatSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.HeatSupplyPoints:
            self.__groupedBtnClicked(self.__btnEditAnyClicked, isChecked, lambda: HeatSupplyPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.CommunicationNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: CommunicationNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.CommunicationObjects:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: CommunicationObjectsMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.CommunicationPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked,lambda: CommunicationPointsMainDialog(self.iface, DlgMode.EDIT, parent,feature))

        elif layerName == LayerNames.WastewaterNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: WastewaterNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.WastewaterObjects:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: WastewaterObjectMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.WastewaterPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked,lambda: WastewaterPointsMainDialog(self.iface, DlgMode.EDIT,parent,feature))

        elif layerName == LayerNames.WaterSupplyNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: WaterSupplyNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.WaterSupplyObjects:
            self.__groupedBtnClicked(self.btnEditAny, isChecked,lambda: WaterSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, parent,feature))
        elif layerName == LayerNames.WaterSupplyPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: WaterSupplyPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.LiquidHydrocarbonsNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda : LiquidHydrocarbonsNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.LiquidHydrocarbonsObjects:
            self.__groupedBtnClicked(self.btnEditAny, isChecked,lambda: LiquidHydrocarbonsObjectsMainDialog(self.iface, DlgMode.EDIT, parent, feature))
        elif layerName == LayerNames.LiquidHydrocarbonsPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda: LiquidHydrocarbonsPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.ConnectionPoints:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda : ConnectionPointsMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        elif layerName == LayerNames.MagistralPipelinesNetworks:
            self.__groupedBtnClicked(self.btnEditAny, isChecked, lambda : MagistralPipelinesNetworksMainDialog(self.iface, DlgMode.EDIT, parent, feature))

        else:
            # запуск системного окна редактирования?
            pass

    def __btnCombineClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnCombine, isChecked, lambda : GeometryCombinerDialog(self.iface, self.iface.mainWindow()))

    def __btnSplitLineClicked(self):
        self.mapTool = SplitPolylineMapTool(self.iface.mapCanvas())
        self.mapTool.finished.connect(self.__splitLineFinished)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def __splitLineFinished(self):
        self.__unsetMapToolUncheckButtons()

    def __unsetMapToolUncheckButtons(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.mapTool = None
        self.__uncheckAll()

    def __btnDataSourceInfoClicked(self):
        isChecked = True
        self.__groupedBtnClicked(self.btnDataSourceInfo, isChecked, lambda: ViewDatasourceDialog(self.iface))

    def __btnInsertGasNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertGasNetwork, isChecked, lambda: GasNetworkMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditGasNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditGasNetwork, isChecked,  lambda: GasNetworkMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))    

    def __btnInsertGasObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertGasObject, isChecked, lambda: GasSupplyObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditGasObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditGasObject, isChecked,  lambda: GasSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertGasSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertGasSupplyPoints, isChecked, lambda : GasSupplyPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditGasSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditGasSupplyPoints, isChecked, lambda : GasSupplyPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertWastewaterNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWastewaterNetwork, isChecked, lambda: WastewaterNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditWastewaterNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWastewaterNetwork, isChecked, lambda: WastewaterNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertWastewaterObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWastewaterObject, isChecked, lambda: WastewaterObjectMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditWastewaterObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWastewaterObject, isChecked, lambda:WastewaterObjectMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertWaterSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWaterSupplyNetwork, isChecked, lambda: WaterSupplyNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditWaterSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWaterSupplyNetwork, isChecked, lambda: WaterSupplyNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertWaterSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWaterSupplyPoints, isChecked, lambda: WaterSupplyPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditWaterSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWaterSupplyPoints, isChecked, lambda: WaterSupplyPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertPowerSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertPowerSupplyNetwork, isChecked, lambda: ElectricitySupplyNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditPowerSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditPowerSupplyNetwork, isChecked, lambda: ElectricitySupplyNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertPowerSupplyObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertPowerSupplyObjects, isChecked, lambda: ElectricitySupplyObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditPowerSupplyObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditPowerSupplyObjects, isChecked, lambda: ElectricitySupplyObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertHeatSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertHeatSupplyNetwork, isChecked, lambda: HeatSupplyNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditHeatSupplyNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditHeatSupplyNetwork, isChecked, lambda: HeatSupplyNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertHeatSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertHeatSupplyPoints, isChecked, lambda: HeatSupplyPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditHeatSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditHeatSupplyPoints, isChecked, lambda: HeatSupplyPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertHeatSupplyObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertHeatSupplyObject, isChecked, lambda : HeatSupplyObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditHeatSupplyObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditHeatSupplyObject, isChecked, lambda : HeatSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertCommunicationNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertCommunicationNetwork, isChecked, lambda: CommunicationNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditCommunicationNetworkClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditCommunicationNetwork, isChecked, lambda: CommunicationNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertCommunicationObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertCommunicationObject, isChecked, lambda: CommunicationObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditCommunicationObjectClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditCommunicationObject, isChecked, lambda: CommunicationObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertCommunicationPointClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertCommunicationPoint, isChecked, lambda: CommunicationPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditCommunicationPointClicked(self, isChekced):
        self.__groupedBtnClicked(self.btnEditCommunicationPoint, isChekced, lambda : CommunicationPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertWastewaterPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWastewaterPoint, isChecked, lambda: WastewaterPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditWastewaterPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWastewaterPoint, isChecked, lambda: WastewaterPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertWaterSupplyObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertWaterSupplyObjects, isChecked, lambda: WaterSupplyObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditWaterSupplyObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditWaterSupplyObjects, isChecked, lambda: WaterSupplyObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertPowerSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertPowerSupplyPoints, isChecked, lambda : ElectricitySupplyPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditPowerSupplyPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditPowerSupplyPoints, isChecked, lambda: ElectricitySupplyPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertMagistralPipelinesNetworksClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertMagistralPipelinesNetworks, isChecked, lambda : MagistralPipelinesNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditMagistralPipelinesNetworksClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditMagistralPipelinesNetworks, isChecked, lambda : MagistralPipelinesNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertLiquidHydrocarbonsNetworksClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertLiquidHydrocarbonsNetworks, isChecked, lambda : LiquidHydrocarbonsNetworksMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditLiquidHydrocarbonsNetworksClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditLiquidHydrocarbonsNetworks, isChecked, lambda : LiquidHydrocarbonsNetworksMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertLiquidHydrocarbonsObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertLiquidHydrocarbonsObjects, isChecked, lambda : LiquidHydrocarbonsObjectsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))
        pass

    def __btnEditLiquidHydrocarbonsObjectsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditLiquidHydrocarbonsObjects, isChecked, lambda : LiquidHydrocarbonsObjectsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))
        pass

    def __btnInsertLiquidHydrocarbonsPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertLiquidHydrocarbonsPoints, isChecked, lambda: LiquidHydrocarbonsPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditLiquidHydrocarbonsPointsClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditLiquidHydrocarbonsPoints, isChecked, lambda: LiquidHydrocarbonsPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __btnInsertConnectionPointClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnInsertConnectionPoint, isChecked, lambda : ConnectionPointsMainDialog(self.iface, DlgMode.CREATE, self.iface.mainWindow()))

    def __btnEditConnectionPointClicked(self, isChecked):
        self.__groupedBtnClicked(self.btnEditConnectionPoint, isChecked, lambda : ConnectionPointsMainDialog(self.iface, DlgMode.EDIT, self.iface.mainWindow()))

    def __groupedBtnClicked(self, btn, isChecked, makeNewDlgCallback):
        self.__resetCurrentDlg()
        if isChecked:
            self.__uncheckAll(btn)
            try:
                self.currentDlg = makeNewDlgCallback()
                self.currentDlg.closingDlg.connect(self.__currentDlgClosed)
            except:
                self.__uncheckAll()

    def __resetCurrentDlg(self):
        if self.currentDlg is not None:
            self.currentDlg.closingDlg.disconnect(self.__currentDlgClosed)
            self.currentDlg = None

    def __uncheckAll(self, exceptBtn = None):
        for btn in self.toggleGroup:
            if btn.isChecked() and btn != exceptBtn:
                btn.setChecked(False)

    def __currentDlgClosed(self):
        self.__uncheckAll()
        self.__resetCurrentDlg()
