import BotHandler
from aiogram import Dispatcher, types
from Client import ClientKeyBoard
from Server import ServerHandler

AddChatActivate = False

async def commandStart(message: types.Message):
    await message.answer('Бот Запущен', reply_markup=ClientKeyBoard.KeyBoardMenu)

async def command_infochats(message: types.Message):
    await message.answer(str(ServerHandler.getchats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('Нажмите на кнопку "/inputchat" и напишите id чата, который хотите добавить', reply_markup=ClientKeyBoard.KeyBoardChats)

async def CommandAddChatInput(message: types.Message):
    global AddChatActivate
    AddChatActivate = True
    await message.answer('введите id чата', reply_markup=ClientKeyBoard.KeyBoardChats)
    @BotHandler.dp.message_handler()
    async def CommandAddChat(message: types.Message):
        global AddChatActivate
        if AddChatActivate == True:
            ServerHandler.addChats(str(message.text))
            AddChatActivate = False

async def CommandAddChatStop(message: types.Message):
    await message.answer('Добавление чатов прервано')
    global AddChatActivate
    AddChatActivate = False


def register_handler_client(dp : Dispatcher):
    BotHandler.dp.register_message_handler(commandStart, commands=['start', 'help'])
    BotHandler.dp.register_message_handler(command_infochats, commands=['infochats'])
    BotHandler.dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchats'])
    BotHandler.dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.dp.register_message_handler(CommandAddChatStop, commands=['stopaddchat'])






