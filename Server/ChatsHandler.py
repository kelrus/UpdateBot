_chats = ['-1001560221019', '-1001706459960']

_idOwner = [1386657498]
_nameOwner = ['Владислав']
_groupsOwner = ['Admin']

_admin = ['AddUser', 'Send']
_user = ['Send']

_rights = {'Admin':_admin, 'User':_user}

_users = {'id':_idOwner, 'name': _nameOwner, 'groups': _groupsOwner}

_currentUserInd = ''

def GetUsers():
    return _users

def GetChats():
    return _chats

def AddChats(IdChat : str):
    _chats.append(IdChat)

def AddUser(id, name, groups):
    newUser = {'id':id, 'name': name, 'groups': groups}
    _users.update([newUser])

def _CkeckUserInDb(idUser: str):
    global _currentUserInd
    if idUser in _users.get('id'):
        _currentUserInd = _users.get('id').index(idUser)
        return True
    return False

def CheckUserRightsIsAddUser(idUser: str):
    global _currentUserInd
    if _CkeckUserInDb(idUser):
        if 'AddUser' in _rights.get(_users.get('groups')[_currentUserInd]):
            return True
        return False
