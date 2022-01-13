#Файл отвечает за управлением отложенными сообщениями с помощью ввода комманд,
#которые пишет пользователь на стороне фронта

import BotInit
import asyncio
from aiogram import types
from BackBot import BackHandler, DataTimeHandler
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup




# Инициализация хранилища. Здесь хранится текст пользователя для отправки отложенных сообщений
# и ввод времени сообщения, которое надо удалить

class FSMStorageDelayedSendBot(StatesGroup):
    replyTextDelayedSend = State()
    replyTextDelete = State()


#Блок отвечает за отправку отложенного сообщения во все доступные чаты.

async def CommandDelayedMessage(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageDelayedSendBot.replyTextDelayedSend.set()
        #Пользователю предлагается написать сообщение в определенном формате. После ввода этого сообщения, запускается событие _CommandDelayedMessageAll
        await message.answer('Напишите сообщение в формате дд.мм.гг чч:мм "сообщение". Если не ввести дату, то будет взята текущая дата.'
                             'Если не ввсети время, то будет взято текущее время')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandDelayedMessageAll(message: types.Message, state=FSMContext):
    #С помощью асинхроного метода запускаем обработку отложеного сообщения.
    #В качестве данных передаём сообщение пользователя и событие.
    asyncio.create_task(__StartDelayedMessage(message, state))

async def __StartDelayedMessage(message: types.Message, state=FSMContext):
    #Передаём в Бек сообщение для его проверки на наличие в нём даты и времени и последующей обработки этих данных.
    #Возвращаемым значением является чистое сообщение без даты и времени.
    message.text = DataTimeHandler.HandlerMessageOnDataTime(message.text)
    #Проверяем является ли заданное время в сообщении текущим. Если да - то немедленно отправляем его в чаты.
    if(DataTimeHandler.IsCurrentDataTime()):
        async with state.proxy() as data:
            data['replyTextDelayedSend'] = str(message.text)
            for chatId in BackHandler.GetIdChats():
                await BotInit.Bot.send_message(int(chatId[0]), data['replyTextDelayedSend'])
    else:
        #Проверям есть ли у нас время для предупреждения о сообщении и если да, мы откладываем предупрждение и сообщение.
        #Если времени нет, то откладывается только сообщение
        if(DataTimeHandler.IsCorrectAlarmTime()):
            datetimeAlarm = DataTimeHandler.GetDataTime(True)
            messageAlarm = "Внимание, через 30 минут: \n\n" + message.text
            BotInit.Scheduler.add_job(__SendDelayedMessageAll, 'date', run_date=datetimeAlarm, args=(messageAlarm, state))
            BackHandler.AddMessage(messageAlarm, datetimeAlarm)
        datetime = DataTimeHandler.GetDataTime()
        BotInit.Scheduler.add_job(__SendDelayedMessageAll, 'date', run_date=datetime,args=(message.text, state))
        BackHandler.AddMessage(message.text, datetime)
    #После того, как мы отложили сообщение, очищаем значение времени и даты в кеше.
    DataTimeHandler.Clear()

    await state.finish()

#Это событие, которое запускается в назначенных момент по дате и времени и отправляет сообщения в чаты.
async def __SendDelayedMessageAll(message: str, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelayedSend'] = str(message)
        for chatId in BackHandler.GetIdChats():
            await BotInit.Bot.send_message(int(chatId[0]), data['replyTextDelayedSend'])
            BackHandler.DeleteMessage(DataTimeHandler.GetCurrentDataTime())
    await state.finish()


#Блок отвечает за получение информации об отложенных сообщениях в Беке с помощью комманд,
#введеных пользователем на фронте
async def CommandInfoMessage(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await message.answer(str(BackHandler.GetMessage()))
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')


#Блок отвечает за удлаение отложенного сообщения. Для этого он просит пользователя дать ему время этого сообщения.

async def CommandDeleteMessageInput(message: types.Message):
    if await BackHandler.CheckUserRightsIsBotAccess(message.from_user.id):
        await FSMStorageDelayedSendBot.replyTextDelete.set()
        await message.answer('Введите время сообщения, которое хотите удалить в формате гг-мм-дд чч:мм:00')
    else:
        await message.answer('У вас нет доступа к боту. Обратитесь к администратору для их получения')

async def __CommandDeleteMessage(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['replyTextDelete'] = message.text
    async with state.proxy() as data:
        BackHandler.DeleteMessage(str(data['replyTextDelete']))
    await state.finish()




#Регистрация команд для управления задерженными сообщениями.

def register_handler_delayed_message():
    BotInit.Dp.register_message_handler(CommandDelayedMessage, commands=['addmessage'], state=None)
    BotInit.Dp.register_message_handler(__CommandDelayedMessageAll, state=FSMStorageDelayedSendBot.replyTextDelayedSend)
    BotInit.Dp.register_message_handler(CommandInfoMessage, commands=['infomessage'])
    BotInit.Dp.register_message_handler(CommandDeleteMessageInput, commands=['deletemessage'], state=None)
    BotInit.Dp.register_message_handler(__CommandDeleteMessage, state=FSMStorageDelayedSendBot.replyTextDelete)