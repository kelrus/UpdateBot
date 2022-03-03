#Файл отвечает за проверку правильности ввода данных пользователем




#Блок проверки правильного ввода информации для чата

#Проверка на правильность ввода id чата. Если хотя бы один символ не принадлежит диапозону "-0123456789", то ввод неверен. Проверка осуществляется по ASC.
def CheckInputChat(text):

    for sym in text:
        if((ord(sym) != 0 and ord(sym) != 45) and not (ord(sym)>=48 and ord(sym)<=57)):
            return False
    return True


#Блок проверки правильного ввода информации для пользователей

#Проверка на правильность ввода id пользователя. Если хотя бы один символ не принадлежит диапозону "0123456789", то ввод неверен. Проверка осуществляется по ASC.
def CheckInputUserId(text):

    for sym in text:
        if((ord(sym) != 0) and not (ord(sym)>=48 and ord(sym)<=57)):
            return False

    return True

#Проверка на правильность ввода имени пользователя. Если хотя бы один символ не принадлежит диапозону "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбю", то ввод неверен. Проверка осуществляется по ASC.
def CheckInputUserName(text):

    for sym in text:
        if((ord(sym) != 0) and not (ord(sym)>=65 and ord(sym)<=90) and not(ord(sym)>=97 and ord(sym)<=122) and not(ord(sym)>=1040 and ord(sym)<=1071) and not(ord(sym)>=1072 and ord(sym)<=1103)):
            print(1)
            return False
    return True

#Проверка на правильность ввода прав пользователя. Если введнные права не соотвествуют ни одному доступному праву на боте, то ввод неверен.
def CheckInputUserRights(text):

    if(text == 'Admin'):
        return True
    return False