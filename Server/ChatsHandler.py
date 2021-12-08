from Server import DataBase

def GetUsers():
    return DataBase.SqlGetUsers()

def GetUsersInfo():
    return DataBase.SqlGetUsersInfo()

def GetChats():
    return DataBase.SqlGetChats()

def AddChats(IdChat : str):
    DataBase.SqlAddChats(IdChat)

def DeleteChats(IdChat : str):
    DataBase.SqlDeleteChats(IdChat)

async def AddUser(state):
    await DataBase.SqlAddUser(state)

async def CheckUserRightsIsBotAccess(idUser: str):
    if DataBase.SqlSearchRightsById(idUser) != []:
        return True
    return False
