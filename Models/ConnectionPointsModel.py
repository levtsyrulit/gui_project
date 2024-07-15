from .ModelBase import ModelBase

class ConnectionPointsModel(ModelBase):
    def __init__(self):
        # Инициализируем родительский класс
        super().__init__()

        self.id = ""
        self.denomination = ""
        self.type_ = ""
        self.dataSource = ""
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
        feature.setAttribute("Type", self.type_)
        feature.setAttribute("DataSource", self.dataSource)
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
        self.type_ = feature["Type"] or ""
        self.dataSource = feature["DataSource"] or ""
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

        if self.type_ is None or self.type_ == "":
            errors.append("Не указан вид объекта")

        return errors

