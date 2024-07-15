import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'WaterSupplyNetworksAdditionalDialog.ui'))


class WaterSupplyNetworksAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(WaterSupplyNetworksAdditionalDialog, self).__init__(parent)
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
        self.sbHatchwayRinkMark.setClearValueMode(0)
        self.sbPipeTopMark.setClearValueMode(0)
        self.sbPipeBottomMark.setClearValueMode(0)
        self.sbGroundMark.setClearValueMode(0)
        self.sbCrosswalkHeight.setClearValueMode(0)
        self.sbGasketNumber.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbMaterial, ds.Dictionary11G.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbConstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbUndergroundLaying, ds.DictionaryCT3.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbMaterialCT4, ds.DictionaryCT4.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbThermalInsulation, ds.DictionaryCT5.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveType, ds.DictionaryCT6.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveMaterial, ds.DictionaryCT7.getElements())
        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.sbPipelineDiameter.setReadOnly(True)
            self.sbPipelineOuterDiameter.setReadOnly(True)
            self.sbOccurrenceDepth.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbNumber.setReadOnly(True)
            self.cbMaterial.setEnabled(False)
            self.sbHatchwayRinkMark.setReadOnly(True)
            self.sbPipeTopMark.setReadOnly(True)
            self.sbPipeBottomMark.setReadOnly(True)
            self.sbGroundMark.setReadOnly(True)
            self.sbCrosswalkHeight.setReadOnly(True)
            self.sbGasketNumber.setReadOnly(True)
            self.tbHatchwayState.setEnabled(False)
            self.cbIsWaterSupplyZone.setEnabled(False)
            self.cbConstructions.setEnabled(False)
            self.cbUndergroundLaying.setEnabled(False)
            self.cbMaterialCT4.setEnabled(False)
            self.cbThermalInsulation.setEnabled(False)
            self.cbSleeveType.setEnabled(False)
            self.cbSleeveMaterial.setEnabled(False)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.diameter = self.sbPipelineDiameter.value()
        self.model.pipelineOuterDiameter = self.sbPipelineOuterDiameter.value()
        self.model.occurrenceDepth = self.sbOccurrenceDepth.value()
        self.model.material = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterial)
        self.model.wear = self.sbWearPercentage.value()
        self.model.number = self.sbNumber.value()
        self.model.hatchwayRingMark = self.sbHatchwayRinkMark.value()
        self.model.pipeTopMark = self.sbPipeTopMark.value()
        self.model.pipeBottomMark = self.sbPipeBottomMark.value()
        self.model.groundMark = self.sbGroundMark.value()
        self.model.crosswalkHeight = self.sbCrosswalkHeight.value()
        self.model.gasketNumber = self.sbGasketNumber.value()
        self.model.hatchwayState = self.tbHatchwayState.text()
        self.model.isWaterSupplyZone = True if self.cbIsWaterSupplyZone.checkState() == 2 else False
        self.model.constructions = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbConstructions)
        self.model.undergroundLaying = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbUndergroundLaying)
        self.model.materialCT4 = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterialCT4)
        self.model.thermalInsulation = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbThermalInsulation)
        self.model.sleeveType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveType)
        self.model.sleeveMaterial = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveMaterial)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbPipelineDiameter.setValue(self.model.diameter)
        self.sbPipelineOuterDiameter.setValue(self.model.pipelineOuterDiameter)
        self.sbOccurrenceDepth.setValue(self.model.occurrenceDepth)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterial, self.model.material)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbNumber.setValue(self.model.number)
        self.sbHatchwayRinkMark.setValue(self.model.hatchwayRingMark)
        self.sbPipeTopMark.setValue(self.model.pipeTopMark)
        self.sbPipeBottomMark.setValue(self.model.pipeBottomMark)
        self.sbGroundMark.setValue(self.model.groundMark)
        self.sbCrosswalkHeight.setValue(self.model.crosswalkHeight)
        self.sbGasketNumber.setValue(self.model.gasketNumber)
        self.tbHatchwayState.setText(self.model.hatchwayState)
        self.cbIsWaterSupplyZone.setCheckState(2 if self.model.isWaterSupplyZone == True else 0)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbConstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbUndergroundLaying, self.model.undergroundLaying)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterialCT4, self.model.materialCT4)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbThermalInsulation, self.model.thermalInsulation)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveType, self.model.sleeveType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveMaterial, self.model.sleeveMaterial)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()