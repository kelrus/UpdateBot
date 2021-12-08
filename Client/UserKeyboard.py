import BotHandler
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from Server import ChatsHandler

class FSMStorageUserBot(StatesGroup):
    replyTextUserId = State()
    replyTextUserName = State()
    replyTextUserRights = State()
    replyTextUserDelete = State()



async def CommandAddUserBot(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageUserBot.replyTextUserId.set()
        await message.answer('Веедите id пользователя')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

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
    await ChatsHandler.AddUser(state)
    await state.finish()
    await message.answer('Пользователь успешно зарегистрирован')



async def CommandInfoUsers(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(ChatsHandler.GetUsersInfo()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')



async def CommandDeleteUserInput(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageUserBot.replyTextUserDelete.set()
        await message.answer('введите id пользователя')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandDeleteUser(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserDelete'] = message.text
    async with state.proxy() as data:
        await ChatsHandler.DeleteUser(str(data['replyTextUserDelete']))
    await state.finish()





def register_handler_users():
    BotHandler.Dp.register_message_handler(CommandAddUserBot, commands=['adduser'], state = None)
    BotHandler.Dp.register_message_handler(CommandReplyIdFSM, state=FSMStorageUserBot.replyTextUserId)
    BotHandler.Dp.register_message_handler(CommandReplyNameFSM, state=FSMStorageUserBot.replyTextUserName)
    BotHandler.Dp.register_message_handler(CommandReplyGroupFSM, state=FSMStorageUserBot.replyTextUserRights)
    BotHandler.Dp.register_message_handler(CommandInfoUsers, commands=['infousers'], state=None)
    BotHandler.Dp.register_message_handler(CommandDeleteUserInput, commands=['deleteuser'], state=None)
    BotHandler.Dp.register_message_handler(CommandDeleteUser, state=FSMStorageUserBot.replyTextUserDelete)
