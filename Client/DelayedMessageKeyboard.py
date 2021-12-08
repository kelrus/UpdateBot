import BotHandler
import asyncio
from aiogram import types
from Server import ChatsHandler, DataTimeHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageDelayedSendBot(StatesGroup):
    replyTextDelayedSend = State()






async def CommandDelayedMessage(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageDelayedSendBot.replyTextDelayedSend.set()
        await message.answer('Напишите сообщение')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandDelayedMessageAll(message: types.Message, state=FSMContext):
    asyncio.create_task(_StartDelayedMessage(message, state))

async def _StartDelayedMessage(message: types.Message, state=FSMContext):
    message.text = DataTimeHandler.HandlerMessageOnDataTime(message.text)
    if(DataTimeHandler.IsCurrentDataTime()):
        async with state.proxy() as data:
            data['replyTextDelayedSend'] = str(message.text)
            for chatid in ChatsHandler.GetChats():
                await BotHandler.Bot.send_message(int(chatid[0]), data['replyTextDelayedSend'])
    else:
        if(DataTimeHandler.IsCorrectAlarmTime()):
            message.text = "Внимание, через 30 минут: \n\n" + message.text
            BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=DataTimeHandler.GetDataTime(True), args=(message, state))
        BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=DataTimeHandler.GetDataTime(),args=(message, state))
    DataTimeHandler.Clear()

    await state.finish()

async def _SendDelayedMessageAll(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = str(message.text)
        for chatid in ChatsHandler.GetChats():
            await BotHandler.Bot.send_message(int(chatid[0]), data['replyTextDelayedSend'])
    await state.finish()





def register_handler_delayed_message():
    BotHandler.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'], state=None)
    BotHandler.Dp.register_message_handler(CommandDelayedMessageAll, state=FSMStorageDelayedSendBot.replyTextDelayedSend)