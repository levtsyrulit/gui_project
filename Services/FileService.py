import os
import base64
import tempfile
import platform
import subprocess

class FileService():
    def __init__(self):
        pass

    def createTmpFolder(self):
        return tempfile.mkdtemp(prefix="gisec_tmp_")

    def saveFileToFolder(self, folder, fileName, fileContentString):
        fullPath = os.path.join(folder, fileName)
        fileContent = base64.b64decode(bytes(fileContentString, 'utf-8'))
        
        with open(fullPath, 'wb') as f:
            f.write(fileContent)
    
    def openFile(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])