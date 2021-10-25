import BotHandler
from aiogram import types
from Client import ClientKeyBoard
from Server import ServerHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMStorageBot(StatesGroup):
    replyTextChat = State()
    replyTextSend = State()

async def CommandMenu(message: types.Message):
    await message.answer('/addchat - открывает клавиатуру для добавления чатов \n/sendmessage - отправить сообщения в чаты', reply_markup=ClientKeyBoard.keyBoardMenu)

async def CommandInfoChats(message: types.Message):
    await message.answer(str(ServerHandler.GetChats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('/addchat - добавить чат в список чатов \n/infochats - инфорсация о чатах'
                         , reply_markup=ClientKeyBoard.keyBoardChats)

async def CommandAddChatInput(message: types.Message):
    await FSMStorageBot.replyTextChat.set()
    await message.answer('введите id чата')

async def CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextChat'] = message.text
    async with state.proxy() as data:
        ServerHandler.AddChats(str(data['replyTextChat']))
    await state.finish()

async def CommandSendMessage(message: types.Message):
    await FSMStorageBot.replyTextSend.set()
    await message.answer('Напишите сообщение')

async def CommandSendMessageAll(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
    async with state.proxy() as data:
        for chatid in ServerHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextSend'])
    await state.finish()

def register_handler_client():
    BotHandler.Dp.register_message_handler(CommandMenu, commands=['start', 'help', 'menu'])
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchat'])
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.Dp.register_message_handler(CommandSendMessage, commands=['sendmessage'])
    BotHandler.Dp.register_message_handler(CommandAddChat, state=FSMStorageBot.replyTextChat)
    BotHandler.Dp.register_message_handler(CommandSendMessageAll, state=FSMStorageBot.replyTextSend)






