from qgis.core import QgsProject
from ..Models.DictionaryModel import DictionaryModel

class DictionariesService():
    def __init__(self):
        self.DictionariesList = {}
        self.Dictionary11A = DictionaryService("Справочник 11A")
        self.DictionariesList['11A'] = self.Dictionary11A
        self.Dictionary11B = DictionaryService("Справочник 11B")
        self.DictionariesList['11B'] = self.Dictionary11B
        self.Dictionary11C = DictionaryService("Справочник 11C")
        self.DictionariesList['11C'] = self.Dictionary11C
        self.Dictionary11D = DictionaryService("Справочник 11D")
        self.DictionariesList['11D'] = self.Dictionary11D
        self.Dictionary11E = DictionaryService("Справочник 11E")
        self.DictionariesList['11E'] = self.Dictionary11E
        self.Dictionary11F = DictionaryService("Справочник 11F")
        self.DictionariesList['11F'] = self.Dictionary11F
        self.Dictionary11I = DictionaryService("Справочник 11I")
        self.DictionariesList['11I'] = self.Dictionary11I
        self.Dictionary11J = DictionaryService("Справочник 11J")
        self.DictionariesList['11J'] = self.Dictionary11J
        self.Dictionary11K = DictionaryService("Справочник 11K")
        self.DictionariesList['11K'] = self.Dictionary11K
        self.Dictionary11H = DictionaryService("Справочник 11H")
        self.DictionariesList['11H'] = self.Dictionary11H
        self.Dictionary11L = DictionaryService("Справочник 11L")
        self.DictionariesList['11L'] = self.Dictionary11L
        self.Dictionary11M = DictionaryService("Справочник 11M")
        self.DictionariesList['11M'] = self.Dictionary11M
        self.Dictionary11N = DictionaryService("Справочник 11N")
        self.DictionariesList['11N'] = self.Dictionary11N
        self.Dictionary11G = DictionaryService("Справочник 11G")
        self.DictionariesList['11G'] = self.Dictionary11G
        self.Dictionary11O = DictionaryService("Справочник 11O")
        self.DictionariesList['11O'] = self.Dictionary11O
        self.Dictionary11P = DictionaryService("Справочник 11P")
        self.DictionariesList['11P'] = self.Dictionary11P
        self.Dictionary11R = DictionaryService("Справочник 11R")
        self.DictionariesList['11R'] = self.Dictionary11R
        self.Dictionary11Q = DictionaryService("Справочник 11Q")
        self.DictionariesList['11Q'] = self.Dictionary11Q
        self.Dictionary11S = DictionaryService("Справочник 11S")
        self.DictionariesList['11S'] = self.Dictionary11S
        self.Dictionary11T = DictionaryService("Справочник 11T")
        self.DictionariesList['11T'] = self.Dictionary11T
        self.Dictionary11V = DictionaryService("Справочник 11V")
        self.DictionariesList['11V'] = self.Dictionary11V
        self.Dictionary11U = DictionaryService("Справочник 11U")
        self.DictionariesList['11U'] = self.Dictionary11U
        self.Dictionary11W = DictionaryService("Справочник 11W")
        self.DictionariesList['11W'] = self.Dictionary11W
        self.Dictionary11X = DictionaryService("Справочник 11X")
        self.DictionariesList['11X'] = self.Dictionary11X
        self.Dictionary11Y = DictionaryService("Справочник 11Y")
        self.DictionariesList['11Y'] = self.Dictionary11Y
        self.Dictionary11Z = DictionaryService("Справочник 11Z")
        self.DictionariesList['11Z'] = self.Dictionary11Z
        self.DictionaryCT1 = DictionaryService("Справочник CT1")
        self.DictionariesList['CT1'] = self.DictionaryCT1
        self.DictionaryCT2 = DictionaryService("Справочник CT2")
        self.DictionariesList['CT2'] = self.DictionaryCT2
        self.DictionaryCT3 = DictionaryService("Справочник CT3")
        self.DictionariesList['CT3'] = self.DictionaryCT3
        self.DictionaryCT4 = DictionaryService("Справочник CT4")
        self.DictionariesList['CT4'] = self.DictionaryCT4
        self.DictionaryCT5 = DictionaryService("Справочник CT5")
        self.DictionariesList['CT5'] = self.DictionaryCT5
        self.DictionaryCT6 = DictionaryService("Справочник CT6")
        self.DictionariesList['CT6'] = self.DictionaryCT6
        self.DictionaryCT7 = DictionaryService("Справочник CT7")
        self.DictionariesList['CT7'] = self.DictionaryCT7
        self.DictionaryCT8 = DictionaryService("Справочник CT8")
        self.DictionariesList['CT8'] = self.DictionaryCT8
        self.DictionaryCT9 = DictionaryService("Справочник CT9")
        self.DictionariesList['CT9'] = self.DictionaryCT9
        self.DictionaryCT10 = DictionaryService("Справочник CT10")
        self.DictionariesList['CT10'] = self.DictionaryCT10
        self.DictionaryCT11 = DictionaryService("Справочник CT11")
        self.DictionariesList['CT11'] = self.DictionaryCT11
        self.DictionaryCT12 = DictionaryService("Справочник CT12")
        self.DictionariesList['CT12'] = self.DictionaryCT12
        self.DictionaryCT13 = DictionaryService("Справочник CT13")
        self.DictionariesList['CT13'] = self.DictionaryCT13
        self.DictionaryCT17 = DictionaryService("Справочник CT17")
        self.DictionariesList['CT17'] = self.DictionaryCT17
        self.DictionaryCT18 = DictionaryService("Справочник CT18")
        self.DictionariesList['CT18'] = self.DictionaryCT18
        self.DictionaryCT19 = DictionaryService("Справочник CT19")
        self.DictionariesList['CT19'] = self.DictionaryCT19
        self.DictionaryCT20 = DictionaryService("Справочник CT20")
        self.DictionariesList['CT20'] = self.DictionaryCT20
        self.DictionaryCT21 = DictionaryService("Справочник CT21")
        self.DictionariesList['CT21'] = self.DictionaryCT21
        self.DictionaryCT22 = DictionaryService("Справочник CT22")
        self.DictionariesList['CT22'] = self.DictionaryCT22
        self.DictionaryCT23 = DictionaryService("Справочник CT23")
        self.DictionariesList['CT23'] = self.DictionaryCT23
        self.DictionaryCT24 = DictionaryService("Справочник CT24")
        self.DictionariesList['CT24'] = self.DictionaryCT24
        self.DictionaryCT25 = DictionaryService("Справочник CT25")
        self.DictionariesList['CT25'] = self.DictionaryCT25
        self.DictionaryCT26 = DictionaryService("Справочник CT26")
        self.DictionariesList['CT26'] = self.DictionaryCT26
        self.DictionaryCT27 = DictionaryService("Справочник CT27")
        self.DictionariesList['CT27'] = self.DictionaryCT27
        self.DictionaryCT28 = DictionaryService("Справочник CT28")
        self.DictionariesList['CT28'] = self.DictionaryCT28
        self.DictionaryCT29 = DictionaryService("Справочник CT29")
        self.DictionariesList['CT29'] = self.DictionaryCT29
        self.DictionaryCT30 = DictionaryService("Справочник CT30")
        self.DictionariesList['CT30'] = self.DictionaryCT30

    """Формирование списка идентификаторов элементов справочника по его значениям"""
    def getElementsByValues(self, values, allElements):
        elements = []
        if values:
            els = [x for x in allElements if x.value in values]
            if els: elements.extend(els)
        
        return elements

    """Формирование строки из списка идентификаторов элементов справочника по его значениямб разделенный указанным разделителем"""
    def getIDsByValuesAsString(self, values, allElements, separator = ","):
        elements = self.getElementsByValues(values, allElements)
        return separator.join([x.id for x in elements])

    """Получения справочника по его иимени"""
    def getDictionaryByName(self, dictionaryName):
        try:
            return self.DictionariesList[dictionaryName]
        except:
            return None

