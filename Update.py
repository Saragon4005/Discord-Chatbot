from Database import c, SQL
import sqlite3

try:
    c.execute("DROP TABLE _Users_old")
except Exception:
    pass

c.executescript("""
BEGIN TRANSACTION;
ALTER TABLE Users RENAME TO _Users_old;

CREATE TABLE Users
(id int NOT NULL PRIMARY KEY, Moirail int DEFAULT 0,
Seen TEXT DEFAULT 0,
LastMessage TEXT DEFAULT 0);

INSERT INTO Users (id, Moirail)
SELECT id, Moirail
FROM _Users_old;
COMMIT;""")
try:
    c.execute("INSERT INTO Settings (Name, Value)"
              "Values('Blacklist', '693964315790934098,clo9d')")
except sqlite3.IntegrityError:
    print("Integrity Error")
try:
    c.execute("INSERT INTO Settings (Name, Value)"
              "Values('BlacklistToggle', 'False')")
except sqlite3.IntegrityError:
    print("Integrity Error")

SQL.commit()
