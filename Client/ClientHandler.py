import BotHandler
from aiogram import Dispatcher, types
from Client import ClientKeyBoard
from Server import ServerHandler

_addChatActivate = False

async def CommandStart(message: types.Message):
    await message.answer('Бот Запущен', reply_markup=ClientKeyBoard.keyBoardMenu)

async def CommandInfoChats(message: types.Message):
    await message.answer(str(ServerHandler.GetChats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('Нажмите на кнопку "/inputchat" и напишите id чата, который хотите добавить', reply_markup=ClientKeyBoard.keyBoardChats)

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

async def CommandAddChatStop(message: types.Message):
    await message.answer('Добавление чатов прервано')
    global _addChatActivate
    _addChatActivate = False


def register_handler_client(dp : Dispatcher):
    BotHandler.Dp.register_message_handler(CommandStart, commands=['start', 'help'])
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchats'])
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.Dp.register_message_handler(CommandAddChatStop, commands=['stopaddchat'])






