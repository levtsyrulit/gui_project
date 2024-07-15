import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ElectricitySupplyNetworksAdditionalDialog.ui'))

class ElectricitySupplyNetworksAdditionalAttributesDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(ElectricitySupplyNetworksAdditionalAttributesDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbLength.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)
        self.sbNumberCablesInBundle.setClearValueMode(0)
        self.sbWiresNumber.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbConstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveType, ds.DictionaryCT6.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveMaterial, ds.DictionaryCT7.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbFormFactor, ds.DictionaryCT12.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbStowageType, ds.DictionaryCT13.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbCableMark, ds.DictionaryCT17.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbCableSegments, ds.DictionaryCT18.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbCableZone, ds.DictionaryCT19.getElements())
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbSizeOfSanitaryProtectionZone.setReadOnly(True)
            self.sbGuardZoneSize.setReadOnly(True)
            self.sbNumberCablesInBundle.setReadOnly(True)
            self.sbWiresNumber.setReadOnly(True)
            self.cbConstructions.setEnabled(False)
            self.cbSleeveType.setEnabled(False)
            self.cbSleeveMaterial.setEnabled(False)
            self.cbFormFactor.setEnabled(False)
            self.cbStowageType.setEnabled(False)
            self.cbCableMark.setEnabled(False)
            self.cbCableSegments.setEnabled(False)
            self.cbCableZone.setEnabled(False)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.sanitaryProtectionZoneSize = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.numberCablesInBundle = self.sbNumberCablesInBundle.value()
        self.model.wiresNumber = self.sbWiresNumber.value()
        self.model.constructions = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbConstructions)
        self.model.sleeveType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveType)
        self.model.sleeveMaterial = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveMaterial)
        self.model.formFactor = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbFormFactor)
        self.model.stowageType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbStowageType)
        self.model.cableMark = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCableMark)
        self.model.cableSegments = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCableSegments)
        self.model.cableZone = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCableZone)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitaryProtectionZoneSize)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.sbNumberCablesInBundle.setValue(self.model.numberCablesInBundle)
        self.sbWiresNumber.setValue(self.model.wiresNumber)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbConstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveType, self.model.sleeveType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveMaterial, self.model.sleeveMaterial)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbFormFactor, self.model.formFactor)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbStowageType, self.model.stowageType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCableMark, self.model.cableMark)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCableSegments, self.model.cableSegments)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCableZone, self.model.cableZone)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





