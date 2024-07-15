import json, requests, os.path
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction,QMessageBox, QListWidget, QListWidgetItem
from qgis.PyQt import QtWidgets
from qgis.core import QgsProject,QgsVectorLayer, QgsDataSourceUri
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt
from PyQt5.QtSql import *
from ..resources import *
from ..projects_class import Project

class AdministrationServerService():
    def __init__(self) -> None:
        self.administrationServerURL = QSettings(QtCore.QSettings.NativeFormat, QtCore.QSettings.UserScope, "Competentit", "GisEC").value('ip')

    """Получение списка проектов"""
    def getProjects(self):        
        projects = []        
        url = self.administrationServerURL  + "/api/QGis/projects"

        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as req_exc:
            raise req_exc
            
        responseJson = json.loads(response.text)
        for i in range(len(responseJson)):
            if 'name' and 'connectionString' and 'databaseName' in responseJson[i].keys():
                project = Project(responseJson[i]['name'], responseJson[i]['databaseName'],
                                            responseJson[i]['connectionString'])
                projects.append(project)
            else:
                raise ValueError

        return projects

    """Получение имени пользователя по логину."""
    def getUserNameBylogin(self, login):        
        url = "{0}/api/users/name/{1}".format(self.administrationServerURL, login)
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                print("Ошибка получения имени пользователя по адресу '{0}': Код {1}, Ошибка: {2}".format(url, response.status_code, response.text))
            
        except:
            return None
            
        return None

    """Получение списка с WepAPI DXF-файлов"""
    def getGeometryList(self, dxfFilePath, listOfSourceFilesPaths):
        dxfPath, dxfName = os.path.split(dxfFilePath)
        url = self.administrationServerURL + "/api/tools/import/dxf/spb?name=" + dxfName

        files = [('files', open(dxfFilePath, 'rb'))]
        for file in listOfSourceFilesPaths:
            files.append(("files", open(file, 'rb')))

        try:
            response = requests.post(url, files=files, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as req_exc: 
            raise req_exc
        
        responseJson = json.loads(response.text)
        return responseJson

    """Получение списка файлов фолдера с содержимым"""
    def downloadFolderFiles(self, folderName):
        url = self.administrationServerURL + "/api/tools/download/folder/" + folderName
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as req_exc: 
            raise req_exc
        
        responseJson = json.loads(response.text)
        return responseJson
