from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyBoardMenu = ReplyKeyboardMarkup(resize_keyboard=True)

_chats = KeyboardButton("/addchat")
_sendMessage = KeyboardButton("/sendmessage")
_delayedMessage = KeyboardButton("/delayedmessage")

keyBoardMenu.add(_chats)
keyBoardMenu.insert(_sendMessage)
keyBoardMenu.add(_delayedMessage)



keyBoardChats = ReplyKeyboardMarkup(resize_keyboard=True)

_input = KeyboardButton("/inputchat")
_stop = KeyboardButton("/stopaddchat")
_info = KeyboardButton("/infochats")

keyBoardChats.add(_input)
keyBoardChats.insert(_stop)
keyBoardChats.insert(_info)

keyBoardDelayed = ReplyKeyboardMarkup(resize_keyboard=True)

_time = KeyboardButton("/addtime")
_data = KeyboardButton("/adddata")
_message = KeyboardButton("/addmessage")

keyBoardDelayed.add(_data)
keyBoardDelayed.insert(_time)
keyBoardDelayed.insert(_message)