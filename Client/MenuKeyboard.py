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



async def CommandStartHelp(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
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



async def CommandMenuKeyboard(message: types.Message):
    if await ChatsHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer("1. Управление чатами - добавление, удаление чатов для отправки сообщений.\n"
                             "2. Управление пользователями - добавление, удаление пользователей на боте. \n"
                             "3. Отправка сообщения - немедленная отправка сообщения в доступные чаты. \n"
                             "4. Управление отложенными сообщениями - добавление, удаление и просмотр информации об отложенных сообщениях"
                             , reply_markup=Keyboards.keyboardMenu)
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')



async def CommandAddChatsKeyboard(callback: types.CallbackQuery):
    if await ChatsHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await callback.message.answer('/addchat - добавить чат в список чатов \n'
                                      '/deletechat - удалить чат из списка чатов \n'
                                      '/infochats - информация о чатах\n'
                                      '/cancel - отменить предыдущее действие'
                                      , reply_markup=Keyboards.keyboardChats)
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')



async def CommandAddDelayedMessageKeyboard(callback: types.CallbackQuery):
    if await ChatsHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
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



async def CommandSendMessage(callback: types.CallbackQuery):
    if await ChatsHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await FSMStorageSendBot.replyTextSend.set()
        await callback.message.answer('Напишите сообщение')
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def CommandSendMessageAll(message: types.Message, state = FSMContext):
    async with state.proxy() as data:
        data['replyTextSend'] = message.text
    for chatid in ChatsHandler.GetChats():
        await BotHandler.Bot.send_message(int(chatid[0]), data['replyTextSend'])
    await state.finish()



async def CommandUsers(callback: types.CallbackQuery):
    if await ChatsHandler.CheckUserRightsIsBotAccess(callback.from_user.id):
        await callback.message.answer('/adduser - добавить пользователя \n'
                                      '/deleteuser - добавить пользователя \n'
                                      '/infousers - информация о текущих пользователях\n'
                                      '/cancel - отменить предыдущее действие'
                                      , reply_markup=Keyboards.keyBoardUsers)
        await callback.answer()
    else:
        await callback.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')




def register_handler_menu():
    BotHandler.Dp.register_message_handler(CommandMenuKeyboard, commands=['menu'])
    BotHandler.Dp.register_message_handler(CommandStartHelp, commands=['start', 'help'])
    BotHandler.Dp.register_callback_query_handler(CommandAddChatsKeyboard, text=['addchatkeyboard'])
    BotHandler.Dp.register_callback_query_handler(CommandAddDelayedMessageKeyboard, text='delayedmessagekeyboard')
    BotHandler.Dp.register_callback_query_handler(CommandSendMessage, text='sendmessage', state = None)
    BotHandler.Dp.register_message_handler(CommandSendMessageAll, state=FSMStorageSendBot.replyTextSend)
    BotHandler.Dp.register_callback_query_handler(CommandUsers, text='users')
