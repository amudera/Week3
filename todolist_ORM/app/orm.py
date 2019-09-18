import sqlite3


class ORM:
    dbpath = ""
    tablename = ""
    fields = []

    def __init__(self, **kwargs):
        raise NotImplementedError


    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()

            fieldlist = ", ".join(self.fields) #returns a string not a tuple
        #create string that goes into our insert statement
            qmarks = ", ".join(["?" for _ in self.fields])
        #create correct number of ?s for values
            SQL = """ INSERT INTO {} ({})
            VALUES ({}); """.format(self.tablename,fieldlist,qmarks)
            values = [getattr(self,field) for field in self.fields] 
            #as fields are ordered the same way as attributes, it will go back to init
            #function and run through self.title, self.description and self.complete in
            #that exact order
            curs.execute(SQL, values)
            pk = curs.lastrowid
            self.pk = pk

# TODO: finish method like the above
    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            set_equals = ", ".join(['{}=?'.format(field) for field in self.fields])
            SQL = """ UPDATE {} SET {}
            WHERE pk = ?; """.format(self.tablename)
            values = [getattr(self,field) for field in self.fields] + [self.pk]
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
    def one_from_where_clause(cls, where_clause="",values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename)
        with sqlite3.connect(cls.dbpath) as conn:
            #sets our return (fetched) data to behave like a dictionary
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()

            curs.execute(SQL, values)
            row = curs.fetchone()
            if not row:
                return None
            return cls(**row)
            #if the fetch clause returns Nothing, this will just return none
    
    @classmethod
    def all_from_where_clause(cls, where_clause="",values=tuple()):
        SQL = "SELECT * FROM {} {};".format(cls.tablename)
        with sqlite3.connect(cls.dbpath) as conn:
            #sets our return (fetched) data to behave like a dictionary
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()

            curs.execute(SQL, values)
            rows = curs.fetchall()
            return [cls(**row) for row in rows]
    

    def __repr__(self):
        pattern = "<{} ORM: pk={}>"
        return pattern.format(self.tablename, self.pk)
