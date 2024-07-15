import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'WastewaterNetworksAdditionalAttributesDialog.ui'))

class WastewaterNetworksAdditionalAttributesDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode = DlgMode.VIEW, parent=None):
        """Constructor."""
        super(WastewaterNetworksAdditionalAttributesDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model        
        self.__setMode(mode)

        self.sbLength.setClearValueMode(0)
        self.sbPipelineDiameter.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbNumber.setClearValueMode(0)
        self.sbPipelineOuterDiameter.setClearValueMode(0)
        self.sbOccurrenceDepth.setClearValueMode(0)
        self.sbHatchwayRingMark.setClearValueMode(0)
        self.sbGroundMark.setClearValueMode(0)
        self.sbTrayMark.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbMaterial, ds.Dictionary11G.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSewerageType, ds.DictionaryCT1.getElements())
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        self.__setReadOnly(mode == DlgMode.VIEW)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    """Перевод всех элементов формы в режим 'Только чтение'"""
    def __setReadOnly(self, readOnly = False):
        self.sbLength.setReadOnly(readOnly)
        self.sbPipelineDiameter.setReadOnly(readOnly)
        self.sbPipelineOuterDiameter.setReadOnly(readOnly)
        self.sbOccurrenceDepth.setReadOnly(readOnly)
        self.cbMaterial.setEnabled(not readOnly)
        self.sbWearPercentage.setReadOnly(readOnly)
        self.sbNumber.setReadOnly(readOnly)
        self.sbHatchwayRingMark.setReadOnly(readOnly)
        self.sbGroundMark.setReadOnly(readOnly)
        self.sbTrayMark.setReadOnly(readOnly)
        self.cbSewerageType.setEnabled(not readOnly)
        self.tbNote.setReadOnly(readOnly)

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.diameter = self.sbPipelineDiameter.value()
        self.model.pipelineOuterDiameter = self.sbPipelineOuterDiameter.value()
        self.model.occurrenceDepth = self.sbOccurrenceDepth.value()
        self.model.material = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterial)
        self.model.wear = self.sbWearPercentage.value()
        self.model.number = self.sbNumber.value()
        self.model.hatchwayRingMark = self.sbHatchwayRingMark.value()
        self.model.groundMark = self.sbGroundMark.value()
        self.model.trayMark = self.sbTrayMark.value()
        self.model.sewerageType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSewerageType)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbPipelineDiameter.setValue(self.model.diameter)
        self.sbPipelineOuterDiameter.setValue(self.model.pipelineOuterDiameter)
        self.sbOccurrenceDepth.setValue(self.model.occurrenceDepth)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterial, self.model.material)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbNumber.setValue(self.model.number)
        self.sbHatchwayRingMark.setValue(self.model.hatchwayRingMark)
        self.sbGroundMark.setValue(self.model.groundMark)
        self.sbTrayMark.setValue(self.model.trayMark)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSewerageType, self.model.sewerageType)
        self.tbNote.setText(self.model.note)
                
    def __closeDlg(self):
        self.close()





            