from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




keyboardMenu = InlineKeyboardMarkup(row_width=2)

_chats = InlineKeyboardButton(text="Управление чатами", callback_data='addchatkeyboard')
_sendMessage = InlineKeyboardButton(text="Отправить сообщение", callback_data='sendmessage')
_delayedMessage = InlineKeyboardButton(text="Управление отложенными сообщениями", callback_data='delayedmessagekeyboard')
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

_addMessage = KeyboardButton("/addmessage")
_infomessage = KeyboardButton("/infomessage")
_deleteMessage = KeyboardButton("/deletemessage")

keyboardDelayed.add(_addMessage)
keyboardDelayed.add(_infomessage)
keyboardDelayed.insert(_deleteMessage)




keyBoardUsers = ReplyKeyboardMarkup(resize_keyboard=True)

_addUser = KeyboardButton("/adduser")
_deleteUser = KeyboardButton("/deleteuser")
_infoUsers = KeyboardButton("/infousers")

keyBoardUsers.add(_infoUsers)
keyBoardUsers.add(_addUser)
keyBoardUsers.insert(_deleteUser)
