import sqlite3


class TodoItem:
    dbpath = ""
    tablename = "todoitems"

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.complete = kwargs.get("complete")

    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """ INSERT INTO {} (title, descrition, complete)
            VALUES (?, ?, ?); """.format(self.tablename)
            values = (self.title, self.description, self.complete)
            curs.execute(SQL, values)
            pk = curs.lastrowid
            self.pk = pk

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """ UPDATE {} SET title=?, descrition=?, complete=?
            WHERE pk = ?; """.format(self.tablename)
            values = (self.title, self.description, self.complete, self.pk)
            curs.execute(SQL, values)

    def delete(self):
        if not self.pk:
            raise KeyError(self.__repr__() + " is not a row in " + 
                            self.tablename)
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """ DELETE FROM {} WHERE pk = ?; """.format(self.tablename)
            curs.execute(SQL, (self.pk,))

    @classmethod
    def all(cls, complete=None):
        if complete is None:
            SQL = "SELECT * FROM {};".format(cls.tablename)
        elif bool(complete) is True:
            SQL = "SELECT * FROM {} WHERE complete = 1;".format(cls.tablename)
        elif bool(complete) is False:
            SQL = "SELECT * FROM {} WHERE complete = 0;".format(cls.tablename)

        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()

            curs.execute(SQL)
            rows = curs.fetchall()
            return [cls(**row) for row in rows]

    @classmethod
    def one_from_pk(cls, pk):
        SQL = "SELECT * FROM {} WHERE pk = ?;".format(cls.tablename)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()

            curs.execute(SQL, (pk,))
            row = curs.fetchone()
            return cls(**row)
    
    # @classmethod
    # def value_from_table(cls,values):
    #     column_header = input("What column you trying to query?")
    #     column_value = input("What column value are you trying to query?")
    #     SQL = "SELECT * FROM {} WHERE ? = ?;".format(cls.tablename)
    #     values = (column_header,column_value)

    #     with sqlite3.connect(cls.dbpath) as conn:
    #         conn.row_factory = sqlite3.Row
    #         curs = conn.cursor()

    #         curs.execute(SQL,(values,)
    #         _row = curs.fetchone()
    #         return cls(**row)

    def __repr__(self):
        pattern = "<TodoItem: title={} pk={}>"
        return pattern.format(self.title, self.pk)
