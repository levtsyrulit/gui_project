import os
import os.path

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtWidgets import QListWidgetItem, QFileDialog
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtCore import *
from qgis.core import QgsProject
from PyQt5.QtSql import *
from ...Helpers.MessageBoxHelper import MessageBoxHelper
from ...Services.AdministrationServerService import AdministrationServerService
from ...Services.DictionaryService import DictionariesService
from ...Services.ImportDXFService import ImportDXFService

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'DXFImporterDialog.ui'))

class DXFImporterDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None, iface=None):
        """Constructor."""
        super(DXFImporterDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface=iface
        self.buttonClose.clicked.connect(self.__closeDlg)
        self.buttonImport.setEnabled(False)
        self.buttonClose.setEnabled(True)
        self.buttonAddSourceFile.setEnabled(False)
        self.buttonRemoveSourceFile.setEnabled(False)
        self.fileWidgetObj.fileChanged.connect(self.__qgsFileWidgetChanged)
        self.buttonImport.clicked.connect(self.__startImport)
        self.buttonAddSourceFile.clicked.connect(self.__addSourceFileClicked)
        self.buttonRemoveSourceFile.clicked.connect(self.__removeSourceFileClicked)
        self.__dictionaryService = DictionariesService()
        self.listOfPathFiles = []
        self.__importDXFService = ImportDXFService()
        self.setModal(True)

    def __closeDlg(self):
        self.close()

    def __disableEveryItem(self):
        self.buttonImport.setEnabled(False)
        self.buttonClose.setEnabled(False)
        self.fileWidgetObj.setReadOnly(True)

    def __enableEveryItem(self):
        self.buttonImport.setEnabled(True)
        self.buttonClose.setEnabled(True)
        self.fileWidgetObj.setReadOnly(False)

    def __qgsFileWidgetChanged(self):
        if self.fileWidgetObj.filePath() != "":
            self.buttonImport.setEnabled(True)
            self.buttonAddSourceFile.setEnabled(True)
        else:
            self.buttonImport.setEnabled(False)

    def __addSourceFileClicked(self):
        dlg = QFileDialog()
        if dlg.exec():
            if os.path.getsize(dlg.selectedFiles()[0]) > 31457280:
                MessageBoxHelper.showSomeFilesAreTooBigMessageBox(self)
                return None

            self.listOfPathFiles.append(dlg.selectedFiles()[0]) #Путь к выбранному файлу
            fileInfoString = str(dlg.selectedFiles()[0].split("/")[-1]) + " (" + str(os.path.getsize(dlg.selectedFiles()[0])) + " байт)" #Строка, отображаемая в QListView
            self.buttonRemoveSourceFile.setEnabled(True)
            lvi = QListWidgetItem()
            lvi.setText(fileInfoString)
            lvi.setCheckState(Qt.Unchecked)
            self.listView.addItem(lvi)

    def __removeSourceFileClicked(self):
        elementIndexesToDelete = []
        for i in range (self.listView.count()):
            if self.listView.item(i).checkState() == 2:
                elementIndexesToDelete.append(i)

        elementIndexesToDelete.sort(reverse=True)

        for i in elementIndexesToDelete:
           self.listView.takeItem(i)
           self.listOfPathFiles.pop(i)

        if self.listView.count() == 0:
            self.buttonRemoveSourceFile.setEnabled(False)

    """Анализ path"""
    def __startImport(self):
        if os.path.isfile(self.fileWidgetObj.filePath()) == False:
            MessageBoxHelper.showPathIsAnExistingRegularFileMessageBox(self)
            self.textEdit.setText("Ошибка. Выбранный путь указывает не на DXF-файл. Выберите DXF-файл.")
        elif os.path.splitext(self.fileWidgetObj.filePath())[1] != ".dxf":
            MessageBoxHelper.showPathIsAnExistingRegularFileMessageBox(self)
            self.textEdit.setText("Ошибка. Выбранный путь указывает не на DXF-файл. Выберите DXF-файл.")
        else:
            self.__perfomImport(self.fileWidgetObj.filePath(), self.listOfPathFiles)

    def __getLayerByName(self, name):
        layers = QgsProject.instance().mapLayersByName(name)
        if layers:
            return layers[0]
        return None

    """Осуществление импорта"""
    def __perfomImport(self, dxfFilePath, listOfSourceFilesPaths):
        elementsIndexesToBeImported = []
        for i in range (self.listView.count()):
            if self.listView.item(i).checkState() == 2:
                elementsIndexesToBeImported.append(i)

        finalListOfSourceFiles = [] #Файлы-источники, которые должны быть импортированы (с галочкой)
        for i in elementsIndexesToBeImported:
            finalListOfSourceFiles.append(listOfSourceFilesPaths[i])

        self.textEdit.append("Производится анализ DXF-файла...")
        self.__disableEveryItem()
        self.repaint()
        try:
            geometryList = AdministrationServerService().getGeometryList(dxfFilePath, listOfSourceFilesPaths) #+listOfFiles[]
            elementsCount = sum([len(x['features']) for x in geometryList['layers']])
            self.textEdit.append("Найдено {0} элементов на {1} слоях...".format(elementsCount, len(geometryList['layers'])))
            self.__perfomAnalysis(geometryList)
            self.textEdit.append("Операция импорта завершена.")
        except Exception as ex:
            print(ex)
            MessageBoxHelper.showGettingGeomertyErrorMessageBox(self)
            self.textEdit.append("Ошибка анализа DXF-файла на сервере администрирования.")
            self.textEdit.append("Операция импорта прервана.")
            return
        finally:
            self.__enableEveryItem()        

    """Анализ слоёв"""
    def __perfomAnalysis(self, geometryList):
        for dxfLayer in geometryList['layers']:
            dxfLayerName = dxfLayer['layerName']
            self.textEdit.append('Импорт данных на слой "{0}":'.format(dxfLayerName))
            self.repaint()
            layer = self.__getLayerByName(dxfLayerName)
            if layer is None:
                self.textEdit.append('  Cлой "{0}" не найден на карте'.format(dxfLayerName))
                continue
            if (layer.isEditable() or layer.startEditing()) == False:
                self.textEdit.append('  У вас нет прав для добавления элементов на слой "{0}"'.format(dxfLayerName))
                continue            
            
            self.__addToLayer(layer, dxfLayer)

    """Добавление на слой"""
    def __addToLayer(self, layer, layerGeometries):
        success = 0
        errors = 0
        for dxfFeature in layerGeometries['features']:
            try:            
                feature = self.__importDXFService.createFeature(layer, dxfFeature)
                layer.dataProvider().addFeatures([feature])
                success = success + 1
            except Exception as ex:
                print(ex)
                errors = errors + 1

        self.textEdit.append('  Успешно импортировано {0} элементов'.format(success))
        self.textEdit.append('  Пропущено с ошибками {0} элементов'.format(errors))
        layer.commitChanges()
        self.iface.mapCanvas().refresh()


