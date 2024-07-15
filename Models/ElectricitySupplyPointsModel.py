from .ModelBase import ModelBase

class ElectricitySupplyPointsModel(ModelBase):
    def __init__(self):
        # Инициализируем родительский класс
        super().__init__()

        # Main
        self.id_ = ""
        self.denomination = ""
        self.state = ""
        self.type_ = ""
        self.arrangement = ""
        self.location = ""
        self.cadastralNumber = ""
        self.additionalStructures = ""
        self.dataSource = ""
        self.rotation = 0

        # Additional
        self.power = 0.0
        self.numberOfTransformers = 0
        self.actualUse = 0.0
        self.mainTypeOfFuel = ""
        self.electricPower = 0.0
        self.thermalPower = 0.0
        self.wear = 0.0
        self.voltage = 0.0
        self.sanitaryProtectionZoneSize = 0.0
        self.guardZoneSize = 0.0
        self.note = ""

        # Passport
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

        feature.setAttribute("Denomination", self.denomination)
        feature.setAttribute("State", self.state)
        feature.setAttribute("Type", self.type_)
        feature.setAttribute("Arrangement", self.arrangement)
        feature.setAttribute("Location", self.location)
        feature.setAttribute("CadastralNumber", self.cadastralNumber)
        feature.setAttribute("AdditionalStructures", self.additionalStructures)
        feature.setAttribute("DataSource", self.dataSource)
        feature.setAttribute("Rotation", self.rotation)

        feature.setAttribute("Power", self.power)
        feature.setAttribute("TransformersNumber", self.numberOfTransformers)
        feature.setAttribute("ActualObjectUsage", self.actualUse )
        feature.setAttribute("MainFuelType", self.mainTypeOfFuel)
        feature.setAttribute("ElectricPower", self.electricPower)
        feature.setAttribute("ThermalPower", self.thermalPower)
        feature.setAttribute("Wear", self.wear)
        feature.setAttribute("Voltage", self.voltage)
        feature.setAttribute("SanitaryProtectionZoneSize", self.sanitaryProtectionZoneSize)
        feature.setAttribute("GuardZoneSize", self.guardZoneSize)
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
        self.rotation = feature["Rotation"] or 0

        self.power = feature["Wear"] or 0.0
        self.numberOfTransformers = feature["TransformersNumber"] or 0
        self.actualUse = feature["ActualObjectUsage"] or 0.0
        self.mainTypeOfFuel = feature["MainFuelType"] or ""
        self.electricPower = feature["ElectricPower"] or 0.0
        self.thermalPower = feature["ThermalPower"] or 0.0
        self.wear = feature["Wear"] or 0.0
        self.voltage = feature["Voltage"] or 0.0
        self.sanitaryProtectionZoneSize = feature["SanitaryProtectionZoneSize"] or 0.0
        self.guardZoneSize = feature["GuardZoneSize"] or 0.0
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

        if self.denomination is None or self.denomination == "":
            errors.append("Не указано наименование объекта")

        if self.state is None or self.state == "":
            errors.append("Не указано состояние объекта")

        if self.type_ is None or self.type_ == "":
            errors.append("Не указан вид объекта")


        return errors