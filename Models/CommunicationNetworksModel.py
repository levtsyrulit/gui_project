from .ModelBase import ModelBase
class CommunicationNetworksModel(ModelBase):
    def __init__(self):
        # Инициализируем родительский класс
        super().__init__()
        
        self.denomination = ""
        self.state = ""
        self.type_ = ""
        self.communicationNetworkStructureType = ""
        self.location = ""
        self.cadastralNumber = ""
        self.dataSource = ""

        #Additional
        self.length = 0.0
        self.communicationLinesType = ""
        self.wear = 0.0
        self.guardZoneSize = 0.0
        self.wiresNumber = 0
        self.constructions = ""
        self.undergroundLaying = ""
        self.communicationNetworkType = ""
        self.note = ""

        #Passport
        self.balanceholder = ""
        self.property_type = ""
        self.operating_organisation = ""
        self.role_of_object = ""
        self.comissioning_year = None
        self.reconstruction_year = None
        self.creation_date = None
        self.update_date = None
        self.creator = ""
        self.editor = ""
        self.comment = ""

        #import
        self.attachedFilesID = ""
        self.attachedFilesCount = ""
        self.dxfFileName = ""

    """Заполнение атрибутов объекта слоя значениями из модели"""
    def fillFeatureFromModel(self, feature):
        # Параметр ID не заполнять!

        feature.setAttribute("Denomination", self.denomination)
        feature.setAttribute("State", self.state)
        feature.setAttribute("Type", self.type_)
        feature.setAttribute("CommunicationNetworkStructureType", self.communicationNetworkStructureType)
        feature.setAttribute("Location", self.location)
        feature.setAttribute("CadastralNumber", self.cadastralNumber)
        feature.setAttribute("DataSource", self.dataSource)

        # Additional
        feature.setAttribute("Length", self.length)
        feature.setAttribute("CommunicationLinesType", self.communicationLinesType)
        feature.setAttribute("GuardZoneSize", self.guardZoneSize)
        feature.setAttribute("Wear", self.wear)
        feature.setAttribute("WiresNumber", self.wiresNumber)
        feature.setAttribute("Constructions", self.constructions)
        feature.setAttribute("UndergroundLaying", self.undergroundLaying)
        feature.setAttribute("CommunicationNetworkType", self.communicationNetworkType)
        feature.setAttribute("Note", self.note)

        feature.setAttribute("BalanceHolder", self.balanceholder)
        feature.setAttribute("PropertyType", self.property_type)
        feature.setAttribute("OperatingOrganisation", self.operating_organisation)
        feature.setAttribute("ObjectRole", self.role_of_object)
        feature.setAttribute("ComissioningYear", self.comissioning_year)
        feature.setAttribute("ReconstructionYear", self.reconstruction_year)        
        feature.setAttribute("Comment", self.comment)

        #import
        feature.setAttribute("AttachedFilesID", self.attachedFilesID)
        feature.setAttribute("AttachedFilesCount", self.attachedFilesCount)        
        feature.setAttribute("DxfFileName", self.dxfFileName)

    """Заполнение модели из атрибутов объекта слоя"""
    def fillModelFromFeature(self, feature):
        self.denomination = feature["Denomination"] or ""
        self.state = feature["State"] or ""
        self.type_ = feature["Type"] or ""
        self.communicationNetworkStructureType = feature["CommunicationNetworkStructureType"] or ""
        self.location = feature["Location"] or ""
        self.cadastralNumber = feature["CadastralNumber"] or ""
        self.dataSource = feature["DataSource"] or ""

        self.length = feature["Length"] or 0.0
        self.communicationLinesType = feature["CommunicationLinesType"] or ""
        self.wear = feature["Wear"] or 0.0
        self.guardZoneSize = feature["GuardZoneSize"] or 0.0
        self.wiresNumber = feature["WiresNumber"] or 0
        self.constructions = feature["Constructions"] or ""
        self.undergroundLaying = feature["UndergroundLaying"] or ""
        self.communicationNetworkType = feature["CommunicationNetworkType"] or ""
        self.note = feature["Note"] or ""

        self.balanceholder = feature["BalanceHolder"] or ""
        self.property_type = feature["PropertyType"] or ""
        self.operating_organisation = feature["OperatingOrganisation"] or ""
        self.role_of_object = feature["ObjectRole"] or ""
        self.comissioning_year = feature["ComissioningYear"]
        self.reconstruction_year = feature["ReconstructionYear"]
        self.creation_date = feature["CreationDate"]
        self.update_date = feature["UpdateDate"]
        self.creator = self._getUserNameByLogin(feature["Creator"])
        self.editor = self._getUserNameByLogin(feature["Editor"])
        self.comment = feature["Comment"] or ""

        #import
        self.attachedFilesID = feature["AttachedFilesID"] or ""
        self.attachedFilesCount = feature["AttachedFilesCount"] or ""
        self.dxfFileName = feature["DxfFileName"] or ""

    def validate(self):
        errors: list[str] = []

        if self.state is None or self.state == "":
            errors.append("Не указано состояние объекта")

        if self.type_ is None or self.type_ == "":
            errors.append("Не указан вид объекта")

        return errors

