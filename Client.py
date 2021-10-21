from aiogram import Bot, types

import Config

def HandlerClient():
    @Config.dp.message_handler(commands=['start', 'help'])
    async def command_start(message: types.Message):
        await Config.bot.send_message(message.from_user.id, 'Бот Запущен')
