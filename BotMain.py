from aiogram.utils import executor
from BotHandler import dp

from Client import ClientHandler
from Server import ServerHandler

ClientHandler.register_handler_client(dp)
executor.start_polling(dp, skip_updates=True)

