import BotHandler
from aiogram import types
from Server import ChatsHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageChatsBot(StatesGroup):
    replyInputChat = State()





async def CommandAddChatInput(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageChatsBot.replyInputChat.set()
        await message.answer('введите id чата')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyInputChat'] = message.text
    async with state.proxy() as data:
        ChatsHandler.AddChats(str(data['replyInputChat']))
    await state.finish()



async def CommandInfoChats(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(ChatsHandler.GetChats()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')




def register_handler_chats():
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['addchat'], state = None)
    BotHandler.Dp.register_message_handler(CommandAddChat, state=FSMStorageChatsBot.replyInputChat)
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])