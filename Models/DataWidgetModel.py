class DataWidgetModel():
    def __init__(self):
        self.sourceName = ""
        self.groupID = 0
        self.groupName = ""
        self.layerName = ""
        self.count = 0
        self.layerFeatureDictionary = {}

    def __init__(self, sourceName, groupID, groupName, layerName, count, layerFeatureDictionary):
        self.sourceName = sourceName
        self.groupID = groupID
        self.groupName = groupName
        self.layerName = layerName
        self.count = count
        self.layerFeatureDictionary = layerFeatureDictionary