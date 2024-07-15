from .ModelBase import ModelBase

class WaterSupplyNetworksModel(ModelBase):
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
        self.dataSource = ""

        # Additional
        self.length = 0.0
        self.diameter = 0.0
        self.pipelineOuterDiameter = 0.0
        self.occurrenceDepth = 0.0
        self.material = ""
        self.wear = 0.0
        self.number = 0
        self.hatchwayRingMark = 0.0
        self.pipeTopMark = 0.0
        self.pipeBottomMark = 0.0
        self.groundMark = 0.0
        self.crosswalkHeight = 0.0 #sbCrosswalkHeight
        self.gasketNumber = 0
        self.hatchwayState = ""
        self.isWaterSupplyZone = False
        self.constructions = ""
        self.undergroundLaying = ""
        self.materialCT4 = ""
        self.thermalInsulation = ""
        self.sleeveType = ""
        self.sleeveMaterial = ""
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
        # Параметр ID не заполнять!

        feature.setAttribute("Denomination", self.denomination)
        feature.setAttribute("State", self.state)
        feature.setAttribute("Type", self.type_)
        feature.setAttribute("Arrangement", self.arrangement)
        feature.setAttribute("Location", self.location)
        feature.setAttribute("CadastralNumber", self.cadastralNumber)
        feature.setAttribute("DataSource", self.dataSource)

        # Additional
        feature.setAttribute("Length", self.length)
        feature.setAttribute("Diameter", self.diameter)
        feature.setAttribute("PipelineOuterDiameter",self.pipelineOuterDiameter)
        feature.setAttribute("OccurrenceDepth", self.occurrenceDepth)
        feature.setAttribute("Material", self.material)
        feature.setAttribute("Wear", self.wear)
        feature.setAttribute("PipesNumber", self.number)
        feature.setAttribute("HatchwayRingMark", self.hatchwayRingMark)
        feature.setAttribute("PipeTopMark",self.pipeTopMark)
        feature.setAttribute("PipeBottomMark", self.pipeBottomMark)
        feature.setAttribute("GroundMark", self.groundMark)
        feature.setAttribute("CrosswalkHeight", self.crosswalkHeight) #???
        feature.setAttribute("GasketNumber", self.gasketNumber)
        feature.setAttribute("IsWaterSupplyZone", self.isWaterSupplyZone)
        feature.setAttribute("HatchwayState", self.hatchwayState)
        feature.setAttribute("Constructions", self.constructions)
        feature.setAttribute("UndergroundLaying", self.undergroundLaying)
        feature.setAttribute("MaterialCT4", self.materialCT4)
        feature.setAttribute("ThermalInsulation", self.thermalInsulation)
        feature.setAttribute("SleeveType", self.sleeveType)
        feature.setAttribute("SleeveMaterial", self.sleeveMaterial)
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
        self.dataSource = feature["DataSource"] or ""

        self.length = feature["Length"] or 0.0
        self.diameter = feature["Diameter"] or 0.0
        self.pipelineOuterDiameter = feature["PipelineOuterDiameter"] or 0.0
        self.occurrenceDepth = feature["OccurrenceDepth"] or 0.0  #
        self.material = feature["Material"] or ""
        self.wear = feature["Wear"] or 0.0
        self.number = feature["PipesNumber"] or 0
        self.hatchwayRingMark = feature["HatchwayRingMark"] or 0.0
        self.pipeTopMark = feature["PipeTopMark"] or 0.0
        self.pipeBottomMark = feature["PipeBottomMark"] or 0.0
        self.groundMark = feature["GroundMark"] or 0.0
        self.crosswalkHeight = feature["CrosswalkHeight"] or 0.0
        self.gasketNumber = feature["GasketNumber"] or 0
        self.isWaterSupplyZone = feature["IsWaterSupplyZone"] or False
        self.hatchwayState = feature["HatchwayState"] or ""
        self.constructions = feature["Constructions"] or ""
        self.undergroundLaying = feature["UndergroundLaying"] or ""
        self.materialCT4 = feature["MaterialCT4"] or ""
        self.thermalInsulation = feature["ThermalInsulation"] or ""
        self.sleeveType = feature["SleeveType"] or ""
        self.sleeveMaterial = feature["SleeveMaterial"] or ""
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




