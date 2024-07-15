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
from ...Services.ImportDXFService import ImportDXFService

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'BatchDXFImporterDialog.ui'))

class BatchDXFImporterDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, parent=None, iface=None):
        """Constructor."""
        super(BatchDXFImporterDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface=iface
        self.buttonClose.setEnabled(True)
        self.buttonImport.setEnabled(False)
        self.buttonRemoveDXFFile.setEnabled(False)
        self.buttonAll.setEnabled(False)
        self.buttonClose.clicked.connect(self.__closeDlg)
        self.buttonImport.clicked.connect(self.__perfomImport)
        self.buttonAddDXFFile.clicked.connect(self.__addDXFFileClicked)
        self.buttonRemoveDXFFile.clicked.connect(self.__removeDXFFileClicked)
        self.buttonAll.clicked.connect(self.__btnAllClicked)
        self.listOfDXFs = []
        self.__importDXFService = ImportDXFService()
        self.setModal(True)

    def __closeDlg(self):
        self.close()

    def __disableEveryItem(self):
        self.buttonImport.setEnabled(False)
        self.buttonClose.setEnabled(False)
        self.buttonAll.setEnabled(False)

    def __enableEveryItem(self):
        self.buttonImport.setEnabled(True)
        self.buttonClose.setEnabled(True)
        self.buttonAll.setEnabled(True)

    def __addDXFFileClicked(self):
        dlg = QFileDialog()
        dlg.setFileMode(3)
        if dlg.exec():
            for selectedFile in dlg.selectedFiles():
                if selectedFile.split(".")[-1] != "dxf":
                    MessageBoxHelper.showPathIsAnExistingRegularFileMessageBox(self)
                    continue
                elif os.path.getsize(selectedFile) > 31457280:
                    MessageBoxHelper.showSomeFilesAreTooBigMessageBox(self)
                    continue
                elif selectedFile in self.listOfDXFs:
                    MessageBoxHelper.showChoosenDXFisAlreadyInTheList(self)
                    continue
                self.listOfDXFs.append(selectedFile)
                self.buttonRemoveDXFFile.setEnabled(True)
                self.buttonImport.setEnabled(True)
                self.buttonAll.setEnabled(True)
                lvi = QListWidgetItem()
                lvi.setText(selectedFile)
                lvi.setCheckState(Qt.Unchecked)
                self.listView.addItem(lvi)

    def __removeDXFFileClicked(self):
        elementIndexesToDelete = []
        for i in range (self.listView.count()):
            if self.listView.item(i).checkState() == 2:
                elementIndexesToDelete.append(i)

        elementIndexesToDelete.sort(reverse=True)

        for i in elementIndexesToDelete:
           self.listView.takeItem(i)
           self.listOfDXFs.pop(i)

        if self.listView.count() == 0:
            self.buttonRemoveDXFFile.setEnabled(False)
            self.buttonImport.setEnabled(False)
            self.buttonAll.setEnabled(False)

    def __getLayerByName(self, name):
        layers = QgsProject.instance().mapLayersByName(name)
        if layers:
            return layers[0]
        return None

    """Осуществление импорта"""
    def __perfomImport(self):
        self.__disableEveryItem()
        for number, file in enumerate(self.listOfDXFs):
            self.textEdit.append("Производится анализ DXF-файла " + str(file) + "...")

            if os.path.isfile(file) == False:
                MessageBoxHelper.showPathIsAnExistingRegularFileMessageBox(self)
                self.textEdit.setTextColor(Qt.red)
                self.textEdit.append("DXF-файл {0} нет возможности импортировать".format(file))
                self.textEdit.setTextColor(Qt.black)
                for i in range(self.listView.count()):
                    if self.listView.item(i).text() == file:
                        self.listView.item(i).setForeground(Qt.red)
                continue

            self.repaint()
            try:
                geometryList = AdministrationServerService().getGeometryList(file, [])
                elementsCount = sum([len(x['features']) for x in geometryList['layers']])
                self.textEdit.append(
                    "Найдено {0} элементов на {1} слоях...".format(elementsCount, len(geometryList['layers'])))
                self.__perfomAnalysis(geometryList)
            except Exception as ex:
                MessageBoxHelper.showGettingGeomertyErrorMessageBox(self)
                self.textEdit.append("Ошибка анализа DXF-файла на сервере администрирования.")
                self.textEdit.append("Операция импорта прервана.")
                continue
            finally:

                self.__enableEveryItem()

        self.textEdit.append("Операция импорта завершена.")
        self.buttonClose.setEnabled(True)

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

    def __btnAllClicked(self):
        checkBool = True
        for i in range(self.listView.count()):
            checkBool = checkBool and self.listView.item(i).checkState() == 2

        self.__doAll(0 if checkBool == True else 2)

    def __doAll(self, checkSate):
        for i in range(self.listView.count()):
            self.listView.item(i).setCheckState(checkSate)



