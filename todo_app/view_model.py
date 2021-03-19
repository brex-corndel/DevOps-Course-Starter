from datetime import datetime, date

# now = datetime.now()

class ViewModel:
   def __init__(self, items):
        self._items = items

   @property
   def items(self): 
      return self._items

   @property
   def todo(self): 
      todo_list=[]
      for item in self._items:
          if item.status == "To Do":
            todo_list.append(item)
      return todo_list

   @property
   def doing(self): 
      doing_list=[]
      for item in self._items:
          if item.status == "Doing":
            doing_list.append(item)
      return doing_list

   @property
   def done(self): 
      done_list=[]
      for item in self._items:
          if item.status == "Done":
            done_list.append(item)
      return done_list

   @property
   def show_all_done_items(self):
      if len(self.done) < 5:
         return True
      else:
         return False
      
   @property
   def recent_done_items(self):
      done_today_list=[]
      for item in self._items:
          if item.status == "Done" and item.updated_time.date() == date.today():
            done_today_list.append(item)
      return done_today_list 

   @property
   def older_done_items(self):
      done_older_list=[]
      for item in self._items:
          if item.status == "Done" and item.updated_time.date() < date.today():
            done_older_list.append(item)
      return done_older_list 