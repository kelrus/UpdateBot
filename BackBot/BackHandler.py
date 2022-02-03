#Файл отвечает за взаимосвязь Фронта и Бэка
from BackBot import DataBase
from BackBot import UidHandler



#Блок по получению и изменению данных пользователя в БД

#Получает информацию о всех пользователей на боте из БД
def GetUsersInfo():
    return DataBase.SqlGetUsersInfo()

#Добавляет пользователя в БД с помощью данных из хранилища
async def AddUser(state):
    await DataBase.SqlAddUser(state)

#Удаляет пользователя из БД с помощью его id
async def DeleteUser(IdChat : str):
    await DataBase.SqlDeleteUser(IdChat)

#Проверяет есть ли у пользователя хоть какие-то права на боте
async def CheckUserRightsIsBotAccess(idUser: str):
    if DataBase.SqlSearchRightsById(idUser) != []:
        return True
    return False


#Блок по получению и изменению чатов в БД

#Получает список id всех чатов из БД
def GetIdChats():
    return DataBase.SqlGetIdChats()

#Добавляет чат в БД с помощью его id
def AddChats(idChat : str):
    DataBase.SqlAddChats(idChat)

#Удаляет чат из БД с помощью его id
def DeleteChats(idChat : str):
    DataBase.SqlDeleteChats(idChat)


#Блок для работы с сообщениями в БД

#Добавляет собщение в БД. Для хранения передаётся текст сообщения и его время отправления
def AddMessage(message : str, time: str, uid:str):
    DataBase.SqlAddMessage(message, time, uid)

#Удаляет сообщение из БД с помощью его времени отправления
def DeleteMessage(time : str):
    DataBase.SqlDeleteMessage(time)

#Получение информации о всех хранящихся сообщениях
def GetMessage():
    return DataBase.SqlGetMessage()


#Блок для работы с uid сообщения

def GetUidMessage(messageid, data, message):
    return UidHandler.GenerateMessageUid(messageid, data, message)

