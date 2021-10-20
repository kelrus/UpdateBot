from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import Config

bot = Bot(token=Config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message: types.Message):
    await message.answer(message.text) # Отправка сообщения в чат
    await message.reply(message.text) # Упоминает сообщение на которое отвечает
    await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp, skip_updates=True)

