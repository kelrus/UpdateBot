#Файл отвечает за взаимосвязь Фронта и Бэка
from BackBot import DataBase
from BackBot import UidHandler
from BackBot import DataTimeHandler
from BackBot import CheckInput
from aiogram.utils.exceptions import BotKicked
import BotInit


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
def DeleteMessage(uid : str):
    DataBase.SqlDeleteMessage(uid)

#Получение информации о всех хранящихся сообщениях
def GetMessages():
    return DataBase.SqlGetMessages()


#Блок для работы с uid сообщения

def GetUidMessage(messageid, data, message):
    return UidHandler.GenerateMessageUid(messageid, data, message)


#Блок проверки на коректность ввода бота

#Проверка текста на добавление чата
def CheckTextAddChat(text):

    if(CheckInput.CheckInputChat(text) and not DataBase.CheckChatInDb(text)):
        return True
    return False

#Проверка текста на удаление чата
def CheckTextDeleteChat(text):

    if(CheckInput.CheckInputChat(text) and DataBase.CheckChatInDb(text)):
        return True
    return False



#Блок запуска работа серверной части приложения

#Это функция, которая регистрирует отложенные сообщения на прямую из базы данных при запуске бота
def GetStartedBack():
    DataBase.SqlStart()
    messagesInBase = GetMessages()
    print(len(messagesInBase))

    for message in messagesInBase:
        print(message)
        datetime = message[0]
        messageText = message[1]
        uid = message[2]

        if DataTimeHandler.IsCorrectDateTime(datetime):
            BotInit.Scheduler.add_job(__SendDelayedMessageAll, 'date', run_date=datetime, args=(messageText, uid,), id=uid)
        else:
            DeleteMessage(uid)

#Это событие, которое запускается в назначенных момент по дате и времени и отправляет сообщения в чаты.
async def __SendDelayedMessageAll(message: str, uid,):
        chatsId = GetIdChats()
        for chatId in chatsId:
            #Обработка исключения, которое возникает в том случаи, если бот не добавлен в чат, но пытается отправить туда сообщение
            try:
                await BotInit.Bot.send_message(int(chatId[0]), message)
            except BotKicked:
                print("Error sending message from database when starting bot. The bot has not been added to the chat.")
        DeleteMessage(uid)