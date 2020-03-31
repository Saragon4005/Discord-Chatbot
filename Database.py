import sqlite3

SQL = sqlite3.connect('users.db')
c = SQL.cursor()


def CreateDB():
    c.execute(
        'CREATE TABLE IF NOT EXISTS Users'
        '(id int NOT NULL PRIMARY KEY, Moirail int,'
        ' Seen TIMESTAMP, LastMessage, TIMESTAMP)')


def QueryID(condition):
    id = [condition]
    c.execute(''' SELECT Moirail FROM Users WHERE id = ? ''', id)
    return(c.fetchone())


def update(Set: str, Condition: str):
    # This should not be exposed to the user
    c.execute(f'''UPDATE Users
                 Set {Set}
                 Where {Condition}''')


CreateDB()
