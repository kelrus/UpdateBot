from aiogram import Dispatcher, types
from Client import ClientKeyBoard

import BotHandler
from Server import ServerHandler

async def command_start(message: types.Message):
    await BotHandler.bot.send_message(message.from_user.id, 'Бот Запущен', reply_markup = ClientKeyBoard.KeyBoardMenu)

async def command_infochats(message: types.Message):
    await message.answer(str(ServerHandler.getchats()))

async def command_addchat(message: types.Message):
    await message.answer('Напишите id чата')
    BotHandler.setAddChatActivate(True)

@BotHandler.dp.message_handler()
async def addchat(message: types.Message):
    if BotHandler.getAddChatActivate == True :
        message: types.Message
        ServerHandler.addChats(message.text)
        await message.answer('Чат добавлен!')
        BotHandler.setAddChatActivate(False)

def register_handler_client(dp : Dispatcher):
    BotHandler.dp.register_message_handler(command_start, commands=['start', 'help'])
    BotHandler.dp.register_message_handler(command_infochats, commands=['infochats'])
    BotHandler.dp.register_message_handler(command_addchat, commands=['addchat'])

