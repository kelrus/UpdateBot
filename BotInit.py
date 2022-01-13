#файл инициализации бота
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler




#Токен используемого бота
TOKEN = '2098888741:AAHCJY8UGeCADgCU7wHb1qlAwNLPW4Auo2A'
#Инициализация хранилища
Storage = MemoryStorage()
#Инициализация Бота
Bot = Bot(token= TOKEN)
#Инициализация диспетчера бота и его хранения данных
Dp = Dispatcher(Bot, storage= Storage)
#Инициализация cron обработчика расписания отправки сообщений
Scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')