class DictionaryService():
    def __init__(self, dictionaryName):
        self.__initLayer(dictionaryName)

    """Инициализация слоя"""
    def __initLayer(self, dictionaryName):
        layers = QgsProject.instance().mapLayersByName(dictionaryName)
        if layers:
            self.layer = layers[0] 
            return
        raise Exception("Не найден слой ""{}""".format(dictionaryName))

    """Получение списка всех значений элементов справочника"""
    def getValues(self):
        features = self.layer.getFeatures()
        return list(map(lambda f: f["Value"], features))

    """Получение списка всех элементов справочника"""
    def getElements(self, parent = None):
        features = self.layer.getFeatures() #список всех элементов справочниках.
        return list(map(lambda f: DictionaryModel(f["ID"], f["Name"], f["Value"]), features)) #, f["ParentDictionaryName"], f["ParentElementName"]), features))

    """Получение списка всех элементов справочника кроме конкретных"""
    def getElementsExcept(self, excList):
        features = self.layer.getFeatures()  # список всех элементов справочниках.
        resList = []

        for feature in features:
            if (feature["Name"] not in excList):
                resList.append(DictionaryModel(feature["ID"], feature["Name"], feature["Value"]))

        return resList

    """Получение конкретных элементов справочника"""
    def getSpecificElements(self, onlyList):
        features = self.layer.getFeatures()  # список всех элементов справочниках.
        resList = []

        for feature in features:
            if (feature["Name"] in onlyList):
                resList.append(DictionaryModel(feature["ID"], feature["Name"], feature["Value"]))

        return resList

    """Установка элементов справочника в качестве источника данных в выпадающий список"""
    def setComboBoxItems(self, comboBox, parent = None):
        comboBox.clear()
        elements = self.getElements(parent)

        for element in elements:
            comboBox.addItem(element.value, element)
