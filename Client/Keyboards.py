from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




keyboardMenu = InlineKeyboardMarkup(row_width=2)

_chats = InlineKeyboardButton(text="Управление чатами", callback_data='addchatkeyboard')
_sendMessage = InlineKeyboardButton(text="Отправить сообщение", callback_data='sendmessage')
_delayedMessage = InlineKeyboardButton(text="Отложить сообщение", callback_data='delayedmessagekeyboard')
_users = InlineKeyboardButton(text="Управление пользователями", callback_data='users')

keyboardMenu.add(_chats)
keyboardMenu.insert(_users)
keyboardMenu.add(_sendMessage)
keyboardMenu.insert(_delayedMessage)





keyboardChats = ReplyKeyboardMarkup(resize_keyboard=True)

_inputChat = KeyboardButton("/addchat")
_deleteChat = KeyboardButton("/deletechat")
_info = KeyboardButton("/infochats")

keyboardChats.add(_inputChat)
keyboardChats.insert(_deleteChat)
keyboardChats.insert(_info)





keyboardDelayed = ReplyKeyboardMarkup(resize_keyboard=True)

_time = KeyboardButton("/addtime")
_data = KeyboardButton("/adddata")
_message = KeyboardButton("/addmessage")

keyboardDelayed.add(_data)
keyboardDelayed.insert(_time)
keyboardDelayed.insert(_message)





keyBoardUsers = ReplyKeyboardMarkup(resize_keyboard=True)

_addUser = KeyboardButton("/adduser")
_infoUsers = KeyboardButton("/infousers")

keyBoardUsers.add(_infoUsers)
keyBoardUsers.add(_addUser)
