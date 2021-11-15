import BotHandler
from Client import MenuKeyboard
from Client import ChatsKeyboard
from Client import DelayedMessageKeyboard
from Client import UserKeyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text





async def CommandCancel(message: types.Message, state=FSMContext):
    currentState = await state.get_state()
    if currentState is None:
        return
    await state.finish()
    await message.answer("Действие отменено")





def register_handler_client():
    BotHandler.Dp.register_message_handler(CommandCancel, state="*", commands='cancel')
    BotHandler.Dp.register_message_handler(CommandCancel, Text(equals='cancel', ignore_case=True), state="*")
    MenuKeyboard.register_handler_menu()
    ChatsKeyboard.register_handler_chats()
    DelayedMessageKeyboard.register_handler_delayed_message()
    UserKeyboard.register_handler_users()
