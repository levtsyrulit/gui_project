import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'GasNetworkAdditionalAttributesDialog.ui'))

class GasPipeAdditionalAttributesDialog(QtWidgets.QDialog, FORM_CLASS):   
    def __init__(self, model, mode = DlgMode.VIEW, parent=None):
        """Constructor."""
        super(GasPipeAdditionalAttributesDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model    
        self.__setMode(mode)

        self.sbConstructionLength.setClearValueMode(0)
        self.sbOperatingPressureInPipeline.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)
        self.sbPipelineDiameter.setClearValueMode(0)
        self.sbOuterPipelineDiameter.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbNumberOfPipes.setClearValueMode(0)
        self.sbHeight.setClearValueMode(0)
        self.sbDepth.setClearValueMode(0)
        self.sbVolume.setClearValueMode(0)
        self.sbArea.setClearValueMode(0)
        self.sbBuiltUpArea.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbPipelineMaterial, ds.Dictionary11G.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbConstructions, ds.DictionaryCT2.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbUndergroundLaying, ds.DictionaryCT3.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbMaterialCT4, ds.DictionaryCT4.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbThermalInsulation, ds.DictionaryCT5.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveType, ds.DictionaryCT6.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbSleeveMaterial, ds.DictionaryCT7.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbGasType, ds.DictionaryCT11.getElements())

        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbOperatingPressureInPipeline.setReadOnly(True)
            self.sbSizeOfSanitaryProtectionZone.setReadOnly(True)
            self.sbGuardZoneSize.setReadOnly(True)
            self.sbPipelineDiameter.setReadOnly(True)
            self.sbOuterPipelineDiameter.setReadOnly(True)
            self.cbPipelineMaterial.setEnabled(False)
            self.sbWearPercentage.setReadOnly(True)
            self.sbNumberOfPipes.setReadOnly(True)
            self.sbHeight.setReadOnly(True)
            self.sbDepth.setReadOnly(True)
            self.sbVolume.setReadOnly(True)
            self.sbArea.setReadOnly(True)
            self.sbBuiltUpArea.setReadOnly(True)
            self.cbConstructions.setEnabled(False)
            self.cbUndergroundLaying.setEnabled(False)
            self.cbMaterialCT4.setEnabled(False)
            self.cbThermalInsulation.setEnabled(False)
            self.cbSleeveType.setEnabled(False)
            self.cbSleeveMaterial.setEnabled(False)
            self.cbGasType.setEnabled(False)
            self.sbConstructionLength.setReadOnly(True)
            self.tbNote.setReadOnly(True)

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.length = self.sbConstructionLength.value()
        self.model.operating_pressure = self.sbOperatingPressureInPipeline.value()
        self.model.sanitary_protection_zone_size = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guard_zone_size = self.sbGuardZoneSize.value()
        self.model.diameter = self.sbPipelineDiameter.value()
        self.model.diameter_outer = self.sbOuterPipelineDiameter.value()
        self.model.material = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbPipelineMaterial)
        self.model.wear = self.sbWearPercentage.value()
        self.model.number = self.sbNumberOfPipes.value()
        self.model.height = self.sbHeight.value()
        self.model.depth = self.sbDepth.value()
        self.model.volume = self.sbVolume.value()
        self.model.area = self.sbArea.value()
        self.model.area_built_up = self.sbBuiltUpArea.value()
        self.model.constructions = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbConstructions)
        self.model.undergroundLaying = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbUndergroundLaying)
        self.model.materialCT4 = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbMaterialCT4)
        self.model.thermalInsulation = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbThermalInsulation)
        self.model.sleeveType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveType)
        self.model.sleeveMaterial = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbSleeveMaterial)
        self.model.gasType = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbGasType)
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbConstructionLength.setValue(self.model.length)
        self.sbOperatingPressureInPipeline.setValue(self.model.operating_pressure)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitary_protection_zone_size)
        self.sbGuardZoneSize.setValue(self.model.guard_zone_size)
        self.sbPipelineDiameter.setValue(self.model.diameter)
        self.sbOuterPipelineDiameter.setValue(self.model.diameter_outer)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString( self.cbPipelineMaterial, self.model.material)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbNumberOfPipes.setValue(self.model.number)
        self.sbHeight.setValue(self.model.height)
        self.sbDepth.setValue(self.model.depth)
        self.sbVolume.setValue(self.model.volume)
        self.sbArea.setValue(self.model.area)
        self.sbBuiltUpArea.setValue(self.model.area_built_up)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbConstructions, self.model.constructions)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbUndergroundLaying, self.model.undergroundLaying)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbMaterialCT4, self.model.materialCT4)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbThermalInsulation, self.model.thermalInsulation)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveType, self.model.sleeveType)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbSleeveMaterial, self.model.sleeveMaterial)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString(self.cbGasType, self.model.gasType)
        self.tbNote.setText(self.model.note)
                
    def __closeDlg(self):
        self.close()





            