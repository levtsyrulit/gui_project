from ntpath import join
from PyQt5.QtCore import Qt
from qgis.gui import QgsCheckableComboBox

from ..Models.DictionaryModel import DictionaryModel

class DictionaryComboBoxHelper():
    UNSELECTED_ITEM = DictionaryModel( "unselected", "unselected",  "(не выбрано)")

    def __init__(self):
        pass

    """Инициализация элементов выпадающего списка"""
    def setItems(self, comboBox, items, parent = None):
        comboBox.clear()
        elements = [x for x in items if x.parenElementName == parent.name] if parent else items

        if isinstance(comboBox, QgsCheckableComboBox) == False:            
            comboBox.addItem(DictionaryComboBoxHelper.UNSELECTED_ITEM.value, DictionaryComboBoxHelper.UNSELECTED_ITEM)
        for element in elements:
            comboBox.addItem(element.value, element)

    """Установка текущего выделенного элемента выпадающего списка"""
    def setSelectedItem(self, comboBox, item):        
        if item:            
            comboBox.setCurrentText(item.value)

    """Установка выделенных элементов для выпадающего списка с мультивыбором"""
    def setCheckedItems(self, comboBox, items): 
        values = [x.value for x in items] if items else []       
        comboBox.setCheckedItems(values)
    
    """Получение выделенного элемента выпадающего списка"""
    def getSelectedItem(self, comboBox):        
        return comboBox.currentData()

    """Получение списка выделенных элементов выпадающего списка с мультивыбором"""
    def getCheckedItems(self, comboBox): 
        items = []
        for index in range(comboBox.count()):
          if comboBox.itemCheckState(index) == Qt.Checked:
            items.append(comboBox.itemData(index))
        
        return items

    """Получение строки-ключа, которая должна быть записана в поле, хранящие значение выбранные в выпадающем списке"""
    def getKeyStringForSelectedElements(self, comboBox):
        if isinstance(comboBox, QgsCheckableComboBox):
            items = self.getCheckedItems(comboBox)
            if len(items) > 0:
                return "{" + ",".join(['"' + x.id + '"' for x in items]) + "}"
            else:
                return None
        else:
            item = self.getSelectedItem(comboBox)
            
            return item.id if item and item.name != DictionaryComboBoxHelper.UNSELECTED_ITEM.name else None

    """Назначение выделенных элементов выпадающего списка, по строке-ключу"""
    def setSelectedElementsFromKeyString(self, comboBox, keyString):
        if not keyString or keyString == "":
            return

        ids = []
        if keyString.startswith("{"):
            tmpIDs = [x.strip('"') for x in keyString.strip('{}').split(',')]
            if tmpIDs and len(tmpIDs) > 0:
                ids.extend(tmpIDs)
        else:
            ids.append(keyString)
        items = []
        for index in range(comboBox.count()):
            item = comboBox.itemData(index)
            if item.id in ids:
                items.append(item)

        if len(items) == 0:
            return
        
        if isinstance(comboBox, QgsCheckableComboBox):
            self.setCheckedItems(comboBox, items)
        else:
            self.setSelectedItem(comboBox, items[0])