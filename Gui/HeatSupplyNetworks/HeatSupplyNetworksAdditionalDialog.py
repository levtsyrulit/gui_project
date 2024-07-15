import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'HeatSupplyNetworksAdditionalDialog.ui'))

class HeatSupplyNetworksAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode=DlgMode.VIEW, parent=None):
        """Constructor."""
        super(HeatSupplyNetworksAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)

        self.sbLength.setClearValueMode(0)
        self.sbSupplyPipeDiameter.setClearValueMode(0)
        self.sbReturnPipeDiameter.setClearValueMode(0)
        self.sbSupplyPipeDiameterHotWater.setClearValueMode(0)
        self.sbCirculationPipeDiameter.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
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
        self.dictionaryComboBoxHelper.setItems(self.cbCounstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbUndergroundLaying, ds.DictionaryCT3.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbMaterialCT4, ds.DictionaryCT4.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbThermalInsulation, ds.DictionaryCT5.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveType, ds.DictionaryCT6.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveMaterial, ds.DictionaryCT7.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbHeatSupplyNetworkZone, ds.DictionaryCT8.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSystemType, ds.DictionaryCT9.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbLiquidType, ds.DictionaryCT10.getElements())

        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbLength.setReadOnly(True)
            self.sbSupplyPipeDiameter.setReadOnly(True)
            self.sbReturnPipeDiameter.setReadOnly(True)
            self.sbSupplyPipeDiameterHotWater.setReadOnly(True)
            self.sbCirculationPipeDiameter.setReadOnly(True)
            self.sbWearPercentage.setReadOnly(True)
            self.sbPipelineOuterDiameter.setReadOnly(True)
            self.sbOccurrenceDepth.setReadOnly(True)
            self.sbHatchwayRinkMark.setReadOnly(True)
            self.sbPipeTopMark.setReadOnly(True)
            self.sbPipeBottomMark.setReadOnly(True)
            self.sbGroundMark.setReadOnly(True)
            self.sbCrosswalkHeight.setReadOnly(True)
            self.sbGasketNumber.setReadOnly(True)
            self.tbHatchwayState.setReadOnly(True)
            self.cbCounstructions.setEnabled(False)
            self.cbUndergroundLaying.setEnabled(False)
            self.cbMaterialCT4.setEnabled(False)
            self.cbThermalInsulation.setEnabled(False)
            self.cbSleeveType.setEnabled(False)
            self.cbSleeveMaterial.setEnabled(False)
            self.cbHeatSupplyNetworkZone.setEnabled(False)
            self.cbSystemType.setEnabled(False)
            self.cbLiquidType.setEnabled(False)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbLength.value()
        self.model.supplyPipeDiameter = self.sbSupplyPipeDiameter.value()
        self.model.returnPipeDiameter = self.sbReturnPipeDiameter.value()
        self.model.hotWaterSupplyPipeDiameter = self.sbSupplyPipeDiameterHotWater.value()
        self.model.hotWaterCirculationPipeDiameter = self.sbCirculationPipeDiameter.value()
        self.model.wear = self.sbWearPercentage.value()
        self.model.pipelineOuterDiameter = self.sbPipelineOuterDiameter.value()
        self.model.occurrenceDepth = self.sbOccurrenceDepth.value()
        self.model.hatchwayRinkMark = self.sbHatchwayRinkMark.value()
        self.model.pipeTopMark = self.sbPipeTopMark.value()
        self.model.pipeBottomMark = self.sbPipeBottomMark.value()
        self.model.groundMark = self.sbGroundMark.value()
        self.model.crosswalkHeight = self.sbCrosswalkHeight.value()
        self.model.gasketNumber = self.sbGasketNumber.value()
        self.model.hatchwayState = self.tbHatchwayState.text()
        self.model.constructions = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbCounstructions)
        self.model.undergroundLaying = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbUndergroundLaying)
        self.model.materialCT4 = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterialCT4)
        self.model.thermalInsulation = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbThermalInsulation)
        self.model.sleeveType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveType)
        self.model.sleeveMaterial = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveMaterial)
        self.model.heatSupplyNetworkZone = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbHeatSupplyNetworkZone)
        self.model.systemType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSystemType)
        self.model.liquidType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbLiquidType)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbLength.setValue(self.model.length)
        self.sbSupplyPipeDiameter.setValue(self.model.supplyPipeDiameter)
        self.sbReturnPipeDiameter.setValue(self.model.returnPipeDiameter)
        self.sbSupplyPipeDiameterHotWater.setValue(self.model.hotWaterSupplyPipeDiameter)
        self.sbCirculationPipeDiameter.setValue(self.model.hotWaterCirculationPipeDiameter)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbPipelineOuterDiameter.setValue(self.model.pipelineOuterDiameter)
        self.sbOccurrenceDepth.setValue(self.model.occurrenceDepth)
        self.sbHatchwayRinkMark.setValue(self.model.hatchwayRinkMark)
        self.sbPipeTopMark.setValue(self.model.pipeTopMark)
        self.sbPipeBottomMark.setValue(self.model.pipeBottomMark)
        self.sbGroundMark.setValue(self.model.groundMark)
        self.sbCrosswalkHeight.setValue(self.model.crosswalkHeight)
        self.sbGasketNumber.setValue(self.model.gasketNumber)
        self.tbHatchwayState.setText(self.model.hatchwayState)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbCounstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbUndergroundLaying, self.model.undergroundLaying)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterialCT4, self.model.materialCT4)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbThermalInsulation, self.model.thermalInsulation)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveType, self.model.sleeveType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveMaterial, self.model.sleeveMaterial)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbHeatSupplyNetworkZone, self.model.heatSupplyNetworkZone)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSystemType, self.model.systemType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbLiquidType, self.model.liquidType)
        self.tbNote.setText(self.model.note)

    def __closeDlg(self):
        self.close()





