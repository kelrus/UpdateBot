from aiogram.utils import executor
from BotHandler import Dp
from Client import ClientHandler
from Server import DataBase
import BotHandler
import asyncio





async def scheduler():
    BotHandler.Scheduler.start()

async def on_startup(_):
    ClientHandler.register_handler_client()
    DataBase.SqlStart()
    asyncio.create_task(scheduler())





executor.start_polling(Dp, skip_updates=True, on_startup=on_startup)
