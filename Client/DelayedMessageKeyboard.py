import BotHandler
import asyncio
from aiogram import types
from Server import ChatsHandler, DataTimeHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageDelayedSendBot(StatesGroup):
    replyTextTime = State()
    replyTextData = State()
    replyTextDelayedSend = State()





async def CommandAddTime(message: types.Message):
    await FSMStorageDelayedSendBot.replyTextTime.set()
    await message.answer('Задайте время сообщения')

async def CommandAddTimeFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextTime'] = message.text
        if(DataTimeHandler.IsCorrectTime(data['replyTextTime'])):
            DataTimeHandler.SetTime(data['replyTextTime'])
        else:
            await message.answer('Неправильно указано время. Введите в формате чч:мм\n'
                                 'где чч - число от 00 до 24, мм - число от 00 до 59')
    await state.finish()



async def CommandAddData(message: types.Message):
    await FSMStorageDelayedSendBot.replyTextData.set()
    await message.answer('Задайте дату сообщения')

async def CommandAddDataFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextData'] = message.text
        if(DataTimeHandler.IsCorrectData(data['replyTextData'])):
            DataTimeHandler.SetData(data['replyTextData'])
        else:
            await message.answer('Неправильно указана дата. Введите в формате дд.мм.гг\n'
                                 'где дд - число от 01 до 31, мм - число от 01 до 12, гг - от текущего года до 99')
    await state.finish()



async def CommandDelayedMessage(message: types.Message):
    await FSMStorageDelayedSendBot.replyTextDelayedSend.set()
    await message.answer('Напишите сообщение')

async def CommandDelayedMessageAll(message: types.Message, state=FSMContext):
    asyncio.create_task(_StartDelayedMessage(message, state))

async def _StartDelayedMessage(message: types.Message, state=FSMContext):
    message.text = DataTimeHandler.HandlerMessageOnDataTime(message.text)
    if (DataTimeHandler.IsCorrectDataTime()):
        BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=DataTimeHandler.GetDataTime(), args=(message, state))
        DataTimeHandler.Clear()
    else:
        await message.answer('Неправлиьно указана дата или время')
    await state.finish()

async def _SendDelayedMessageAll(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = str(message.text)
        for chatid in ChatsHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextDelayedSend'])
    await state.finish()





def register_handler_delayed_message():
    BotHandler.Dp.register_message_handler(CommandAddTime, commands=['addtime'])
    BotHandler.Dp.register_message_handler(CommandAddTimeFSM, state=FSMStorageDelayedSendBot.replyTextTime)
    BotHandler.Dp.register_message_handler(CommandAddData, commands=['adddata'])
    BotHandler.Dp.register_message_handler(CommandAddDataFSM, state=FSMStorageDelayedSendBot.replyTextData)
    BotHandler.Dp.register_message_handler(CommandDelayedMessageAll, state=FSMStorageDelayedSendBot.replyTextDelayedSend)
    BotHandler.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'])