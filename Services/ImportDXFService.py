from qgis.core import QgsFeature, QgsGeometry
from .DictionaryService import DictionariesService
from osgeo import ogr

class ImportDXFService():

    """Создание элемента слоя"""
    def createFeature(self, layer, dxfFeature):
        geom = self.__getGeometry(dxfFeature['geometry'])
        feature = QgsFeature(layer.fields())
        feature.setGeometry(geom)
        self.__setAttributes(feature, dxfFeature['attributes'])
        return feature

    def __getGeometry(self, geoJsonString):
        orgGeom = ogr.CreateGeometryFromJson(geoJsonString)
        return QgsGeometry.fromWkt(orgGeom.ExportToWkt())

    def __setAttributes(self, feature, attributes):
        if (attributes is None) or (len(attributes) == 0):
            return
        for attribute in attributes:
            attributeValue = self.__getDictionaryFieldValue(attribute, attributes[attribute])
            if attributeValue is None:
                feature.setAttribute(attribute, self.__getValue(attributes[attribute]))
            else:
                feature.setAttribute(attribute, attributeValue)

    def __getDictionaryFieldValue(self, attributeName, attributeValue):
        dictionaryName = attributeValue.split('.', 1)[0]
        dictionary = DictionariesService().getDictionaryByName(dictionaryName)
        if (dictionary is None):
            return None
        elements = dictionary.getSpecificElements([x.strip() for x in attributeValue.split(',')])
        if len(elements) > 0:
            if attributeName in {'Arrangement', 'SewageType'}:
                return "{" + ",".join(['"' + x.id + '"' for x in elements]) + "}"
            else:
                return str(elements[0].id)
        else:
            return ""

    def __getValue(self, attributeValue):
        return attributeValue == 'True' if attributeValue in { 'True', 'False'} else attributeValue


