import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'MagistralPipelinesNetworksAdditionalDialog.ui'))

class MagistralPipelinesNetworksAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(MagistralPipelinesNetworksAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbLength.setClearValueMode(0)
        self.sbOperatingPressure.setClearValueMode(0)
        self.sbPipelineDiameter.setClearValueMode(0)
        self.sbNumber.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)
        self.sbMinimalLengthZoneSize.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbMaterial, ds.Dictionary11G.getElements())
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.sbOperatingPressure.setReadOnly(True)
            self.sbPipelineDiameter.setReadOnly(True)
            self.sbNumber.setReadOnly(True)
            self.cbMaterial.setEnabled(False)
            self.sbWearPercentage.setReadOnly(True)
            self.sbSizeOfSanitaryProtectionZone.setReadOnly(True)
            self.sbGuardZoneSize.setReadOnly(True)
            self.sbMinimalLengthZoneSize.setReadOnly(True)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.operatingPressure = self.sbOperatingPressure.value()
        self.model.diameter = self.sbPipelineDiameter.value()
        self.model.material = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterial)
        self.model.wear = self.sbWearPercentage.value()
        self.model.number = self.sbNumber.value()
        self.model.sanitaryProtectionZoneSize = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.minimalLengthZoneSize = self.sbMinimalLengthZoneSize.value()
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbOperatingPressure.setValue(self.model.operatingPressure)
        self.sbPipelineDiameter.setValue(self.model.diameter)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterial, self.model.material)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbNumber.setValue(self.model.number)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitaryProtectionZoneSize)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.sbMinimalLengthZoneSize.setValue(self.model.sanitaryProtectionZoneSize)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





