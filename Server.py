from aiogram import Bot, types

import Config

Chats = []

def HandlerServer():
    @Config.dp.message_handler(commands=['addchats'])
    async def command_start(message: types.Message):
        await message.answer('Напишите id чата')
