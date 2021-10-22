from aiogram.utils import executor
from BotHandler import Dp
from Client import ClientHandler


ClientHandler.register_handler_client(Dp)
executor.start_polling(Dp, skip_updates=True)

