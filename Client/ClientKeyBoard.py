from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

chats = KeyboardButton("Чаты")
send_message = KeyboardButton("Отправить сообщение")

KeyBoardMenu = ReplyKeyboardMarkup(resize_keyboard=True)

KeyBoardMenu.add(chats)
KeyBoardMenu.insert(send_message)
