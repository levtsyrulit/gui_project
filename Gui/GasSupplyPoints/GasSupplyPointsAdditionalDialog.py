import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

from ...Enums.DlgMode import DlgMode

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'GasSupplyPointsAdditionalDialog.ui'))

class GasSupplyPointsAdditionalDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, model, mode = DlgMode.VIEW, parent=None):
        """Constructor."""
        super(GasSupplyPointsAdditionalDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model    
        self.__setMode(mode)

        self.sbActualUseOfTheObject.setClearValueMode(0)
        self.sbCapacity.setClearValueMode(0)
        self.sbPower.setClearValueMode(0)
        self.sbWearPercentage.setClearValueMode(0)
        self.sbSizeOfSanitaryProtectionZone.setClearValueMode(0)
        self.sbGuardZoneSize.setClearValueMode(0)

        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)

        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.sbActualUseOfTheObject.setEnabled(False)
            self.sbCapacity.setEnabled(False)
            self.sbPower.setEnabled(False)
            self.tbPowerUnit.setReadOnly(True)
            self.sbWearPercentage.setEnabled(False)
            self.sbSizeOfSanitaryProtectionZone.setEnabled(False)
            self.sbGuardZoneSize.setEnabled(False)
            self.tbNote.setReadOnly(True)
            pass

    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.actualUseOfTheObject = self.sbActualUseOfTheObject.value()
        self.model.capacity = self.sbCapacity.value()
        self.model.power = self.sbPower.value()
        self.model.powerUnit = self.tbPowerUnit.text()
        self.model.wear = self.sbWearPercentage.value()
        self.model.sanitaryProtectionZoneSize = self.sbSizeOfSanitaryProtectionZone.value()
        self.model.guardZoneSize = self.sbGuardZoneSize.value()
        self.model.note = self.tbNote.text()

    def __initFields(self):
        self.sbActualUseOfTheObject.setValue(self.model.actualUseOfTheObject)
        self.sbCapacity.setValue(self.model.capacity)
        self.sbPower.setValue(self.model.power)
        self.tbPowerUnit.setText(self.model.powerUnit)
        self.sbWearPercentage.setValue(self.model.wear)
        self.sbSizeOfSanitaryProtectionZone.setValue(self.model.sanitaryProtectionZoneSize)
        self.sbGuardZoneSize.setValue(self.model.guardZoneSize)
        self.tbNote.setText(self.model.note)
                
    def __closeDlg(self):
        self.close()





            