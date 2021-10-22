from aiogram import Dispatcher, types

import BotHandler

Chats = []

def getchats():
    return Chats

def addChats(IdChat : str):
    Chats.append(IdChat)