from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

KeyBoardMenu = ReplyKeyboardMarkup(resize_keyboard=True)

chats = KeyboardButton("Чаты")
send_message = KeyboardButton("Отправить сообщение")

KeyBoardMenu.add(chats)
KeyBoardMenu.insert(send_message)



KeyBoardChats = ReplyKeyboardMarkup(resize_keyboard=True)

_input = KeyboardButton("/inputchat")
_stop = KeyboardButton("/stopaddchat")
_info = KeyboardButton("/infochats")

KeyBoardChats.add(_input)
KeyBoardChats.insert(_stop)
KeyBoardChats.insert(_info)