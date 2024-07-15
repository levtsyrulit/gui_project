import os

from qgis.PyQt import uic 
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QTableWidgetItem
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.core import QgsProject, QgsLayerTreeGroup, QgsLayerTreeNode
from qgis.gui import QgsMapToolIdentifyFeature

from ...Models.DataWidgetModel import DataWidgetModel
from ...MapTools.ViewDataSourceMapTool import ViewDataSourceMapTool
from ...Helpers.DataSourceObject import DataSourceObject
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ViewDatasourceDialog.ui'))

class ViewDatasourceDialog(QtWidgets.QDialog, FORM_CLASS):
    closingDlg = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ViewDatasourceDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.objectsDictionary = {}
        self.dataSourceList = []

        self.btnOk.clicked.connect(self.__btnOkClicked)
        self.btnCancel.clicked.connect(self.__canceled)

        self.sourceDictionary = {}
        self.groupDictionary = {}
        self.objectDictionary = {}

        self.__initMapTool()

    def __initMapTool(self):
        self.mapTool = ViewDataSourceMapTool(self.iface)
        self.mapTool.finished.connect(self.__dataSourceMapToolFinished)
        self.mapTool.canceled.connect(self.__closeDlg)
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def __dataSourceMapToolFinished(self, dictionary):
        if dictionary != {}:
            self.objectsDictionary = dictionary
            self.__setIDProperyToLayerTreeGroups(QgsProject.instance().layerTreeRoot(), 0)
            self.__createDataSourceList(self.objectsDictionary)
            self.__initializeQTableWidget(self.dataSourceList)
        self.show()

    def __setIDProperyToLayerTreeGroups(self, group, id):
        for child in group.children():
            if child.nodeType() == QgsLayerTreeNode.NodeGroup:
                id += 1
                child.setCustomProperty("id", id)
                self.__setIDProperyToLayerTreeGroups(child, id)

    def __createDataSourceList(self, objectsDictionary):
        for item in objectsDictionary.items():
            layer = item[0]
            layerName = layer.name()
            layerID = layer.id()
            featureList = item[1]
            numberOfFeatures = len(featureList)
            featureIDs = []
            for feature in featureList:
                featureIDs.append(feature.id())

            sources = self.__getLayerSources(layer)
            self.dataSourceList.append(DataSourceObject(sources[0], sources[1], layerName, numberOfFeatures, layerID, featureIDs, sources[2]))

    def __getLayerSources(self, layer):
        root = QgsProject.instance().layerTreeRoot()
        extentalSourceNodes = self.__getExtentalSourceNodes(root)
        group = root.findLayer(layer.id())        
        if group is root:
            return ("Фонд топографо-геодезических работ и ИИ", layer.name(), layer.id())            
        if group in extentalSourceNodes:
            return(layer.name(), layer.name(), layer.id())
        
        parent = group.parent()
        if parent is root:
            return("Фонд топографо-геодезических работ и ИИ", group.name(), group.customProperty("id"))
        if parent in extentalSourceNodes:
            return(group.name(), layer.name(), layer.id())

        return self.__getNodeTwoParents(root, extentalSourceNodes, parent, group)

    def __getNodeTwoParents(self, root, extentalSourceNodes, node, child):
        parent = node.parent()
        if parent is root:
            return("Фонд топографо-геодезических работ и ИИ", node.name(), node.customProperty("id"))
        if parent in extentalSourceNodes:
            return(node.name(), child.name(), child.customProperty("id"))

        return self.__getNodeTwoParents(root, extentalSourceNodes, node.parent(), node)

    def __getExtentalSourceNodes(self, root):
        return [node for node in root.children() if node.name() == "Внешние источники"]

    """Инициализация QTableWidget"""
    def __initializeQTableWidget(self, dataSourceObjects):
        self.__initWidgetsData(dataSourceObjects)

        self.__initTableSourcesWidget(self.sourceDictionary)
        self.__initTableLayersWidget(self.groupDictionary)
        self.__initTableObjectsWidget(self.objectDictionary)

    """Инициализируем данные формы"""
    def __initWidgetsData(self, dataSourceObjects):
        for object in dataSourceObjects:
            sourceName = object.sourceName
            groupName = object.groupName
            layerName = object.layerName
            count = object.count
            layerID = object.layerID
            featureIDs = object.featureIDs
            groupID = object.groupID
            
            if sourceName not in self.sourceDictionary.keys():
                dictionary = {layerID: featureIDs}
                modelSource = DataWidgetModel(sourceName, groupID, None, None, count, dictionary)
                self.sourceDictionary[sourceName] = modelSource
            else:
                modelSource = self.sourceDictionary[sourceName]
                modelSource.layerFeatureDictionary[layerID] = featureIDs
                modelSource.count += count

            if groupID not in self.groupDictionary.keys():
                dictionary = {layerID: featureIDs}
                modelGroup = DataWidgetModel(sourceName, groupID, groupName, layerName, count, dictionary)
                self.groupDictionary[groupID] = modelGroup
            else:
                modelGroup = self.groupDictionary[groupID]                
                modelGroup.layerFeatureDictionary[layerID] = featureIDs
                modelGroup.count += count

            modelObject = DataWidgetModel(sourceName, None, None, layerName, count, {layerID: featureIDs})
            self.objectDictionary[layerID] = modelObject

    def __initTableSourcesWidget(self, sourceDictionary):
        self.tableSources.setRowCount(len(sourceDictionary))
        row = 0
        for key in sourceDictionary.keys():
            itemWithData = QTableWidgetItem(key)
            itemWithData.setData(Qt.UserRole, sourceDictionary[key].layerFeatureDictionary)
            self.tableSources.setItem(row, 0, itemWithData)
            self.tableSources.setItem(row, 1, QTableWidgetItem(str(sourceDictionary[key].count)))
            row += 1

        self.tableSources.resizeColumnsToContents()

    def __initTableLayersWidget(self, groupDictionary):
        self.tableLayers.setRowCount(len(groupDictionary))
        self.tableLayers.setColumnWidth(1, 150)
        row = 0

        for key in groupDictionary.keys():
            itemWithData = QTableWidgetItem(groupDictionary[key].groupName)
            itemWithData.setData(Qt.UserRole, groupDictionary[key].layerFeatureDictionary)
            self.tableLayers.setItem(row, 0, itemWithData)
            self.tableLayers.setItem(row, 1, QTableWidgetItem(str(groupDictionary[key].count)))
            self.tableLayers.setItem(row, 2, QTableWidgetItem(groupDictionary[key].sourceName))
            row += 1

        self.tableObjects.resizeColumnsToContents()

    def __initTableObjectsWidget(self, objectDictionary):
        self.tableObjects.setRowCount(len(objectDictionary))
        self.tableObjects.setColumnWidth(1, 150)
        row = 0
        for key in objectDictionary.keys():
            itemWithData = QTableWidgetItem(objectDictionary[key].layerName)
            itemWithData.setData(Qt.UserRole, objectDictionary[key].layerFeatureDictionary)
            self.tableObjects.setItem(row, 0, itemWithData)
            self.tableObjects.setItem(row, 1, QTableWidgetItem(str(objectDictionary[key].count)))
            self.tableObjects.setItem(row, 2, QTableWidgetItem(objectDictionary[key].sourceName))
            row += 1

        self.tableObjects.resizeColumnsToContents()

    def __btnOkClicked(self):
        selectedItems = self.__getSelectedItems()
        if selectedItems != []:
           self.__selectObjects(selectedItems)
        self.__closeDlg()

    def __getSelectedItems(self):
        if self.tabWidget.currentWidget().objectName() == "tabSources":
            return self.tableSources.selectedItems()
        elif self.tabWidget.currentWidget().objectName() == "tabLayers":
            return self.tableLayers.selectedItems()
        elif  self.tabWidget.currentWidget().objectName() == "tabObjects":
            return self.tableObjects.selectedItems()

    def __selectObjects(self, selectedItems):
        for item in selectedItems:
            if item.column() == 0:
                data = item.data(Qt.UserRole)
                for layerID in data.keys():
                    QgsProject.instance().mapLayers()[layerID].select(data[layerID])

    def __canceled(self):
        self.__selectAll()
        self.__closeDlg()

    def __selectAll(self):
        for item in self.objectsDictionary.items():
            for feature in item[1]:
                item[0].select(feature.id())

    def __closeDlg(self):
        self.iface.mapCanvas().unsetMapTool(self.iface.mapCanvas().mapTool())
        self.close()

    def closeEvent(self, event):
        self.closingDlg.emit()

