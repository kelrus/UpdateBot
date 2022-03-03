#Файл отвечает за проверку правильности ввода данных пользователем





#Проверка на правильность ввода id чата. Если хотя бы один символ не принадлежит диапозону "-0123456789", то ввод неверен. Проверка осуществляется по ASC.
def CheckInputChat(text):

    for sym in text:
        if((ord(sym) != 0 and ord(sym) != 45) and not (ord(sym)>=48 and ord(sym)<=57)):
            return False
        return True

