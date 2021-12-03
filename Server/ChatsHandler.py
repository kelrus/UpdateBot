_chats = ['-1001560221019', '-1001706459960']

_idOwner = 1386657498
_nameOwner = 'Владислав'
_rightsOwner = ['BotAccess']

_rightsBotAccess= "BotAccess"

_userOwner = dict()
_userOwner["id"] = _idOwner
_userOwner["name"] = _nameOwner
_userOwner["rights"] = _rightsOwner

_users = []
_users.append(_userOwner)

_currentUserInd = ''

def GetUsers():
    return _users

def GetChats():
    return _chats

def AddChats(IdChat : str):
    _chats.append(IdChat)

def AddUser(id, name, rights):
    _newUser = dict()
    _newUser["id"] = int(id)
    _newUser["name"] = name
    _newUser["rights"] = [rights]
    _users.append(_newUser)
    print(_users)

def _CkeckUserInDb(idUser: str):
    global _currentUserInd
    num = 0
    for _user in _users:
        if int(idUser) == int(_user["id"]):
            _currentUserInd = num
            return True
        num += 1
    return False

def CheckUserRightsIsBotAccess(idUser: str):
    global _currentUserInd
    if _CkeckUserInDb(idUser):
        if _rightsBotAccess in (_users[_currentUserInd])["rights"]:
            return True
    return False
