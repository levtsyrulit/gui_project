from ..Services.AdministrationServerService import AdministrationServerService

class ModelBase():
    def __init__(self):
        pass

    def validate(self):
        errors: list[str] = []
        return errors

    def _getUserNameByLogin(self, login):
        if not login:
            return ""
        
        service = AdministrationServerService()
        name = service.getUserNameBylogin(login)
        if name:
            return "{0} ({1})".format(name, login)
        
        return ""