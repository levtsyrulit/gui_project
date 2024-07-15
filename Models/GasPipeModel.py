from .ModelBase import ModelBase

class GasPipeModel(ModelBase):
    def __init__(self):
        # Инициализируем родительский класс
        super().__init__()

        #Main
        self.id_ = ""
        self.state = ""
        self.type_ = ""
        self.category = ""
        self.arrangement = ""
        self.length = 0.0
        self.cadastral_number = ""
        self.specialPurpose = ""
        self.data_source = ""
        
        #Additional
        self.denomination = ""
        self.location = ""
        self.operating_pressure = 0
        self.sanitary_protection_zone_size = 0.0
        self.guard_zone_size = 0.0
        self.diameter = 0.0
        self.diameter_outer = 0.0
        self.material = ""
        self.wear = 0.0
        self.number = 0
        self.height = 0.0
        self.depth = 0.0
        self.volume = 0.0
        self.area = 0.0
        self.area_built_up = 0.0
        self.constructions = ""
        self.undergroundLaying = ""
        self.materialCT4 = ""
        self.thermalInsulation = ""
        self.sleeveType = ""
        self.sleeveMaterial = ""
        self.gasType = ""
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

        feature.setAttribute("State", self.state)
        feature.setAttribute("Type", self.type_)
        feature.setAttribute("Category", self.category)
        feature.setAttribute("Arrangement", self.arrangement)
        feature.setAttribute("Length", self.length)
        feature.setAttribute("CadastralNumber", self.cadastral_number)
        feature.setAttribute("SpecialPurpose", self.specialPurpose)
        feature.setAttribute("DataSource", self.data_source)

        feature.setAttribute("Denomination", self.denomination)
        feature.setAttribute("Location", self.location)
        feature.setAttribute("OperatingPressure", self.operating_pressure)
        feature.setAttribute("SanitaryProtectionZoneSize", self.sanitary_protection_zone_size)
        feature.setAttribute("GuardZoneSize", self.guard_zone_size)
        feature.setAttribute("Diameter", self.diameter)
        feature.setAttribute("DiameterOuter", self.diameter_outer)
        feature.setAttribute("Material", self.material)
        feature.setAttribute("Wear", self.wear)
        feature.setAttribute("PipesNumber", self.number)
        feature.setAttribute("Height", self.height)
        feature.setAttribute("Depth", self.depth)
        feature.setAttribute("Volume", self.volume)
        feature.setAttribute("Area", self.area)
        feature.setAttribute("AreaBuiltUp", self.area_built_up)
        feature.setAttribute("Constructions", self.constructions)
        feature.setAttribute("UndergroundLaying", self.undergroundLaying)
        feature.setAttribute("MaterialCT4", self.materialCT4)
        feature.setAttribute("ThermalInsulation",self.thermalInsulation)
        feature.setAttribute("SleeveType",self.sleeveType)
        feature.setAttribute("SleeveMaterial", self.sleeveMaterial)
        feature.setAttribute("GasType", self.gasType)
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
        self.state = feature["State"] or ""
        self.type_ = feature["Type"] or ""
        self.category = feature["Category"] or ""
        self.arrangement  = feature["Arrangement"] or ""
        self.length = feature["Length"] or 0.0
        self.cadastral_number = feature["CadastralNumber"] or ""
        self.specialPurpose = feature["SpecialPurpose"] or ""
        self.data_source = feature["DataSource"] or ""

        # Additional
        self.denomination = feature["Denomination"] or ""
        self.location = feature["Location"] or ""
        self.operating_pressure = feature["OperatingPressure"] or 0.0
        self.sanitary_protection_zone_size = feature["SanitaryProtectionZoneSize"] or 0.0
        self.guard_zone_size = feature["GuardZoneSize"] or 0.0
        self.diameter = feature["Diameter"] or 0.0
        self.diameter_outer = feature["DiameterOuter"] or 0.0
        self.material = feature["Material"] or ""
        self.wear = feature["Wear"] or 0.0
        self.number = feature["PipesNumber"] or 0.0
        self.height = feature["Height"] or 0.0
        self.depth = feature["Depth"] or 0.0
        self.volume = feature["Volume"] or 0.0
        self.area = feature["Area"] or 0.0
        self.area_built_up = feature["AreaBuiltUp"] or 0.0
        self.constructions = feature["Constructions"] or ""
        self.undergroundLaying = feature["UndergroundLaying"] or ""
        self.materialCT4 = feature["MaterialCT4"] or ""
        self.thermalInsulation = feature["ThermalInsulation"] or ""
        self.sleeveType = feature["SleeveType"] or ""
        self.sleeveMaterial = feature["SleeveMaterial"] or ""
        self.gasType = feature["GasType"] or ""
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

        if self.category is None or self.category == "":
            errors.append("Не указана категория")

        if self.arrangement is None or self.arrangement == "":
            errors.append("Не указано расположение объекта")
        
        return errors





