#Файл запуска бота
from aiogram.utils import executor
from BotInit import Dp
from FrontBot import FrontHandler
from BackBot import DataBase
import BotInit
import asyncio





async def scheduler():
    BotInit.Scheduler.start()

#Запуск работы бота
async def on_startup(_):
    #Запуск регистрации всех комманд на боте
    FrontHandler.register_handler_client()
    #Запуск базы данных
    DataBase.SqlStart()
    #Запуск cron обработчика
    asyncio.create_task(scheduler())





executor.start_polling(Dp, skip_updates=True, on_startup=on_startup)
