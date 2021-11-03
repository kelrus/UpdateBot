import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect('updatebot.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS users(id TEXT, name TEXT, groups TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy as data:
        cur.execute('INSERT INTO users VALUES(?,?,?)', tuple(data.values()))
        base.commit()