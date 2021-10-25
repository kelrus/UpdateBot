from aiogram.utils import executor
from BotHandler import Dp
from Client import ClientHandler


ClientHandler.register_handler_client()
executor.start_polling(Dp, skip_updates=True)

