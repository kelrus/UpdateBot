#Данный файл отвечает за управление чатами пользователем на фронте с помощью команд.

import BotHandler
from aiogram import types
from BackBot import BackHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup





#Инициализация хранилища сообщений, в котором хранятся ответы пользователя.

class FSMStorageChatsBot(StatesGroup):
    replyInputAddChat = State()
    replyInputDeleteChat = State()


#Блок отвечает за добавление нового id чата. При вводе пользователем команды добавления чата,
#бот просит его написать id добавляемого чата, затем он передаёт id в Бэк

async def CommandAddChatInput(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageChatsBot.replyInputAddChat.set()
        await message.answer('введите id чата')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyInputAddChat'] = message.text
    async with state.proxy() as data:
        BackHandler.AddChats(str(data['replyInputAddChat']))
    await state.finish()


#Блок отвечает за удаление чата. При вводе пользователем команды удаления чата,
#бот просит его написать id удаляемого чата, затем он передаёт id в Бэк

async def CommandDeleteChatInput(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageChatsBot.replyInputDeleteChat.set()
        await message.answer('введите id чата')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandDeleteChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyInputDeleteChat'] = message.text
    async with state.proxy() as data:
        BackHandler.DeleteChats(str(data['replyInputDeleteChat']))
    await state.finish()


#Блок отвечает за вывод хранящихся в боте чатах. После вводе команды пользователем,
#бот посылает запрос в Бек для получения информации о чатах.
#После получения информации он пишет её пользователю.


async def CommandInfoChats(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(BackHandler.GetIdChats()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')




#Регистрация комманд для соответствующих функций управления чатами на боте.

def register_handler_chats():
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['addchat'], state = None)
    BotHandler.Dp.register_message_handler(__CommandAddChat, state=FSMStorageChatsBot.replyInputAddChat)
    BotHandler.Dp.register_message_handler(CommandDeleteChatInput, commands=['deletechat'], state=None)
    BotHandler.Dp.register_message_handler(__CommandDeleteChat, state=FSMStorageChatsBot.replyInputDeleteChat)
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])