import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CommunicationObjectsAdditionalDialog.ui'))

class CommunicationObjectsAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(CommunicationObjectsAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbActualUseOfTheObject.setClearValueMode(0)
        self.sbCapacitance.setClearValueMode(0)
        self.sbPower.setClearValueMode(0)
        self.sbSpeed.setClearValueMode(0)
        self.sbMaxDistanceOfBRZone.setClearValueMode(0)
        self.sbBottomBorderHeight.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbCommunicationLineType, ds.Dictionary11M.getElements())

        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.cbCommunicationLineType.setEnabled(False)
            self.sbActualUseOfTheObject.setReadOnly(True)
            self.sbCapacitance.setReadOnly(True)
            self.sbPower.setReadOnly(True)
            self.tbPowerUnit.setReadOnly(True)
            self.sbSpeed.setReadOnly(True)
            self.sbMaxDistanceOfBRZone.setReadOnly(True)
            self.sbBottomBorderHeight.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.communicationLineType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCommunicationLineType)
        self.model.actualUseOfTheObject = self.sbActualUseOfTheObject.value()
        self.model.capacity = self.sbCapacitance.value()
        self.model.power = self.sbPower.value()
        self.model.powerUnit = self.tbPowerUnit.text()
        self.model.dataTransferSpeed = self.sbSpeed.value()
        self.model.buildingRestructionZoneDistance = self.sbMaxDistanceOfBRZone.value()
        self.model.buildingRestructionZoneHeight = self.sbBottomBorderHeight.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCommunicationLineType, self.model.communicationLineType)
        self.sbActualUseOfTheObject.setValue(self.model.actualUseOfTheObject)
        self.sbCapacitance.setValue(self.model.capacity)
        self.sbPower.setValue(self.model.power)
        self.tbPowerUnit.setText(self.model.powerUnit)
        self.sbSpeed.setValue(self.model.dataTransferSpeed)
        self.sbMaxDistanceOfBRZone.setValue(self.model.buildingRestructionZoneDistance)
        self.sbBottomBorderHeight.setValue(self.model.buildingRestructionZoneHeight)
        self.sbWearPercentage.setValue(self.model.wear)
        self.tbNote.setText(self.model.note)


    def __closeDlg(self):
        self.close()





