#Файл для инициализации различных клавиатур на боте

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



#Инициализация клавиатуры для меню
keyboardMenu = InlineKeyboardMarkup(row_width=2)

#Инициализация кнопок для клавиатуры
__chats = InlineKeyboardButton(text="Управление чатами", callback_data='addchatkeyboard')
__sendMessage = InlineKeyboardButton(text="Отправить сообщение", callback_data='sendmessage')
__delayedMessage = InlineKeyboardButton(text="Управление отложенными сообщениями", callback_data='delayedmessagekeyboard')
__users = InlineKeyboardButton(text="Управление пользователями", callback_data='users')

#Добавление кнопок в клавиатуру
keyboardMenu.add(__chats)
keyboardMenu.insert(__users)
keyboardMenu.add(__sendMessage)
keyboardMenu.insert(__delayedMessage)




#Клавиатура для управления чатами
keyboardChats = ReplyKeyboardMarkup(resize_keyboard=True)

__inputChat = KeyboardButton("/addchat")
__deleteChat = KeyboardButton("/deletechat")
__infoChats = KeyboardButton("/infochats")

keyboardChats.add(__inputChat)
keyboardChats.insert(__deleteChat)
keyboardChats.insert(__infoChats)




#Клавиатура для управления отложенными сообщениями
keyboardDelayed = ReplyKeyboardMarkup(resize_keyboard=True)

__addMessage = KeyboardButton("/addmessage")
__infoMessage = KeyboardButton("/infomessage")
__deleteMessage = KeyboardButton("/deletemessage")

keyboardDelayed.add(__addMessage)
keyboardDelayed.add(__infoMessage)
keyboardDelayed.insert(__deleteMessage)



#Клавиатура для управления пользователями
keyboardUsers = ReplyKeyboardMarkup(resize_keyboard=True)

__addUser = KeyboardButton("/adduser")
__deleteUser = KeyboardButton("/deleteuser")
__infoUsers = KeyboardButton("/infousers")

keyboardUsers.add(__infoUsers)
keyboardUsers.add(__addUser)
keyboardUsers.insert(__deleteUser)
