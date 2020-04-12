from Database import c, SQL
# from subprocess import call
# call()

c.executescript("""
BEGIN TRANSACTION;
DROP TABLE _Users_old;
ALTER TABLE Users RENAME TO _Users_old;

CREATE TABLE Users
(id int NOT NULL PRIMARY KEY, Moirail int DEFAULT 0,
Seen TEXT DEFAULT 0,
LastMessage TEXT DEFAULT 0);

INSERT INTO Users (id, Moirail)
SELECT id, Moirail
FROM _Users_old;
COMMIT;""")


SQL.commit()
