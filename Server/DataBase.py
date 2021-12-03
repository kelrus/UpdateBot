import sqlite3 as sq

def SqlStart():
    global base, cur
    base = sq.connect('updatebot.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS users(id INT PRIMARY KEY, name TEXT, rights TEXT)')
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS chats(id TEXT INT PRIMARY KEY)')
    base.commit()

async def SqlAddUser(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users VALUES(?,?,?)', tuple(data.values()))
        base.commit()

async def SqlAddChats(id):
    cur.execute('INSERT INTO chats VALUES(?)', tuple(id))
    base.commit()

def SqlGetUsers():
    return cur.execute("SELECT id FROM users").fetchall()

def SqlGetChats():
    return cur.execute("SELECT id FROM chats").fetchall()

def SqlSearchRightsById(id):
    return cur.execute('SELECT rights FROM users WHERE id == ?', (str(id),)).fetchall()
