from Server import DataBase

def GetUsers():
    return DataBase.SqlGetUsers()

def GetChats():
    return DataBase.SqlGetChats()

def AddChats(IdChat : str):
    DataBase.SqlAddChats(IdChat)

def CheckUserRightsIsBotAccess(idUser: str):
    print(DataBase.SqlSearchRightsById(idUser))
    if DataBase.SqlSearchRightsById(idUser) != []:
        return True
    return False
