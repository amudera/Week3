import sqlite3
import os

DIR = os.path.dirname(__file__)
DBPATH = os.path.join(DIR, 'todo.db')

def seed(dbname=DBPATH):
    with sqlite3.connect(dbname) as conn:
        cur = conn.cursor()
        SQL = """INSERT INTO todoitems (title, description, complete) VALUES (?, ?, ?)"""
        values = [("Pick up Milk","Half and Half",1),
                ("Call Mike","Regarding meeting",1),
                ("Do Laundry","Separate out colours",0),
                ]
    
        cur.executemany(SQL,(values))


if __name__ == "__main__":
    seed()