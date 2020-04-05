import sqlite3

SQL = sqlite3.connect('users.db')
c = SQL.cursor()


def CreateDB():
    c.execute(
        'CREATE TABLE IF NOT EXISTS Users'
        '(id int NOT NULL PRIMARY KEY, Moirail int,'
        ' Seen TIMESTAMP, LastMessage, TIMESTAMP)')
    c.execute('CREATE TABLE IF NOT EXISTS Settings'
              '(Name TEXT NOT NULL PRIMARY KEY, Value TEXT)')


def QueryID(condition):
    return(QueryModular(condition, "moirail"))


def QuerySetting(condition):
    return(QueryModular(condition, "setting"))


def QueryModular(condition, s):
    selection = [condition]
    if s == "moirail":
        c.execute('SELECT Moirail FROM Users WHERE id = ?', selection)
    elif s == "setting":
        c.execute('SELECT Value FROM Settings WHERE Name = ?', selection)
    return(c.fetchone())


def update(Set: str, Condition: str):
    # This should not be exposed to the user
    c.execute(f'''UPDATE Users
                 Set {Set}
                 Where {Condition}''')


CreateDB()
