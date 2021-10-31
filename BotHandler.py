from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = '2098888741:AAHCJY8UGeCADgCU7wHb1qlAwNLPW4Auo2A'
Storage = MemoryStorage()

Bot = Bot(token= TOKEN)
Dp = Dispatcher(Bot, storage= Storage)

Scheduler = AsyncIOScheduler()