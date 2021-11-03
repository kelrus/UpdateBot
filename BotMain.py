from aiogram.utils import executor
from BotHandler import Dp
from Client import ClientHandler
import BotHandler
import asyncio

async def scheduler():
    BotHandler.Scheduler.start();

async def on_startup(_):
    asyncio.create_task(scheduler())

ClientHandler.register_handler_client()
executor.start_polling(Dp, skip_updates=True, on_startup=on_startup)
