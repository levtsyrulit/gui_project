import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CommunicationNetworksAdditionalDialog.ui'))

class CommunicationNetworksAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(CommunicationNetworksAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbLength.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbWiresNumber.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbCommunicationLinesType, ds.Dictionary11M.getElements()) #communication line type
        self.dictionaryComboBoxHelper.setItems(self.cbConstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbUndergroundLaying, ds.DictionaryCT3.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbCommunicationNetworkType, ds.DictionaryCT20.getElements()) #network В ед. числе
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.cbCommunicationLinesType.setEnabled(False)
            self.sbGuardZoneSize.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbWiresNumber.setReadOnly(True)
            self.cbConstructions.setEnabled(False)
            self.cbUndergroundLaying.setEnabled(False)
            self.cbCommunicationNetworkType.setEnabled(False)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.communicationLinesType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCommunicationLinesType)
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.wiresNumber = self.sbWiresNumber.value()
        self.model.constructions = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbConstructions)
        self.model.undergroundLaying = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbUndergroundLaying)
        self.model.communicationNetworkType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCommunicationNetworkType)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCommunicationLinesType, self.model.communicationLinesType)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbWiresNumber.setValue(self.model.wiresNumber)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbConstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbUndergroundLaying, self.model.undergroundLaying)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCommunicationNetworkType, self.model.communicationNetworkType)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





