class DataSourceObject:
    def __init__(self):
        self.sourceName = ""
        self.groupName = ""
        self.layerName = ""
        self.count = 0
        self.layerID = None
        self.featureIDs = []
        self.groupID = None

    def __init__(self, name, groupName, layerName, count, layerID, featureIDs, groupID):
        self.sourceName = name
        self.groupName = groupName
        self.layerName = layerName
        self.count = count
        self.layerID = layerID
        self.featureIDs = featureIDs
        self.groupID = groupID