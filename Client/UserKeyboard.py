import BotHandler
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server import ChatsHandler
from Server import DataBase

class FSMStorageUserBot(StatesGroup):
    replyTextUserId = State()
    replyTextUserName = State()
    replyTextUserRights = State()



async def CommandAddUserBot(message: types.Message):
    if ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageUserBot.replyTextUserId.set()
        await message.answer('Веедите id пользователя')
    else:
        await message.answer('У вас нет прав доступа для добавления пользователей')

async def CommandReplyIdFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserId'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Веедите имя пользователя')

async def CommandReplyNameFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserName'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Выберите права пользователя')

async def CommandReplyGroupFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserRights'] = str(message.text)
    ChatsHandler.AddUser(data['replyTextUserId'], data['replyTextUserName'], data['replyTextUserRights'])
    await DataBase.SqlAddUser(state)
    await state.finish()
    await message.answer('Пользователь успешно зарегистрирован')





def register_handler_users():
    BotHandler.Dp.register_message_handler(CommandAddUserBot, commands=['adduser'], state = None)
    BotHandler.Dp.register_message_handler(CommandReplyIdFSM, state=FSMStorageUserBot.replyTextUserId)
    BotHandler.Dp.register_message_handler(CommandReplyNameFSM, state=FSMStorageUserBot.replyTextUserName)
    BotHandler.Dp.register_message_handler(CommandReplyGroupFSM, state=FSMStorageUserBot.replyTextUserRights)

