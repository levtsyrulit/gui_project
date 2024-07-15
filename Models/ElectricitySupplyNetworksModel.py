from .ModelBase import ModelBase

class ElectricitySupplyNetworksModel(ModelBase):
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
        self.voltage = ""
        self.cadastralNumber = ""
        self.additionalDevice = ""
        self.dataSource = ""

        # Additional
        self.length = 0.0
        self.wear = 0.0
        self.sanitaryProtectionZoneSize = 0.0
        self.guardZoneSize = 0.0
        self.numberCablesInBundle = 0
        self.wiresNumber = 0
        self.constructions = ""
        self.sleeveType = ""
        self.sleeveMaterial = ""
        self.formFactor = ""
        self.stowageType = ""
        self.cableMark = ""
        self.cableSegments = ""
        self.cableZone = ""
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
        feature.setAttribute("Voltage", self.voltage)
        feature.setAttribute("CadastralNumber", self.cadastralNumber)
        feature.setAttribute("AdditionalDevice", self.additionalDevice)
        feature.setAttribute("DataSource", self.dataSource)

        feature.setAttribute("Length", self.length)
        feature.setAttribute("Wear", self.wear)
        feature.setAttribute("SanitaryProtectionZoneSize", self.sanitaryProtectionZoneSize)
        feature.setAttribute("GuardZoneSize", self.guardZoneSize)
        feature.setAttribute("NumberCablesInBundle", self.numberCablesInBundle)
        feature.setAttribute("WiresNumber", self.wiresNumber)
        feature.setAttribute("Constructions", self.constructions)
        feature.setAttribute("SleeveType", self.sleeveType)
        feature.setAttribute("SleeveMaterial", self.sleeveMaterial)
        feature.setAttribute("FormFactor", self.formFactor)
        feature.setAttribute("StowageType", self.stowageType)
        feature.setAttribute("CableMark", self.cableMark)
        feature.setAttribute("CableSegments", self.cableSegments)
        feature.setAttribute("CableZone", self.cableZone)
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
        self.voltage = feature["Voltage"] or ""
        self.cadastralNumber = feature["CadastralNumber"] or ""
        self.additionalDevice = feature["AdditionalDevice" or ""]
        self.dataSource = feature["DataSource"] or ""

        self.length = feature["Length"] or 0.0
        self.wear = feature["Wear"] or 0.0
        self.sanitaryProtectionZoneSize = feature["SanitaryProtectionZoneSize"] or 0.0
        self.guardZoneSize = feature["GuardZoneSize"] or 0.0
        self.numberCablesInBundle = feature["NumberCablesInBundle"] or 0
        self.wiresNumber = feature["WiresNumber"] or 0
        self.constructions = feature["Constructions"] or ""
        self.sleeveType = feature["SleeveType"] or ""
        self.sleeveMaterial = feature["SleeveMaterial"] or ""
        self.formFactor = feature["FormFactor"] or ""
        self.stowageType = feature["StowageType"] or ""
        self.cableMark = feature["CableMark"] or ""
        self.cableSegments = feature["CableSegments"] or ""
        self.cableZone = feature["CableZone"] or ""
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

        if self.voltage is None or self.voltage == "":
            errors.append("Не указано напряжение")

        return errors