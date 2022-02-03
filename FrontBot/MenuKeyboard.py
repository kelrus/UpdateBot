#Файл для управления общими частями бота в виде клавиатуры-меню.
import BotInit
from aiogram import types
from aiogram.utils.exceptions import BotKicked
from FrontBot import Keyboards
from BackBot import BackHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup




#Хранилище для отправки текста в текущее время

class FSMStorageSendBot(StatesGroup):
    replyTextSend = State()


#Блок отвечающий за ознакомление пользователя с ботом. Вызывается с помощью команд start и help

async def CommandStartHelp(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer('Системные команды: \n'
                             '/start, /help - открывает список всех доступных команд на боте \n'
                             '/cancel - отменить предыдущее действие\n'
                             '/menu - вызывает удобное меню по боту\n\n'
                             'Управление чатами:\n'
                             '/addchat - добавить чат в список чатов \n'
                             '/deletechat - удалить чат из списка чатов \n'
                             '/infochats - информация о чатах\n\n'
                             'Управление пользователями:\n'
                             '/adduser - добавить пользователя \n'
                             '/deleteuser - удалить пользователя \n'
                             '/infousers - информация о текущих пользователях\n\n'
                             'Управление сообщениями:\n'
                             '/addmessage - написать отложенное сообщение\n'
                             '/infomessage - информация об отложенных сообщениях\n'
                             '/deletemessage - удалить отложенное сообщение\n')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок для вызова меню по боту с помощью комманды menu

async def CommandMenuKeyboard(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer("1. Управление чатами - добавление, удаление чатов для отправки сообщений.\n"
                             "2. Управление пользователями - добавление, удаление пользователей на боте. \n"
                             "3. Отправка сообщения - немедленная отправка сообщения в доступные чаты. \n"
                             "4. Управление отложенными сообщениями - добавление, удаление и просмотр информации об отложенных сообщениях"
                             , reply_markup=Keyboards.keyboardMenu)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок для вызова клавиатуры по управлению чатами

async def CommandAddChatsKeyboard(callback: types.CallbackQuery):
    if await BackHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await callback.message.answer('/addchat - добавить чат в список чатов \n'
                                      '/deletechat - удалить чат из списка чатов \n'
                                      '/infochats - информация о чатах\n'
                                      '/cancel - отменить предыдущее действие'
                                      , reply_markup=Keyboards.keyboardChats)
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок для вызова клавиатуры по управлению отложенными сообщениями

async def CommandAddDelayedMessageKeyboard(callback: types.CallbackQuery):
    if await BackHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await callback.message.answer('Для ввода времени сообщения используйте формат: \n дд.мм.гг чч:мм "соообщение"\n'
                             'При пустом вводе времени или даты, будет использовано текущее время или дата\n'
                             '/addmessage - написать отложенное сообщение\n'
                             '/infomessage - информация об отложенных сообщениях\n'     
                             '/deletemessage - удалить отложенное сообщение\n'
                             '/cancel - отменить предыдущее действие\n'
                             , reply_markup=Keyboards.keyboardDelayed)
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок для вызова клавиатуры по управлению пользователями

async def CommandUsers(callback: types.CallbackQuery):
    if await BackHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await callback.message.answer('/adduser - добавить пользователя \n'
                                      '/deleteuser - добавить пользователя \n'
                                      '/infousers - информация о текущих пользователях\n'
                                      '/cancel - отменить предыдущее действие'
                                      , reply_markup=Keyboards.keyboardUsers)
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок для отправки сообщения в данный момент

async def CommandSendMessage(callback: types.CallbackQuery):
    if await BackHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await FSMStorageSendBot.replyTextSend.set()
        await callback.message.answer('Напишите сообщение')
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandSendMessageAll(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
    for chatid in BackHandler.GetIdChats():
        try:
            await BotInit.Bot.send_message(int(chatid[0]), data['replyTextSend'])
        except BotKicked:
            await message.answer(str(chatid[0]) + ' - бот не добавлен в данный чат')
    await state.finish()




#Регистрация общих комманд для меню

def register_handler_menu():
    BotInit.Dp.register_message_handler(CommandMenuKeyboard, commands=['menu'])
    BotInit.Dp.register_message_handler(CommandStartHelp, commands=['start', 'help'])
    BotInit.Dp.register_callback_query_handler(CommandAddChatsKeyboard, text=['addchatkeyboard'])
    BotInit.Dp.register_callback_query_handler(CommandAddDelayedMessageKeyboard, text='delayedmessagekeyboard')
    BotInit.Dp.register_callback_query_handler(CommandSendMessage, text='sendmessage', state = None)
    BotInit.Dp.register_message_handler(__CommandSendMessageAll, state=FSMStorageSendBot.replyTextSend)
    BotInit.Dp.register_callback_query_handler(CommandUsers, text='users')
