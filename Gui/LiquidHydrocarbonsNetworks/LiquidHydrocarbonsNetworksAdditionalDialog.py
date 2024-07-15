import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'LiquidHydrocarbonsNetworksAdditionalDialog.ui'))

class LiquidHydrocarbonsNetworksAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, specialPurposePipelineEnabled, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(LiquidHydrocarbonsNetworksAdditionalDialog, self).__init__(parent)
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
        self.sbPipesNumber.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)
        self.sbMinimalLengthZoneSize.setClearValueMode(0)
        self.sbPipelineOuterDiameter.setClearValueMode(0)
        self.sbOccurrenceDepth.setClearValueMode(0)
        self.sbHatchwayRingMark.setClearValueMode(0)
        self.sbTrayMark.setClearValueMode(0)
        self.sbPipeTopMark.setClearValueMode(0)
        self.sbPipeBottomMark.setClearValueMode(0)
        self.sbGroundMark.setClearValueMode(0)
        self.sbGasketNumber.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbConstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbUndergroundLaying, ds.DictionaryCT3.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbMaterialCT4, ds.DictionaryCT4.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSpecialPurposePipeline, ds.DictionaryCT21.getElements())

        self.__initFields()

        if specialPurposePipelineEnabled == True:
            self.cbSpecialPurposePipeline.setEnabled(self.mode != DlgMode.VIEW)
        else:
            self.cbSpecialPurposePipeline.setEnabled(False)
            self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSpecialPurposePipeline, DictionaryComboBoxHelper.UNSELECTED_ITEM.id)

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.sbOperatingPressure.setReadOnly(True)
            self.sbPipelineDiameter.setReadOnly(True)
            self.sbPipelineOuterDiameter.setReadOnly(True)
            self.sbPipesNumber.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbSizeOfSanitaryProtectionZone.setReadOnly(True)
            self.sbGuardZoneSize.setReadOnly(True)
            self.sbMinimalLengthZoneSize.setReadOnly(True)
            self.sbOccurrenceDepth.setReadOnly(True)
            self.sbHatchwayRingMark.setReadOnly(True)
            self.sbTrayMark.setReadOnly(True)
            self.sbPipeTopMark.setReadOnly(True)
            self.sbPipeBottomMark.setReadOnly(True)
            self.sbGroundMark.setReadOnly(True)
            self.sbGasketNumber.setReadOnly(True)
            self.cbConstructions.setEnabled(False)
            self.cbUndergroundLaying.setEnabled(False)
            self.cbMaterialCT4.setEnabled(False)
            self.cbSpecialPurposePipeline.setEnabled(False)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.operatingPressure = self.sbOperatingPressure.value()
        self.model.diameter = self.sbPipelineDiameter.value()
        self.model.pipelineOuterDiameter  = self.sbPipelineOuterDiameter.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.number = self.sbPipesNumber.value()
        self.model.sanitaryProtectionZoneSize = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.minimalLengthZoneSize = self.sbMinimalLengthZoneSize.value()
        self.model.occurrenceDepth  = self.sbOccurrenceDepth.value()
        self.model.hatchwayRingMark  = self.sbHatchwayRingMark.value()
        self.model.trayMark  = self.sbTrayMark.value()
        self.model.pipeTopMark  = self.sbPipeTopMark.value()
        self.model.pipeBottomMark  = self.sbPipeBottomMark.value()
        self.model.groundMark  = self.sbGroundMark.value()
        self.model.gasketNumber  = self.sbGasketNumber.value()
        self.model.constructions  = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbConstructions)
        self.model.undergroundLaying  = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbUndergroundLaying)
        self.model.materialCT4  = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterialCT4)
        self.model.specialPurposePipeline = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSpecialPurposePipeline)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbOperatingPressure.setValue(self.model.operatingPressure)
        self.sbPipelineDiameter.setValue(self.model.diameter)
        self.sbPipelineOuterDiameter.setValue(self.model.pipelineOuterDiameter)
        self.sbPipesNumber.setValue(self.model.number)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitaryProtectionZoneSize)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.sbMinimalLengthZoneSize.setValue(self.model.minimalLengthZoneSize)
        self.sbOccurrenceDepth.setValue(self.model.occurrenceDepth)
        self.sbHatchwayRingMark.setValue(self.model.hatchwayRingMark)
        self.sbTrayMark.setValue(self.model.trayMark)
        self.sbPipeTopMark.setValue(self.model.pipeTopMark)
        self.sbPipeBottomMark.setValue(self.model.pipeBottomMark)
        self.sbGroundMark.setValue(self.model.groundMark)
        self.sbGasketNumber.setValue(self.model.gasketNumber)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbConstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbUndergroundLaying, self.model.undergroundLaying)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterialCT4, self.model.materialCT4)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSpecialPurposePipeline, self.model.specialPurposePipeline)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





