from aiogram.types import ReplyKeyboardMarkup, KeyboardButton





keyboardMenu = ReplyKeyboardMarkup(resize_keyboard=True)

_chats = KeyboardButton("/addchatkeyboard")
_sendMessage = KeyboardButton("/sendmessage")
_delayedMessage = KeyboardButton("/delayedmessagekeyboard")
_users = KeyboardButton("/users")

keyboardMenu.add(_chats)
keyboardMenu.insert(_users)
keyboardMenu.add(_sendMessage)
keyboardMenu.insert(_delayedMessage)





keyboardChats = ReplyKeyboardMarkup(resize_keyboard=True)

_inputChat = KeyboardButton("/addchat")
_info = KeyboardButton("/infochats")

keyboardChats.add(_inputChat)
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
_addRigthts = KeyboardButton("/addrigths")
_infoUsers = KeyboardButton("/infousers")

keyBoardUsers.add(_infoUsers)
keyBoardUsers.add(_addUser)
keyBoardUsers.insert(_addRigthts)
