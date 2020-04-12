from Database import c, SQL
# from subprocess import call
# call()

c.executescript("""
BEGIN TRANSACTION;
ALTER TABLE Users RENAME TO _Users_old;

CREATE TABLE Users
(id int NOT NULL PRIMARY KEY, Moirail int DEFAULT 0,
Seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
LastMessage TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

INSERT INTO Users (id, Moirail)
SELECT id, Moirail
FROM _Users_old;
COMMIT;""")


SQL.commit()
