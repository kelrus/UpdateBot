#Данный файл отвечает за управление пользователями на фронте с помощью команд.

import BotInit
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from BackBot import BackHandler




#Инициализация хранилища сообщений, в котором хранятся ответы пользователя.

class FSMStorageUserBot(StatesGroup):
    replyTextUserId = State()
    replyTextUserName = State()
    replyTextUserRights = State()
    replyTextUserDelete = State()


#Блок добавления нового пользователя на боте. Просит указать имя id и права пользователя,
#после чего отправляет эти данные в Бэк

async def CommandAddUserBot(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageUserBot.replyTextUserId.set()
        await message.answer('Веедите id пользователя')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandReplyIdFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserId'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Веедите имя пользователя')

async def __CommandReplyNameFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserName'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Выберите права пользователя')

async def __CommandReplyRightsFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserRights'] = str(message.text)
    await BackHandler.AddUser(state)
    await state.finish()
    await message.answer('Пользователь успешно зарегистрирован')


#Блок запрашивает информацию о доступных пользователях в Бэке, после чего выводит её

async def CommandInfoUsers(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(BackHandler.GetUsersInfo()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок отвечает за удаление пользователя. Просит ввести его id  и отправляет в Бэк для обработки и удаления.

async def CommandDeleteUserInput(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageUserBot.replyTextUserDelete.set()
        await message.answer('введите id пользователя')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandDeleteUser(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserDelete'] = message.text
    async with state.proxy() as data:
        await BackHandler.DeleteUser(str(data['replyTextUserDelete']))
    await state.finish()




#Регистрация комманд на боте

def register_handler_users():
    BotInit.Dp.register_message_handler(CommandAddUserBot, commands=['adduser'], state = None)
    BotInit.Dp.register_message_handler(__CommandReplyIdFSM, state=FSMStorageUserBot.replyTextUserId)
    BotInit.Dp.register_message_handler(__CommandReplyNameFSM, state=FSMStorageUserBot.replyTextUserName)
    BotInit.Dp.register_message_handler(__CommandReplyRightsFSM, state=FSMStorageUserBot.replyTextUserRights)
    BotInit.Dp.register_message_handler(CommandInfoUsers, commands=['infousers'], state=None)
    BotInit.Dp.register_message_handler(CommandDeleteUserInput, commands=['deleteuser'], state=None)
    BotInit.Dp.register_message_handler(__CommandDeleteUser, state=FSMStorageUserBot.replyTextUserDelete)
