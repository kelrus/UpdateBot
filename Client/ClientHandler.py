import BotHandler
from aiogram import Dispatcher, types
from Client import ClientKeyBoard
from Server import ServerHandler

_addChatActivate = False
_sendMessageActivate = False

async def CommandMenu(message: types.Message):
    await message.answer('/addchat - открывает клавиатуру для добавления чатов \n/sendmessage - отправить сообщения в чаты', reply_markup=ClientKeyBoard.keyBoardMenu)

async def CommandInfoChats(message: types.Message):
    await message.answer(str(ServerHandler.GetChats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('/addchat - добавить чат в список чатов \n/infochats - инфорсация о чатах'
                         , reply_markup=ClientKeyBoard.keyBoardChats)

async def CommandAddChatInput(message: types.Message):
    global _addChatActivate
    _addChatActivate = True
    await message.answer('введите id чата', reply_markup=ClientKeyBoard.keyBoardChats)
    @BotHandler.Dp.message_handler()
    async def CommandAddChat(message: types.Message):
        global _addChatActivate
        if _addChatActivate == True:
            ServerHandler.AddChats(str(message.text))
            _addChatActivate = False

async def CommandSendMessage(message: types.Message):
    global _sendMessageActivate
    _sendMessageActivate = True
    await message.answer('Напишите сообщение')
    @BotHandler.Dp.message_handler()
    async def CommandSendMessage(message: types.Message):
        global _sendMessageActivate
        _chats=ServerHandler.GetChats()
        if _sendMessageActivate == True:
            for chatid in ServerHandler.GetChats():
                # this send all
            _sendMessageActivate = False


def register_handler_client(dp : Dispatcher):
    BotHandler.Dp.register_message_handler(CommandMenu, commands=['start', 'help', 'menu'])
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchat'])
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.Dp.register_message_handler(CommandSendMessage, commands=['sendmessage'])






