from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from BotHandler import dp
from Client import ClientHandler


ClientHandler.register_handler_client(dp)
executor.start_polling(dp, skip_updates=True)

