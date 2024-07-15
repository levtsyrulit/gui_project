import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtGui import QMovie

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ProgressDialog.ui'))

class ProgressDialog(QtWidgets.QDialog, FORM_CLASS):

    def __init__(self, message, action, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi(self)
        self.movie = QMovie("progress.gif")
        self.lblGif.setMovie(self.movie)
        self.movie.start()
        self.lblMessage.setText(message)
        self.lblAction.setText(action)

    def setMessage(self, message):
        self.lblMessage.setText(message)
        self.repaint()
    
    def setAction(self, action):
        self.lblAction.setText(action)
        self.repaint()
        self.update()
