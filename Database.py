import sqlite3

SQL = sqlite3.connect('users.db')
c = SQL.cursor()


def CreateDB():
    c.execute(
        'CREATE TABLE IF NOT EXISTS Users'
        '(id int NOT NULL PRIMARY KEY, Moirail int DEFAULT 0,'
        ' Seen TEXT DEFAULT 0,'
        ' LastMessage TEXT DEFAULT 0)')
    c.execute('CREATE TABLE IF NOT EXISTS Settings'
              '(Name TEXT NOT NULL PRIMARY KEY, Value TEXT)')


def QueryID(condition):
    return(QueryModular(condition, "moirail"))


def QuerySetting(condition):
    return(QueryModular(condition, "setting"))


def QueryModular(condition, m):
    selection = [condition]  # too scared to remove this
    if m == "moirail":
        c.execute('SELECT Moirail FROM Users WHERE id = ?', selection)
    elif m == "setting":
        c.execute('SELECT Value FROM Settings WHERE Name = ?', selection)
    return(c.fetchone())


def update(Set: str, Condition: str, Table: str = "Users"):
    # This should not be exposed to the user
    c.execute(f'''UPDATE {Table}
                  Set {Set}
                  Where {Condition}''')


CreateDB()
