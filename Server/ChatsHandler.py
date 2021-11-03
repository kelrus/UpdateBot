_chats = ['-1001560221019', '-1001706459960']

_id = ['1386657498']
_name = ['Владислав']
_groups = ['Admin']

_admin = ['AddUser', 'Send']
_user = ['Send']

_rights = {'Admin':_admin, 'User':_user}

_users = {'id':_id, 'name': _name, 'groups': _groups}

_currentUserInd = str

def GetUsers():
    return _users

def GetChats():
    return _chats

def AddChats(IdChat : str):
    _chats.append(IdChat)

def AddUser(id, name, groups):
    newUser = {'id':id, 'name': name, 'groups': groups}
    _users.update([newUser])

def CkeckUserInDb(idUser: str):
    global _currentUserInd
    if idUser in _users.get('id'):
        _currentUserInd = _users.get('id').index(idUser)
        return True
    return False

def CheckUserRightsIsAddUser(idUser: str):
    global _currentUserInd
    if CkeckUserInDb(idUser):
        if 'AddUser' in _rights.get(_users.get('groups')[_currentUserInd]):
            return True
        return False
