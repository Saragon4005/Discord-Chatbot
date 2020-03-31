import sqlite3
from Database import c, SQL
# from subprocess import call
# call()

for col in ["Seen", "LastMessage"]:
    try:
        c.execute(f'''ALTER TABLE Users
        ADD {col} TIMESTAMP;''')
    except sqlite3.OperationalError:
        pass


SQL.commit()
