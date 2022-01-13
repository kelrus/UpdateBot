#Данный файл осуществляет регистриацию всех основных элементов фронта, а также его общих частей.

import BotInit
from FrontBot import MenuKeyboard
from FrontBot import ChatsKeyboard
from FrontBot import DelayedMessageKeyboard
from FrontBot import UserKeyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text




#Блок реализует логику комманды отмены для других комманд в случаи,
#если пользователь передумал вводить какие-либо данные.

async def CommandCancel(message: types.Message, state=FSMContext):
    currentState = await state.get_state()
    if currentState is None:
        return
    await state.finish()
    await message.answer("Действие отменено")




#Здесь осуществляется запуск регистрации основных элементов фронта и его общих частей.

def register_handler_client():
    BotInit.Dp.register_message_handler(CommandCancel, state="*", commands='cancel')
    BotInit.Dp.register_message_handler(CommandCancel, Text(equals='cancel', ignore_case=True), state="*")
    MenuKeyboard.register_handler_menu()
    ChatsKeyboard.register_handler_chats()
    DelayedMessageKeyboard.register_handler_delayed_message()
    UserKeyboard.register_handler_users()
