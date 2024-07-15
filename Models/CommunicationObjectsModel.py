from .ModelBase import ModelBase

class CommunicationObjectsModel(ModelBase):
    def __init__(self):
        # Инициализируем родительский класс
        super().__init__()
        
        self.id = ""
        self.denomination = ""
        self.state = ""
        self.type_ = ""
        self.arrangement = ""
        self.location = ""
        self.cadastralNumber = ""
        self.additionalStructures = ""
        self.dataSource = ""

        #Additional
        self.communicationLineType = ""
        self.actualUseOfTheObject = 0.0
        self.capacity = 0
        self.power = 0.0
        self.powerUnit = ""
        self.dataTransferSpeed = 0.0
        self.buildingRestructionZoneDistance = 0.0
        self.buildingRestructionZoneHeight = 0.0
        self.wear = 0.0
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
        feature.setAttribute("Arrangement", self.arrangement)
        feature.setAttribute("Location", self.location)
        feature.setAttribute("CadastralNumber", self.cadastralNumber)
        feature.setAttribute("AdditionalStructures", self.additionalStructures)
        feature.setAttribute("DataSource", self.dataSource)

        # Additional
        feature.setAttribute("CommunicationLineType", self.communicationLineType)
        feature.setAttribute("ActualObjectUsage", self.actualUseOfTheObject)
        feature.setAttribute("Capacity", self.capacity)
        feature.setAttribute("Power", self.power)
        feature.setAttribute("PowerUnit", self.powerUnit)
        feature.setAttribute("DataTransferSpeed", self.dataTransferSpeed)
        feature.setAttribute("BuildingRestrictionsZoneDistance", self.buildingRestructionZoneDistance)
        feature.setAttribute("BuildingRestrictionsZoneHeight", self.buildingRestructionZoneHeight)
        feature.setAttribute("Wear", self.wear)
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
        self.arrangement = feature["Arrangement"] or ""
        self.location = feature["Location"] or ""
        self.cadastralNumber = feature["CadastralNumber"] or ""
        self.additionalStructures = feature["AdditionalStructures"] or ""
        self.dataSource = feature["DataSource"] or ""

        self.communicationLineType = feature["CommunicationLineType"] or ""
        self.actualUseOfTheObject = feature["ActualObjectUsage"] or 0.0
        self.capacity = feature["Capacity"] or 0
        self.power = feature["Power"] or 0.0
        self.powerUnit = feature["PowerUnit"] or ""
        self.dataTransferSpeed = feature["DataTransferSpeed"]
        self.buildingRestructionZoneDistance = feature["BuildingRestrictionsZoneDistance"] or 0.0
        self.buildingRestructionZoneHeight = feature["BuildingRestrictionsZoneHeight"] or 0.0
        self.wear = feature["Wear"] or 0.0
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

