import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal, QDateTime, QCoreApplication
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsProject, QgsGeometry, QgsMapLayer, QgsFeature
from qgis.gui import QgsMapToolIdentifyFeature

from ...Helpers.LayerNames import LayerNames
from ...MapTools.PolygonMapTool import PolygonMapTool
from ...Models.GasSupplyObjectsModel import GasSupplyObjectsModel
from ..ObjectPassport.ObjectPassportDialog import ObjectPassportDialog
from .GasSupplyObjectsAdditionalDialog import GasSupplyObjectsAdditionalDialog
from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper
from ...Services.FileService import FileService
from ...Services.AdministrationServerService import AdministrationServerService
from ..ProgressDialog.ProgressDialog import ProgressDialog

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'GasSupplyObjectsMainDialog.ui'))

class GasSupplyObjectsMainDialog(QtWidgets.QDialog, FORM_CLASS):
    LAYERNAME = LayerNames.GasSupplyObjects
    closingDlg = pyqtSignal()

    def __init__(self, iface, mode = DlgMode.VIEW, parent=None, feature=None):

        """Constructor."""
        super(GasSupplyObjectsMainDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setModal(True)

        self.mapTool = None
        self.model = GasSupplyObjectsModel()
        self.layer = None
        self.points = []
        self.mode = mode
        self.feature = feature
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.additionalStructuresIsSelected = False

        signal = self.__initLayer()
        if signal == False:
            raise
        else:
            ds = DictionariesService()
            self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
            self.dictionaryComboBoxHelper.setItems(self.cbObjectState, ds.Dictionary11C.getElements())
            self.dictionaryComboBoxHelper.setItems(self.cbObjectType, ds.Dictionary11J.getElementsExcept(["11J.14", "11J.21"]))
            self.dictionaryComboBoxHelper.setItems(self.cbArrangement, ds.Dictionary11F.getElements())
            self.dictionaryComboBoxHelper.setItems(self.cbAdditionalStructures, ds.DictionaryCT24.getSpecificElements(["CT24.1"]))

            self.__initFields()

            self.cbObjectType.currentIndexChanged.connect(self.__checkAddictionalStructuresEnable)
            self.btnAdditionalAttributes.clicked.connect(self.__openAdditionalAttributesDlg)
            self.btnObjectPassport.clicked.connect(self.__openObjectPassportDlg)
            self.btnCancel.clicked.connect(self.__closeDlg)
            self.btnOk.clicked.connect(self.__applyChanges)
            self.btnDownloadFiles.clicked.connect(self.__downloadAttachedFiles)

            self.__initMode()
            self.__checkAddictionalStructuresEnable()

    def __checkAddictionalStructuresEnable(self):
        item = self.dictionaryComboBoxHelper.getSelectedItem(self.cbObjectType)
        self.additionalStructuresIsSelected = item and item.name == "11J.0"
        if self.additionalStructuresIsSelected:
            self.cbAdditionalStructures.setEnabled(self.mode != DlgMode.VIEW)
        else:
            self.cbAdditionalStructures.setEnabled(False)
            self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbAdditionalStructures, DictionaryComboBoxHelper.UNSELECTED_ITEM.id)

    """Инициализируем режим работы формы и подготавливаем инструмент работы с картой"""
    def __initMode(self):
        self.__setReadOnly(self.mode == DlgMode.VIEW)
        if self.mode == DlgMode.CREATE:
            self.btnDownloadFiles.hide()
            self.mapTool = PolygonMapTool(self.canvas)
            self.mapTool.finished.connect(self.__geometrySpecified)
            self.mapTool.canceled.connect(self.__canceled)
        else:
            if self.feature:
                self.__editElement(self.feature)
                return
            else:
                self.mapTool = QgsMapToolIdentifyFeature(self.canvas) 
                self.mapTool.setLayer(self.layer)
                self.mapTool.featureIdentified.connect(self.__featureSelected)

        self.canvas.setMapTool(self.mapTool)
        self.mapTool.deactivated.connect(self.__canceled)

    """Перевод всех элементов формы в режим 'Только чтение'"""
    def __setReadOnly(self, readOnly = False):
        self.tbDenomination.setReadOnly(readOnly)
        self.cbObjectState.setEnabled(not readOnly)
        self.cbObjectType.setEnabled(not readOnly)
        self.cbArrangement.setEnabled(not readOnly)
        self.tbLocation.setEnabled(not readOnly)
        self.tbCadastralNumber.setReadOnly(readOnly)
        self.cbAdditionalStructures.setEnabled(not readOnly)
        self.tbDataSource.setReadOnly(readOnly)

    """Инициализация слоя"""
    def __initLayer(self):
        layer = self.__getLayerByName(self.LAYERNAME)
        if layer is None:
            QMessageBox.critical(self, "Критическая ошибка", "Не найден слой ""{0}""".format(self.LAYERNAME),
                                 QMessageBox.Ok)
            return False
        if ((layer.isEditable() or layer.startEditing()) == False):
            if self.mode == DlgMode.CREATE:
                QMessageBox.critical(self, "Критическая ошибка", "У Вас нет прав для редактирования этого слоя",
                                     QMessageBox.Ok)
                return False
            elif self.mode == DlgMode.EDIT:
                self.mode = DlgMode.VIEW

        self.layer = layer
        return True

    def closeEvent(self, event):
        self.closingDlg.emit()

    def __closeDlg(self):
        if self.mapTool != None:
            self.canvas.unsetMapTool(self.mapTool)
        self.close()

    def __geometrySpecified(self, points: list):
        self.__createElement(points)

    def __featureSelected(self, feature):
        self.__editElement(feature)

    def __createElement(self, points: list):
        if len(points) < 2:
            self.closeDlg()
        else:
            self.points = points
            self.show()

    def __editElement(self, feature):
        if not feature:
            self.closeDlg()
        else:
            self.layer.removeSelection()
            self.layer.select([feature.id()])
            self.feature = feature
            self.model.fillModelFromFeature(feature)
            self.__initFields()
            self.show()

    def __canceled(self):
        if self.feature == None:
            self.mapTool.deactivated.disconnect(self.__canceled)
        self.__closeDlg()

    def __fillModel(self):
        self.model.denomination = self.tbDenomination.text()
        self.model.state = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbObjectState)
        self.model.type_ = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbObjectType)
        self.model.arrangement = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbArrangement)
        self.model.location = self.tbLocation.text()
        self.model.cadastralNumber = self.tbCadastralNumber.text()
        if self.additionalStructuresIsSelected:
            self.model.additionalStructures = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(
                self.cbAdditionalStructures)
        else:
            self.model.additionalStructures = None
        self.model.dataSource = self.tbDataSource.text()

        if self.mode == DlgMode.CREATE:
            self.model.creation_date = QDateTime.currentDateTime()
            # self.model.creator = "Создатель"
        self.model.update_date = QDateTime.currentDateTime()
        # self.model.editor = "Редактор"
        
    def __initFields(self):
        self.tbDenomination.setText(self.model.denomination)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbObjectState, self.model.state)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbObjectType, self.model.type_)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbArrangement, self.model.arrangement)
        self.tbLocation.setText(self.model.location)
        self.tbCadastralNumber.setText(self.model.cadastralNumber)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbAdditionalStructures,
                                                                       self.model.additionalStructures)
        self.tbDataSource.setText(self.model.dataSource)

        self.__checkAddictionalStructuresEnable()

        if self.model.attachedFilesCount is None or self.model.attachedFilesCount.strip() == "" or self.model.attachedFilesCount.strip() == "0":
            self.btnDownloadFiles.setText("Файл источник")
            self.btnDownloadFiles.setEnabled(False)
        else:
            self.btnDownloadFiles.setText("Файл источник ({0})".format("0" if self.model.attachedFilesCount == "" else self.model.attachedFilesCount))
            self.btnDownloadFiles.setEnabled(True)

    def __createFeatureFromModel(self, layer: QgsMapLayer):
        feature = QgsFeature(layer.fields())
        self.model.fillFeatureFromModel(feature)
        feature.setGeometry(self.__getGeometry())
        (created, outFeatures) = layer.dataProvider().addFeatures([feature])
        if created:
            return outFeatures[0]
        return None

    def __getGeometry(self):
        return QgsGeometry.fromPolygonXY([self.points])

    def __getLayerByName(self, name):
        layers = QgsProject.instance().mapLayersByName(name) 
        if layers:
            return layers[0]        
        return None

    def __applyChanges(self):
        if self.mode not in [DlgMode.CREATE, DlgMode.EDIT]:
            self.__closeDlg()
            return

        self.__fillModel()
        errors = self.model.validate()
        if len(errors) > 0:
            QMessageBox.critical(self, "Ошибка заполнения полей", "\n".join(errors), QMessageBox.Ok)
            return

        if self.mode == DlgMode.CREATE:
            self.__insertFeature()
        elif self.mode == DlgMode.EDIT:
            self.__updateFeature()
        
        if self.mode != DlgMode.VIEW:
            self.layer.commitChanges()            
        self.__closeDlg()

    def __updateFeature(self):
        if self.feature and self.layer:
            self.model.fillFeatureFromModel(self.feature)
            self.layer.updateFeature(self.feature)
            self.canvas.refresh()

    def __insertFeature(self):
        feature = self.__createFeatureFromModel(self.layer)
        self.layer.reload()
        self.canvas.refresh() 

    def __openAdditionalAttributesDlg(self):
        dlgAdditionalAttributes = GasSupplyObjectsAdditionalDialog(self.model, self.mode, self)
        dlgAdditionalAttributes.exec()

    def __openObjectPassportDlg(self):
        dlgObjectPassport = ObjectPassportDialog(self.model, self.mode, self)
        dlgObjectPassport.exec()

    def __downloadAttachedFiles(self):
        progressDlg = ProgressDialog("Скачивание файлов", "инициализация", self)
        try:            
            progressDlg.show()
            QCoreApplication.processEvents()

            aService = AdministrationServerService()
            progressDlg.setAction("получение файлов из API")
            model =  aService.downloadFolderFiles(self.model.attachedFilesID)

            if len(model["files"]) == 0:
                QMessageBox.info(self, "Скачивание файлов", "В каталоге отсутствуют файлы.", QMessageBox.Ok)    
                return

            fileService = FileService()
            progressDlg.setAction("создание временного каталога")
            tmpFolder = fileService.createTmpFolder()
            for file in model["files"]:
                progressDlg.setAction("сохранение файла {0}".format(file["name"]))
                fileService.saveFileToFolder(tmpFolder, file["name"], file["content"])

            fileService.openFile(tmpFolder)
        except Exception as ex:
            print(ex)
            QMessageBox.critical(self, "Критическая ошибка", "Ошибка скачивания файлов", QMessageBox.Ok)
        finally:
            progressDlg.close()