from Server import DataBase

async def GetUsers():
    return DataBase.SqlGetUsers()

async def GetChats():
    return DataBase.SqlGetChats()

async def AddChats(IdChat : str):
    await DataBase.SqlAddChats(IdChat)

async def AddUser(state):
    await DataBase.SqlAddUser(state)

async def CheckUserRightsIsBotAccess(idUser: str):
    if DataBase.SqlSearchRightsById(idUser) != []:
        return True
    return False
