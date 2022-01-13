import BotHandler
import asyncio
from aiogram import types
from Server import ChatsHandler, DataTimeHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageDelayedSendBot(StatesGroup):
    replyTextDelayedSend = State()
    replyTextDelete = State()





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
            datetimeAlarm = DataTimeHandler.GetDataTime(True)
            messageAlarm = "Внимание, через 30 минут: \n\n" + message.text
            BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=datetimeAlarm, args=(messageAlarm, state))
            ChatsHandler.AddMessage(messageAlarm, datetimeAlarm)
        datetime = DataTimeHandler.GetDataTime()
        BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=datetime,args=(message.text, state))
        ChatsHandler.AddMessage(message.text, datetime)

    DataTimeHandler.Clear()

    await state.finish()

async def _SendDelayedMessageAll(message: str, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = str(message)
        for chatid in ChatsHandler.GetChats():
            await BotHandler.Bot.send_message(int(chatid[0]), data['replyTextDelayedSend'])
            ChatsHandler.DeleteMessage(DataTimeHandler.GetCurrentDataTime())
    await state.finish()



async def CommandInfoMessage(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(ChatsHandler.GetMessage()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')



async def CommandDeleteMessageInput(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageDelayedSendBot.replyTextDelete.set()
        await message.answer('введите время сообщения, которое хотите удалить в формате гг-мм-дд чч:мм:00')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandDeleteMessage(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelete'] = message.text
    async with state.proxy() as data:
        ChatsHandler.DeleteMessage(str(data['replyTextDelete']))
    await state.finish()






def register_handler_delayed_message():
    BotHandler.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'], state=None)
    BotHandler.Dp.register_message_handler(CommandDelayedMessageAll, state=FSMStorageDelayedSendBot.replyTextDelayedSend)
    BotHandler.Dp.register_message_handler(CommandInfoMessage, commands=['infomessage'])
    BotHandler.Dp.register_message_handler(CommandDeleteMessageInput, commands=['deletemessage'], state=None)
    BotHandler.Dp.register_message_handler(CommandDeleteMessage, state=FSMStorageDelayedSendBot.replyTextDelete)