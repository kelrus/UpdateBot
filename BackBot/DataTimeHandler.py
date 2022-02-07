#Файл для обработки даты, времени и временных зон
from datetime import datetime, timedelta
import pytz
from tzlocal import get_localzone
import re




#Блок инициализации

#Задаётся формат записи времени и даты
datetimeFormat = '%Y %m %d %H %M'
timeFormat = '%H:%M'
dateFormat = '%d.%m.%Y'

#Задаётся рабочая временная зона
tzMoscow = pytz.timezone("Europe/Moscow")
tzLocal = get_localzone()

#Вычисление разници между временем сервера и рабочей временной зоны
deltaLocal = abs(tzMoscow.localize(datetime.now()) - tzLocal.localize(datetime.now()).astimezone(tzMoscow))

#Инициализация переменных даты и времени
_data = ''
_day = ''
_month = ''
_year = ''
_time = ''
_hours = ''
_minute = ''
_seconds = '00'
_isCurrentData = False
_isCurrentTime = False


#Блок очистки даты и времени

def Clear():
    global _data, _day, _month, _year, _hours, _minute , _time,  _isCurrentData, _isCurrentTime
    _data = ''
    _day = ''
    _month = ''
    _year = ''
    _time = ''
    _hours = ''
    _minute = ''
    _isCurrentData = False
    _isCurrentTime = False


#Блок получения данных даты и времени

#Получение даты
def GetData():
    return _data

#Получение дня
def GetDay():
    return _day

#Получение года
def GetYear():
    return _year

#Получение месяца
def GetMonth():
    return _month

#Получение времени
def GetTime():
    return _time

#Получение даты и времени отправки сообщения
def GetDataTime(alarm = False):
    #Если сообщения является предупреждением, то выставить время на 30 минут раньше
    if(alarm):
        return datetime(int(_year), int(_month), int(_day), int(_hours), int(_minute), int(_seconds)) - timedelta(minutes=30)
    return datetime(int(_year), int(_month), int(_day), int(_hours), int(_minute), int(_seconds))

#Получение текущего рабочего времени
def GetCurrentDataTime():
    return (datetime.now() + timedelta(seconds=deltaLocal.seconds)).strftime('%Y-%m-%d %H:%M:00')


#Блок внесения данных даты и времени

#Установка даты сообщения
def SetData(data: str):
    global  _data, _isCurrentData, _day, _month, _year
    #Если текущая рабочая дата совпадает с полученной, то запоминаем, что новая дата является текущей.
    if(str(datetime.now().date().strftime(dateFormat)) == str(data)):
        _isCurrentData = True

    _data = data
    #По умолчанию дата приходит в формате дд.мм.гггг
    #Для получения дня месяца и года выделяем из формата строки нужные символы
    _day = str(data[0] + data[1])
    _month = str(data[3] + data[4])
    _year = str(data[6] + data[7] + data[8] + data[9])

#Устанавливаем время сообщения
def SetTime(time: str):
    global _time,_isCurrentTime, _hours, _minute
    # Если текущее рабочее время совпадает с полученным, то запоминаем, что новое время является текущим.
    if((str(datetime.now().time().strftime(timeFormat))) == str(time)):
        _isCurrentTime = True

    _time = time
    # По умолчанию время приходит в формате чч:мм
    # Для получения часов и минут выделяем из формата строки нужные символы
    _hours= str(time[0] + time[1])
    _minute = str(time[3] + time[4])


#Блок проверки даты и времени на корректность

#Проверяем является ли введённая пользователем дата корректной
def IsCorrectData(data: str):
    #Длина формата дд.мм.гг составляет 8 символом, что мы и проверяем
    if len(data)!=8:
        return False
    # По умолчанию дата приходит в формате дд.мм.гг
    # Для получения дня месяца и года выделяем из формата строки нужные символы
    day = str(data[0]+data[1])
    month = str(data[3]+data[4])
    year = str(data[6]+data[7])
    #Если день месяц и год являются корректными, то и дата является корректной.
    if _IsCorrectMonth(month) and _IsCorrectYear(year) and _IsCorrectDay(day):
        #Проверям правильно ли был записан формат даты пользователем. Если нет, то нельзя гарантировать корректность даты.
        if re.search(r'^[0-9]{2}.[0-9]{2}.[0-9]{2}$', data):
            return True
    return False

#С помощью регулярного выражения проверям правильность дня - от 01 до 31
def _IsCorrectDay(day: str):
    if re.search(r'([3]{1}[0-1]{1})|([1-2]{1}[0-9]{1})|([0]{1}[1-9]{1})', day):
        return True
    return False

#С помощью регулярного выражения проверяем правильность месяца - от 01 до 12
def _IsCorrectMonth(month: str):
    if re.search(r'([1]{1}[0-2]{1})|([0]{1}[1-9]{1})', month):
        return True
    return False

#С помощью регулярного выражения проверяем правильность года - он должен быть не меньше текущего в формате 'гг'
def _IsCorrectYear(year: str):
    yearFull= '20'+str(year)
    if re.search(r'^[2-9]{1}[0-9]{1}$', year):
        if int(yearFull) >= datetime.now().year:
            return True
    return False

#С помощью регулярного выражения проверяем корректность времени. Оно должно быть в формате 'чч:мм', где
# чч - от 00 до 23 и мм - от 00 до 59
def IsCorrectTime(time: str):
    if re.search(r'([2]{1}[0-3]{1}:[0-5]{1}[0-9]{1})|([0-1]{1}[0-9]{1}:[0-5]{1}[0-9]{1})', time):
        return True
    return False

#Проверям является ли время отправки сообщения текущим временем
def IsCurrentDataTime():
    #Если оба флага правда - значит время отправки является текущим
    if(_isCurrentTime == True and _isCurrentData == True):
        return True
    return False

#Проверяем является ли возможным запуситить предупреждение о сообщении
def IsCorrectAlarmTime():
    if datetime.now() < (datetime(int(_year),int(_month),int(_day),int(_hours),int(_minute)) - timedelta(minutes=30)):
        return True
    return False

#Проверяем является ли данная дата уже прошедншей
def IsCorrectDateTime(datetimeIs: datetime):
    if datetime.now() < datetimeIs :
        return True
    return False



#Блок обработки даты и времени

#Функция получает сообщение пользователя об отложенном сообщении и обрабатывает его.
#Если сообщение корректно - она записывает дату и время отправки этого сообщения и возвращает сообщение без даты и времени.
def HandlerMessageOnDataTime(message: str):
    #Проверяем корректна ли дата.
    if IsCorrectData(message[:8]):
        SetData(message[:6] + '20' + message[6] + message[7])
        message = message[9:]
    else:
        SetData(str(datetime.now().date().strftime(dateFormat)))
    #Проверяем корректно ли время
    if IsCorrectTime(message):
        SetTime(message[:5])
        message = message[6:]
    else:
        SetTime(str(datetime.now().time().strftime(timeFormat)))
    return message