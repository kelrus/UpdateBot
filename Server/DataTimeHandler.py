from datetime import datetime, timedelta
import re

datetimeFormat = '%Y %m %d %H %M'
timeFormat = '%H:%M'
dateFormat = '%d.%m.%Y'

_data = ''
_day = ''
_month = ''
_year = ''
_time = ''
_hours = ''
_minute = ''
_isCurrentData = False
_isCurrentTime = False

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

def GetData():
    return _data

def GetDataTime(alarm = False):
    if(alarm):
        return datetime(int(_year),int(_month),int(_day),int(_hours),int(_minute)) - timedelta(minutes=30)
    return datetime(int(_year),int(_month),int(_day),int(_hours),int(_minute))

def GetDay():
    return _day

def GetYear():
    return _year

def GetMonth():
    return _month

def GetTime():
    return _time

def SetData(data: str):
    global  _data, _isCurrentData, _day, _month, _year
    if(str(datetime.now().date().strftime(dateFormat)) == str(data)):
        _isCurrentData = True

    _data = data
    _day = str(data[8] + data[9])
    _month = str(data[5] + data[6])
    _year = str(data[0] + data[1] + data[2] + data[3])


def SetTime(time: str):
    global _time,_isCurrentTime, _hours, _minute

    if((str(datetime.now().time().strftime(timeFormat))) == str(time)):
        _isCurrentTime = True

    _time = time
    _hours= str(time[0] + time[1])
    _minute = str(time[3] + time[4])


def HandlerMessageOnDataTime(message: str):
    global _isCurrentData, _isCurrentTime
    if IsCorrectData(message[:8]):
        SetData(message[:6] + '20' + message[6] + message[7])
        message = message[9:]
    else:
        SetData(str(datetime.now().date().strftime(dateFormat)))
    if IsCorrectTime(message):
        SetTime(message[:5])
        message = message[6:]
    else:
        SetTime(str(datetime.now().time().strftime(timeFormat)))
    return message

def IsCorrectData(data: str):
    if len(data)!=8:
        return False
    day = str(data[0]+data[1])
    month = str(data[3]+data[4])
    year = str(data[6]+data[7])
    if _IsCorrectMonth(month) and _IsCorrectYear(year) and _IsCorrectDay(day):
        if re.search(r'^[0-9]{2}.[0-9]{2}.[0-9]{2}$', data):
            return True
    return False

def IsCorrectTime(time: str):
    if re.search(r'([2]{1}[0-3]{1}:[0-5]{1}[0-9]{1})|([0-1]{1}[0-9]{1}:[0-5]{1}[0-9]{1})', time):
        return True
    return False

def _IsCorrectDay(day: str):
    if re.search(r'([3]{1}[0-1]{1})|([1-2]{1}[0-9]{1})|([0]{1}[1-9]{1})', day):
        return True
    return False

def _IsCorrectMonth(month: str):
    if re.search(r'([1]{1}[0-2]{1})|([0]{1}[1-9]{1})', month):
        return True
    return False

def _IsCorrectYear(year: str):
    yearFull= '20'+str(year)
    if re.search(r'^[2-9]{1}[0-9]{1}$', year):
        if int(yearFull) >= datetime.now().year:
            return True
    return False

def IsCurrentDataTime():
    if(_isCurrentTime == True and _isCurrentData == True):
        return True
    return False

def IsCorrectAlarmTime():
    if datetime.now() < (datetime(int(_year),int(_month),int(_day),int(_hours),int(_minute)) - timedelta(minutes=30)):
        return True
    return False