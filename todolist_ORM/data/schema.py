import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'todo.db')

def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()

        SQL = "DROP TABLE IF EXISTS todoitems;"
        cur.execute(SQL)

        SQL = """ CREATE TABLE todoitems (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            adj_close FLOAT,
            volume INTEGER
        ); """
        cur.execute(SQL)


if __name__ == "__main__":
    schema()