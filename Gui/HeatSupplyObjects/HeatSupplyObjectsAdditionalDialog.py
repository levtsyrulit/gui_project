import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'HeatSupplyObjectsAdditionalDialog.ui'))

class HeatSupplyObjectsAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(HeatSupplyObjectsAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbActualUse.setClearValueMode(0)
        self.sbElectricPower.setClearValueMode(0)
        self.sbThermalPower.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbMainTypeOfFuel, ds.Dictionary11O.getElements())
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.cbMainTypeOfFuel.setEnabled(False)
            self.sbActualUse.setReadOnly(True)
            self.sbElectricPower.setReadOnly(True)
            self.sbThermalPower.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbSizeOfSanitaryProtectionZone.setReadOnly(True)
            self.sbGuardZoneSize.setReadOnly(True)
            self.tbNote.setReadOnly(True)
            pass

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.mainTypeOfFuel = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMainTypeOfFuel)
        self.model.actualUse = self.sbActualUse.value()
        self.model.electricPower = self.sbElectricPower.value()
        self.model.thermalPower = self.sbThermalPower.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.sanitaryProtectionZoneSize = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMainTypeOfFuel, self.model.mainTypeOfFuel)
        self.sbActualUse.setValue(self.model.actualUse)
        self.sbElectricPower.setValue(self.model.electricPower)
        self.sbThermalPower.setValue(self.model.thermalPower)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitaryProtectionZoneSize)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





