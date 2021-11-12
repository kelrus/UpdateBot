import BotHandler
import asyncio
from aiogram import types
from Client import ClientKeyBoard
from Server import ChatsHandler, DataTimeHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStorageSendBot(StatesGroup):
    replyTextChat = State()
    replyTextSend = State()
    replyTextTime = State()
    replyTextData = State()
    replyTextDelayedSend = State()

class FSMStorageUserBot(StatesGroup):
    replyTextUserId = State()
    replyTextUserName = State()
    replyTextUserGroups = State()


async def CommandMenu(message: types.Message):
    await message.answer('/addchat - открывает клавиатуру для добавления чатов \n'
                         '/sendmessage - отправить сообщения в чаты\n'
                         '/delayednessage - добавить отложенное сообщение'
                         , reply_markup=ClientKeyBoard.keyBoardMenu)

async def CommandInfoChats(message: types.Message):
    await message.answer(str(ChatsHandler.GetChats()))

async def CommandAddChatsKeyboard(message: types.Message):
    await message.answer('/addchat - добавить чат в список чатов \n'
                         '/infochats - инфорсация о чатах'
                         , reply_markup=ClientKeyBoard.keyBoardChats)

async def CommandAddChatInput(message: types.Message):
    await FSMStorageSendBot.replyTextChat.set()
    await message.answer('введите id чата')

async def CommandAddChat(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextChat'] = message.text
    async with state.proxy() as data:
        ChatsHandler.AddChats(str(data['replyTextChat']))
    await state.finish()

async def CommandSendMessage(message: types.Message):
    await FSMStorageSendBot.replyTextSend.set()
    await message.answer('Напишите сообщение')

async def CommandSendMessageAll(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
        for chatid in ChatsHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextSend'])
    await state.finish()

async def CommandAddDelayedMessageKeyboard(message: types.Message):
    await message.answer('/addtime - задаёт время отправки сообщения. По умолчанию в 23:59 \n'
                         '/adddata - задаёт дату отправки сообщения. По умолчанию берёт текущий день \n'
                         '/addmessage - написать отложенное сообщение'
                         , reply_markup=ClientKeyBoard.keyBoardDelayed)

async def CommandAddTime(message: types.Message):
    await FSMStorageSendBot.replyTextTime.set()
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
    await FSMStorageSendBot.replyTextData.set()
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
    await FSMStorageSendBot.replyTextDelayedSend.set()
    await message.answer('Напишите сообщение')

async def CommandDelayedMessageAll(message: types.Message,  state=FSMContext):
    asyncio.create_task( _StartDelayedMessage(message, state))

async def _StartDelayedMessage(message: types.Message,  state=FSMContext):
    message.text = DataTimeHandler.HandlerMessageOnDataTime(message.text)
    if(DataTimeHandler.IsCorrectDataTime()):
        BotHandler.Scheduler.add_job(_SendDelayedMessageAll, 'date', run_date=DataTimeHandler.GetDataTime(), args=(message, state))
        DataTimeHandler.Clear()
    else:
        await message.answer('Неправлиьно указана дата или время')
    await state.finish()

async def _SendDelayedMessageAll(message: types.Message,  state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = str(message.text)
        for chatid in ChatsHandler.GetChats():
            await BotHandler.Bot.send_message(chatid, data['replyTextDelayedSend'])
    await state.finish()

async def CommandAddUserBot(message: types.Message):
    if ChatsHandler.CheckUserRightsIsAddUser(message.from_user.id):
        await FSMStorageUserBot.replyTextUserId.set()
        await message.answer('Веедите id пользователя')
    else:
        await message.answer('У вас нет прав доступа для добавления пользователей')

async def CommandReplyIdFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserId'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Веедите имя пользователя')

async def CommandReplyNameFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserName'] = str(message.text)
    await FSMStorageUserBot.next()
    await message.answer('Веедите группу(Права) пользователя')

async def CommandReplyGroupFSM(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextUserGroup'] = str(message.text)
    await state.finish()
    await message.answer('Пользователь успешно зарегистрирован')


async def CommandUsers(message: types.Message):
    await message.answer('/adduser - добавить пользователя \n'
                         '/addrigths - добавить права пользователю\n'
                         '/infousers - информация о текущих пользователях'
                         , reply_markup=ClientKeyBoard.keyBoardUsers)

def register_handler_client():
    BotHandler.Dp.register_message_handler(CommandMenu, commands=['start', 'help', 'menu'])
    BotHandler.Dp.register_message_handler(CommandInfoChats, commands=['infochats'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchat'])
    BotHandler.Dp.register_message_handler(CommandAddDelayedMessageKeyboard, commands=['delayedmessage'])
    BotHandler.Dp.register_message_handler(CommandAddChatInput, commands=['inputchat'])
    BotHandler.Dp.register_message_handler(CommandSendMessage, commands=['sendmessage'])
    BotHandler.Dp.register_message_handler(CommandAddChat, state=FSMStorageSendBot.replyTextChat)
    BotHandler.Dp.register_message_handler(CommandSendMessageAll, state=FSMStorageSendBot.replyTextSend)
    BotHandler.Dp.register_message_handler(CommandDelayedMessageAll, state=FSMStorageSendBot.replyTextDelayedSend)
    BotHandler.Dp.register_message_handler(CommandAddTime, commands=['addtime'])
    BotHandler.Dp.register_message_handler(CommandAddData, commands=['adddata'])
    BotHandler.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'])
    BotHandler.Dp.register_message_handler(CommandAddTimeFSM, state=FSMStorageSendBot.replyTextTime)
    BotHandler.Dp.register_message_handler(CommandAddDataFSM, state=FSMStorageSendBot.replyTextData)
    BotHandler.Dp.register_message_handler(CommandReplyIdFSM, state=FSMStorageUserBot.replyTextUserId)
    BotHandler.Dp.register_message_handler(CommandReplyNameFSM, state=FSMStorageUserBot.replyTextUserName)
    BotHandler.Dp.register_message_handler(CommandReplyGroupFSM, state=FSMStorageUserBot.replyTextUserRights)
    BotHandler.Dp.register_message_handler(CommandUsers, commands=['users'])
    BotHandler.Dp.register_message_handler(CommandAddUserBot, commands=['adduser'])