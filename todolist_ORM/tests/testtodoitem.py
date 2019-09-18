import unittest
import sqlite3
from ..data import schema, seed
from ..app.new_todoitem import TodoItem
import os

class TestToDoItem(unittest.TestCase):

    def setUp(self):
        #create test database and seed with a row of Data
        schema.schema(dbpath='test.db')
        seed.seed(dbpath='test.db')

    def testSelectOne(self):
        test = TodoItem.one_from_where_clause('WHERE pk=?',(3,))
        self.assertEqual(test.title,"Get Lunch","Title matches data")
    #this tests the init method

    def testAll(self):
        test = TodoItem.all()
        self.assertEqual(len(test),3,"all returns correct number of elements")
    #check the number of data lines in the test database and check that it equals 
    #what you put in
        test = TodoItem.all(complete=1)
        self.assertEqual(len(test),1,"all returns correct number of  completed elements")

        test = TodoItem.all(complete=0)
        self.assertEqual(len(test),1,"all returns correct number of  incompleted elements")

    def testrepr(self):
        #this is an instance method so need to reference instances
        test = TodoItem(pk=1,title="Test")
        self.assertEqual(test.__repr__(),"<TodoItem: title={} pk={}>","__repr__ gives correct output")

    def testSelectOne(self):
        test = TodoItem(pk=1,title="Get Lunch",description="Test")
        #this is an instance
        self.assertEqual(test.complete,None,"__init__ works correctly")
    #init sets missing attributes (complete) as None

    def tearDown(self):
        os.remove('data/test.db')

