from unittest import TestCase
from .todoitem import TodoItem

class TestToDo(TestCase):

    def testinsert(self):
        x = TodoItem()
        values = ("Buy cereal","Fruitloops",0)
        x._insert(values)
        x.save()
        x.value_from_table("title","Buy cereal")

        self.assertEqual(x.value_from_table,"Buy cereal","New pk inserted and saved")
    
    def testupdate(self):
        x = TodoItem()
        title = "Buy Milk"
        new_value = "Buy 2x Milk"
        x._update(title,new_value)
        x.save
        x.value_from_table("title","Buy 2x Milk")

        self.assertEqual(x.value_from_table,"Buy 2x Milk",PK updated and saved")
    
    def testdelete(self):
        x = TodoItem()
        del_value = "Buy cereal"
        pk = 2
        x.delete(del_val,pk)
        self.assertNotIn(self.tablename,pk,"pk deleted")
        
    