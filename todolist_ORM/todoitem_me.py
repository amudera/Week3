import sqlite3


class ToDoItem:
    dbpath = ""
    tablename = "todoitems"

    def __init__(self,**kwargs):
         #use kwargs if your table name is constantly changing, kwargs lets you take in any column value pairs
         self.pk = kwargs.get("pk")
         self.title = kwargs.get("title")
         self.description = kwargs.get("description")
         self.complete = kwargs.get("complete")
        
    def save(self):
        if self.pk is None: #if pk doesnt exist, insert or update data
            self.insert()
        else:
            self.update()

    def insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """INSERT INTO {} (title,description,complete) VALUES(?,?,?);""".format(self.tablename)
            values = (self.title, self.description, self.complete)
            curs.execute(SQL,values)
            pk = curs.lastrowid #this just put the id of the last row it interacted with
            self.pk = pk #or could say self.pk = curs.lastrowid


    def update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
            SQL = """UPDATE {} SET title=?,description=?,complete=? WHERE pk=?;""".format(self.tablename)
            values = (self.title, self.description, self.complete,self.pk)
            curs.execute(SQL,values)
    
    def delete(self):
        if not self.pk:
            raise KeyError(self.__repr__() + " is not a row in " + self.tablename)
        with sqlite3.connect(self.dbpath) as conn:
            curs = conn.cursor()
        SQL = """DELETE FROM {} WHERE pk=?;""".format(self.tablename)
        curs.execute(SQL, (self.pk,))
  

    @classmethod
    def all(cls,complete=None): #select all, if used True it would select all where complete = True only
        if complete is None: #if none are complete
            SQL = """ SELECT * FROM {};""".format(cls.tablename)
        elif bool(complete) is True:
            SQL = """SELECT * FROM {} WHERE complete=1;""".format(cls.tablename)
        elif bool(complete) is False:
                SQL = """SELECT * FROM {} WHERE complete=1;""".format(cls.tablename)
        
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
            curs.execute(SQL)
            rows = curs.fetchall()
            return [cls(***row) for row in rows] # lets you manipualte rows like a dictionary
            #this returns a list of objects that are of type ToDoItem that can be fed into the init method
    
    @classmethod
    def one_from_pk(cls,pk):
        SQL = """SELECT * FROM {} WHERE pk=?;""".format(cls.tablename)
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            curs = conn.cursor()
           
            curs.execute(SQL,(pk,)) #class method so there is no self, no instance attributes yet
            rows = curs.fetchone()
            return cls(***row) #creating one instance
    
    
    def __repr__(self):
        pattern = "<ToDoItem: title={} pk={}>"
        return pattern.format(self.title,self.pk)


