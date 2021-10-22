from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

keyBoardMenu = ReplyKeyboardMarkup(resize_keyboard=True)

_chats = KeyboardButton("/addchat")
_sendMessage = KeyboardButton("/sendmessage")

keyBoardMenu.add(_chats)
keyBoardMenu.insert(_sendMessage)



keyBoardChats = ReplyKeyboardMarkup(resize_keyboard=True)

_input = KeyboardButton("/inputchat")
_stop = KeyboardButton("/stopaddchat")
_info = KeyboardButton("/infochats")

keyBoardChats.add(_input)
keyBoardChats.insert(_stop)
keyBoardChats.insert(_info)