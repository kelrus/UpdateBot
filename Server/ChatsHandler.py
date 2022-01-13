from Server import DataBase

def GetUsers():
    return DataBase.SqlGetUsers()

def GetUsersInfo():
    return DataBase.SqlGetUsersInfo()

def GetChats():
    return DataBase.SqlGetChats()

def AddChats(idChat : str):
    DataBase.SqlAddChats(idChat)

def DeleteChats(dChat : str):
    DataBase.SqlDeleteChats(dChat)

def AddMessage(message : str, time: str):
    DataBase.SqlAddMessage(message, time)

def DeleteMessage(time : str):
    DataBase.SqlDeleteMessage(time)

def GetMessage():
    return DataBase.SqlGetMessage()

async def AddUser(state):
    await DataBase.SqlAddUser(state)

async def DeleteUser(IdChat : str):
    await DataBase.SqlDeleteUser(IdChat)

async def CheckUserRightsIsBotAccess(idUser: str):
    if DataBase.SqlSearchRightsById(idUser) != []:
        return True
    return False
