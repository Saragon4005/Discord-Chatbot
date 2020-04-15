import sqlite3

SQL = sqlite3.connect('users.db')
c = SQL.cursor()


def CreateDB():
    '''
    Creates User and Setting databases
    '''
    c.execute(
        'CREATE TABLE IF NOT EXISTS Users'
        '(id int NOT NULL PRIMARY KEY, Moirail int DEFAULT 0,'
        ' Seen TEXT DEFAULT 0,'
        ' LastMessage TEXT DEFAULT 0)')
    c.execute('CREATE TABLE IF NOT EXISTS Settings'
              '(Name TEXT NOT NULL PRIMARY KEY, Value TEXT)')


def QueryMoirail(condition):
    """
    Outputs the Moirail value for the specified user
    """
    return(QueryModular(condition).moirail())


def QuerySetting(condition):
    """
    Outputs the value for the specified setting
    """
    return(QueryModular(condition).setting())


def QueryUser(condition):
    """
    Outputs a list for the user in Moirail, Seen, LastMessage order
    """
    return(QueryModular(condition).user())


class QueryModular():

    def __init__(self, condition):
        self.selection = [condition]  # too scared to remove this

    def moirail(self):
        c.execute('SELECT Moirail FROM Users WHERE id = ?', self.selection)
        return(c.fetchone())

    def setting(self):
        c.execute('SELECT Value FROM Settings WHERE Name = ?', self.selection)
        return(c.fetchone())

    def user(self):
        c.execute('SELECT Moirail, Seen, LastMessage '
                  'FROM Users WHERE id = ?', self.selection)
        return(c.fetchone())


def update(Set: str, Condition: str, Table: str = "Users"):
    # This should not be exposed to the user
    c.execute(f'''UPDATE {Table}
                  Set {Set}
                  Where {Condition}''')


CreateDB()
