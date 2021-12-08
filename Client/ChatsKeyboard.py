import BotHandler
from aiogram import types
from Server import ChatsHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageChatsBot(StatesGroup):
    replyInputAddChat = State()
    replyInputDeleteChat = State()




async def CommandAddChatInput(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageChatsBot.replyInputAddChat.set()
        await message.answer('введите id чата')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyInputAddChat'] = message.text
    async with state.proxy() as data:
        ChatsHandler.AddChats(str(data['replyInputAddChat']))
    await state.finish()



async def CommandDeleteChatInput(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageChatsBot.replyInputDeleteChat.set()
        await message.answer('введите id чата')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandDeleteChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyInputDeleteChat'] = message.text
    async with state.proxy() as data:
        ChatsHandler.DeleteChats(str(data['replyInputDeleteChat']))
    await state.finish()



async def CommandInfoChats(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(ChatsHandler.GetChats()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')




def register_handler_chats():
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['addchat'], state = None)
    BotHandler.Dp.register_message_handler(CommandAddChat, state=FSMStorageChatsBot.replyInputAddChat)
    BotHandler.Dp.register_message_handler(CommandDeleteChatInput, commands=['deletechat'], state=None)
    BotHandler.Dp.register_message_handler(CommandDeleteChat, state=FSMStorageChatsBot.replyInputDeleteChat)
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])