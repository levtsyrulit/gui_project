import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal
from PyQt5.QtCore import QDate

from ...Enums.DlgMode import DlgMode
from ...Services.DictionaryService import DictionariesService
from ...Helpers.DictionaryComboBoxHelper import DictionaryComboBoxHelper


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ObjectPassportDialog.ui'))

class ObjectPassportDialog(QtWidgets.QDialog, FORM_CLASS):
    closingDlg = pyqtSignal()

    def __init__(self, model, mode, parent=None):
        """Constructor."""
        super(ObjectPassportDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.model = model
        self.__setMode(mode)
        self.btnCancel.clicked.connect(self.__closeDlg)
        self.btnOk.clicked.connect(self.__acceptChanges)
        self.setModal(True)
        
        ds = DictionariesService()
        self.dictionaryComboBoxHelper = DictionaryComboBoxHelper()
        self.dictionaryComboBoxHelper.setItems(self.cbTypeOfProperty, ds.Dictionary11D.getElements())
        self.dictionaryComboBoxHelper.setItems(self.cbObjectValue, ds.Dictionary11Z.getElements())
        self.dteYearOfCommissioning.setNullRepresentation("")
        self.dteYearOfReconstruction.setNullRepresentation("")

        self.__initFields()

    def __setMode(self, mode):
        self.mode = mode
        if self.mode == DlgMode.VIEW:
            self.tbBalanceHolder.setReadOnly(True)
            self.cbTypeOfProperty.setEnabled(False)
            self.tbOperationOgranization.setReadOnly(True)
            self.cbObjectValue.setEnabled(False)
            self.dteYearOfCommissioning.setEnabled(False)
            self.dteYearOfReconstruction.setEnabled(False)
            self.tbCreationDate.setReadOnly(True)
            self.tbUpdateDate.setReadOnly(True)
            self.tbCreator.setReadOnly(True)
            self.tbEditor.setReadOnly(True)
            self.tbComment.setReadOnly(True)
            pass   

    def __closeDlg(self):
        self.close()
        
    def __acceptChanges(self):
        self.__fillModel()
        self.__closeDlg()

    def __fillModel(self):
        self.model.balanceholder = self.tbBalanceHolder.text()
        self.model.property_type = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbTypeOfProperty)
        self.model.operating_organisation = self.tbOperationOgranization.text()
        self.model.role_of_object = self.dictionaryComboBoxHelper.getKeyStringForSelectedElements(self.cbObjectValue)
        self.model.comissioning_year = self.dteYearOfCommissioning.dateTime()
        self.model.reconstruction_year = self.dteYearOfReconstruction.dateTime()
        self.model.comment = self.tbComment.text()
        
        #self.model.creation_date = self.tbCreationDate.date().toPyDate()
        #self.model.update_date = self.tbUpdateDate.date().toPyDate()
        #self.model.creator = self.tbCreator.text()
        #self.model.editor = self.tbEditor.text()

    def __initFields(self):        
        self.tbBalanceHolder.setText(self.model.balanceholder)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString( self.cbTypeOfProperty, self.model.property_type)
        self.tbOperationOgranization.setText(self.model.operating_organisation)
        self.dictionaryComboBoxHelper.setSelectedElementsFromKeyString( self.cbObjectValue, self.model.role_of_object)

        if self.model.comissioning_year and not self.model.comissioning_year.isNull():
           self.dteYearOfCommissioning.setDateTime(self.model.comissioning_year)
        else:
            self.dteYearOfCommissioning.clear()

        if self.model.reconstruction_year and not self.model.reconstruction_year.isNull():            
            self.dteYearOfReconstruction.setDateTime(self.model.reconstruction_year)
        else:
            self.dteYearOfReconstruction.clear()

        self.tbCreationDate.setText( self.model.creation_date.toString("dd-MM-yyyy HH:mm") if self.model.creation_date and not self.model.creation_date.isNull()  else "")
        self.tbUpdateDate.setText(self.model.update_date.toString("dd-MM-yyyy HH:mm") if self.model.update_date and not self.model.update_date.isNull() else "")
        self.tbCreator.setText(self.model.creator)
        self.tbEditor.setText(self.model.editor)
        self.tbComment.setText(self.model.comment)