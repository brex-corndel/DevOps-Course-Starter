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
            
      if len(self.done) < 5:
            return done_list
      else:
            return done_list[:4]

# show_all_done_items?
# recent_done_items?
# older_done_items?