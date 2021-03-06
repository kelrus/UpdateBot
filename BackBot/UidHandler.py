# Файл генерации uid по id сообщения в планировщике, дате отправки сообщения и тексту сообщения.
from datetime import datetime



#Инициизация таблицы перевода в шестнадцатеричную систему

__table = '0123456789ABCDEF'

def __TableUid(dig, base):

    global __table

    quotient, remainder = divmod(dig, base)

    if quotient == 0:
        return __table[remainder]
    else:
        return str(__TableUid(quotient, base)) + str(__table[remainder])



def __StepGenUid(num: int):
    if num > 16:
        return int(num / 16) + 1
    else:
        return 1



def __SplittingMessageIntoASC(message):

    step = __StepGenUid(len(message))

    newMessageASC = []
    currentNum = 0
    while currentNum + step <= len(message):
        newSymbolMessageASC = 0
        num = 0
        while num < step:
            newSymbolMessageASC += ord(message[currentNum  + num])
            num += 1
        currentNum += int(step)
        newMessageASC.append(newSymbolMessageASC)

    return newMessageASC



def __GetTaleMessageUid(message):
    sumTale = 0
    for sym in message:
        sumTale += ord(sym)
    return sumTale



def GenerateMessageUid(messageid, data : datetime, message):

    time = data.hour + data.day + data.year + data.month + data.minute
    messageASCII = __SplittingMessageIntoASC(message)
    messageUID = ''
    step = __StepGenUid(len(message))
    newLenMessage = len(message) - step*16

    taleMessage = 0
    if newLenMessage > 0:
        taleMessage = __GetTaleMessageUid(message[len(message)-newLenMessage:len(message)])

    stepGenUid = 0
    global symUID
    for sym in messageASCII:
        if(stepGenUid % 2 == 0):
            symUID = sym + taleMessage + messageid
        else:
            symUID = sym + messageid + int(time)
        stepGenUid += 1
        symUID = __TableUid(symUID, 16)
        messageUID += str(symUID)
    return messageUID