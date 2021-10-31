from datetime import datetime
import re
_data = ''
_day = ''
_month = ''
_year = ''
_time = ''

def GetData():
    return _data

def GetDay():
    return _day

def GetYear():
    return _year

def GetMonth():
    return _month

def GetTime():
    return _time

def SetData(data: str):
    global  _data, _day, _month, _year
    _data = data
    _day = str(data[0] + data[1])
    _month = str(data[3] + data[4])
    _year = str(data[6] + data[7])

def SetTime(time: str):
    global _time
    _time = time

def IsCorrectTime(time: str):
    if time[0]=='2':
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
    if int(yearFull)>=datetime.now().year:
        if re.search(r'^[2-9]{1}[0-9]{1}$', year):
            return True
    return False


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