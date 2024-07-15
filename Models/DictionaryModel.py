class DictionaryModel():
    def __init__(self):
        self.id = "",
        self.name = "",
        self.value = "",
        self.parentDictionaryName = "",
        self.parenElementName = ""

    def __init__(self, id, name, value):#, parentDictionaryName, parenElementName):
        self.id = id
        self.name = name
        self.value = value
        self.parentDictionaryName = "" # parentDictionaryName
        self.parenElementName = "" # parenElementName