import sqlite3 as sq

def SqlStart():
    global base, cur
    base = sq.connect('updatebot.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, name TEXT, rights TEXT)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS chats(id INT PRIMARY KEY)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS message(time TEXT PRIMARY KEY, message TEXT)')
    base.commit()

async def SqlAddUser(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users VALUES(?,?,?)', tuple(data.values()))
        base.commit()

async def SqlDeleteUser(id):
    cur.execute('DELETE FROM users WHERE id == ?', (int(id),)).fetchall()
    base.commit()

def SqlAddMessage(message, time):
    cur.execute('INSERT INTO message VALUES(?,?)', (str(time), str(message),))
    base.commit()

def SqlDeleteMessage(time):
    cur.execute('DELETE FROM message WHERE time == ?', (time,)).fetchall()
    base.commit()

def SqlGetMessage():
    return cur.execute("SELECT * FROM message").fetchall()

def SqlAddChats(id):
    cur.execute('INSERT INTO chats VALUES(?)', (id,))
    base.commit()

def SqlDeleteChats(id):
    cur.execute('DELETE FROM chats WHERE id == ?', (int(id),)).fetchall()
    base.commit()


def SqlGetUsers():
    return cur.execute("SELECT id FROM users").fetchall()

def SqlGetUsersInfo():
    return cur.execute("SELECT * FROM users").fetchall()

def SqlGetChats():
    return cur.execute("SELECT id FROM chats").fetchall()

def SqlSearchRightsById(id):
    return cur.execute('SELECT rights FROM users WHERE id == ?', (str(id),)).fetchall()
