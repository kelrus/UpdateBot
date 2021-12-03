import sqlite3 as sq

def SqlStart():
    global base, cur
    base = sq.connect('updatebot.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, name TEXT, rights TEXT)')
    base.commit()

async def SqlAddUser(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO users VALUES(?,?,?)', tuple(data.values()))
        base.commit()
