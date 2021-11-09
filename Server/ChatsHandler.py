_chats = ['-1001560221019', '-1001706459960']

_idOwner = 1386657498
_nameOwner = 'Владислав'
_rightsOwner = ['AddUser','AddChat', 'SendMessage']

_rightsAddUser = "AddUser"
_rightsAddChats = "AddChat"
_rightsSendMessage = "SendMessage"

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
    _newUser["id"] = _idOwner
    _newUser["name"] = _nameOwner
    _newUser["rights"] = _rightsOwner
    _users.append(_newUser)

def AddRightsSendMessage(idUser: str):
    s = 1

def _CkeckUserInDb(idUser: str):
    global _currentUserInd
    num = 0
    for _user in _users:
        if int(idUser) == int(_user["id"]):
            _currentUserInd = num
            return True
        num += 1
    return False

def CheckUserRightsIsAddUser(idUser: str):
    global _currentUserInd
    if _CkeckUserInDb(idUser):
        if _rightsAddUser in (_users[_currentUserInd])["rights"]:
            return True
    return False

def CheckUserRightsIsSendMessage(idUser: str):
    global _currentUserInd
    if _CkeckUserInDb(idUser):
        if _rightsSendMessage in (_users[_currentUserInd])["rights"]:
            return True
    return False