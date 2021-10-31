import BotHandler
import aioschedule
import apscheduler
import asyncio
from aiogram import types
from Client import ClientKeyBoard
from Client import DataTimeHandler
from Server import ServerHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMStorageBot(StatesGroup):
    replyTextChat = State()
    replyTextSend = State()
    replyTextTime = State()
    replyTextData = State()
    replyTextDelayedSend = State()

async def CommandMenu(message: types.Message):
    await message.answer('/addchat - открывает клавиатуру для добавления чатов \n'
                         '/sendmessage - отправить сообщения в чаты\n'
                         '/delayednessage - добавить отложенное сообщение'
                         , reply_markup=ClientKeyBoard.keyBoardMenu)

async def CommandInfoChats(message: types.Message):
    await message.answer(str(ServerHandler.GetChats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('/addchat - добавить чат в список чатов \n'
                         '/infochats - инфорсация о чатах'
                         , reply_markup=ClientKeyBoard.keyBoardChats)

async def CommandAddChatInput(message: types.Message):
    await FSMStorageBot.replyTextChat.set()
    await message.answer('введите id чата')

async def CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextChat'] = message.text
    async with state.proxy() as data:
        ServerHandler.AddChats(str(data['replyTextChat']))
    await state.finish()

async def CommandSendMessage(message: types.Message):
    await FSMStorageBot.replyTextSend.set()
    await message.answer('Напишите сообщение')

async def CommandSendMessageAll(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
        for chatid in ServerHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextSend'])
    await state.finish()

async def CommandAddDelayedMessageKeyboard(message: types.Message):
    await message.answer('/addtime - задаёт время отправки сообщения. По умолчанию в 23:59 \n'
                         '/adddata - задаёт дату отправки сообщения. По умолчанию берёт текущий день \n'
                         '/addmessage - написать отложенное сообщение'
                         , reply_markup=ClientKeyBoard.keyBoardDelayed)

async def CommandAddTime(message: types.Message):
    await FSMStorageBot.replyTextTime.set()
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
    await FSMStorageBot.replyTextData.set()
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
    await FSMStorageBot.replyTextDelayedSend.set()
    await message.answer('Напишите сообщение')

async def CommandDelayedMessageAll(message: types.Message,  state=FSMContext):
    asyncio.create_task( StartDelayedMessage(message, state))

async def StartDelayedMessage(message: types.Message,  state=FSMContext):

    BotHandler.Scheduler.add_job(SendDelayedMessageAll, 'date',run_date=DataTimeHandler.GetDataTime() , args=(message, state))
    BotHandler.Scheduler.start();

async def SendDelayedMessageAll(message: types.Message,  state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = message.text
        for chatid in ServerHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextDelayedSend'])
    await state.finish()


def register_handler_client():
    BotHandler.Dp.register_message_handler(CommandMenu, commands=['start', 'help', 'menu'])
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchat'])
    BotHandler.Dp.register_message_handler(CommandAddDelayedMessageKeyboard, commands=['delayedmessage'])
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.Dp.register_message_handler(CommandSendMessage, commands=['sendmessage'])
    BotHandler.Dp.register_message_handler(CommandAddChat, state=FSMStorageBot.replyTextChat)
    BotHandler.Dp.register_message_handler(CommandSendMessageAll, state=FSMStorageBot.replyTextSend)
    BotHandler.Dp.register_message_handler(CommandDelayedMessageAll, state=FSMStorageBot.replyTextDelayedSend)
    BotHandler.Dp.register_message_handler(CommandAddTime, commands=['addtime'])
    BotHandler.Dp.register_message_handler(CommandAddData, commands=['adddata'])
    BotHandler.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'])
    BotHandler.Dp.register_message_handler(CommandAddTimeFSM, state=FSMStorageBot.replyTextTime)
    BotHandler.Dp.register_message_handler(CommandAddDataFSM, state=FSMStorageBot.replyTextData)