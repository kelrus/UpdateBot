import BotHandler
from aiogram import types
from Client import Keyboards
from Server import ChatsHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMStorageSendBot(StatesGroup):
    replyTextSend = State()

class FSMStorageUserFirstBot(StatesGroup):
    replyTextUserId = State()
    replyTextUserName = State()
    replyTextUserRights = State()



async def CommandMenuKeyboard(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer('/addchat - открывает клавиатуру для добавления чатов \n'
                             '/sendmessage - отправить сообщения в чаты\n'
                             '/delayednessage - добавить отложенное сообщение\n'
                             '/cancel - отменить предыдущее действие'
                             , reply_markup=Keyboards.keyboardMenu)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


async def CommandAddChatsKeyboard(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer('/addchat - добавить чат в список чатов \n'
                             '/infochats - инфорсация о чатах\n'
                             '/cancel - отменить предыдущее действие'
                             , reply_markup=Keyboards.keyboardChats)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


async def CommandAddDelayedMessageKeyboard(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer('/addtime - задаёт время отправки сообщения. По умолчанию в 23:59 \n'
                             '/adddata - задаёт дату отправки сообщения. По умолчанию берёт текущий день \n'
                             '/addmessage - написать отложенное сообщение\n'
                             '/cancel - отменить предыдущее действие'
                             , reply_markup=Keyboards.keyboardDelayed)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


async def CommandSendMessage(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageSendBot.replyTextSend.set()
        await message.answer('Напишите сообщение')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandSendMessageAll(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
    for chatid in ChatsHandler.GetChats():
        await BotHandler.Bot.send_message(chatid, data['replyTextSend'])
    await state.finish()



async def CommandUsers(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer('/adduser - добавить пользователя \n'
                             '/addrigths - добавить права пользователю\n'
                             '/infousers - информация о текущих пользователях\n'
                             '/cancel - отменить предыдущее действие'
                             , reply_markup=Keyboards.keyBoardUsers)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')




def register_handler_menu():
    BotHandler.Dp.register_message_handler(CommandMenuKeyboard, commands=['start', 'help', 'menu'])
    BotHandler.Dp.register_message_handler(CommandAddChatsKeyboard, commands=['addchatkeyboard'])
    BotHandler.Dp.register_message_handler(CommandAddDelayedMessageKeyboard, commands=['delayedmessagekeyboard'])
    BotHandler.Dp.register_message_handler(CommandSendMessage, commands=['sendmessage'], state = None)
    BotHandler.Dp.register_message_handler(CommandSendMessageAll, state=FSMStorageSendBot.replyTextSend)
    BotHandler.Dp.register_message_handler(CommandUsers, commands=['users'])
