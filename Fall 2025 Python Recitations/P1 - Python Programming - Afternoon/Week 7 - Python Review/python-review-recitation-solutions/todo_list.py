import datetime
from io_utils import read_todo_list, write_todo_list

class Todo:
    """
    Represents a single To-Do item. Stores task name, date, and completion status.
    """
    def __init__(self, task, date, completed=False):
        self.set_task(task)
        self.set_date(date)
        self.set_completed(completed)

    def get_task(self):
        return self._task

    def get_date(self):
        return self._date

    def is_completed(self):
        return self._completed

    def set_task(self, new_task):
        self._task = new_task

    def set_date(self, new_date):
        if not isinstance(new_date, datetime.date):
            raise TypeError("Date must be a datetime.date object.")
        self._date = new_date

    def set_completed(self, status):
        self._completed = status

    def toggle_completion(self):
        self._completed = not self._completed

    def to_dict(self):
        """Converts the Todo object to dictionary format."""
        return {
            'task': self.get_task(),
            'date': self.get_date(),
            'completed': self.is_completed()
        }

    def __str__(self):
        status_char = '+' if self.is_completed() else '-'
        date_str = self.get_date().strftime('%Y-%m-%d')
        return f"[{status_char}] {date_str}: {self.get_task()}"

class TodoList:
    """
    Manages a collection of Todo objects for a specific list.
    """
    def __init__(self, name, items=[]):
        self._name = name
        self._items = items

    def get_name(self):
        return self._name

    def get_items(self):
        return self._items
    
    def set_name(self, new_name):
        self._name = new_name

    def set_items(self, new_items):
        self._items = new_items

    def add_task(self, task_name, date):
        new_todo = Todo(task=task_name, date=date)
        self._items.append(new_todo)

    def remove_task(self, index):
        if 0 <= index < len(self.get_items()):
            self._items.pop(index)
        else:
            raise IndexError("Index out of range.")

    def mark_complete(self, index, status=True):
        if 0 <= index < len(self.get_items()):
            self.get_items()[index].set_completed(status)
        else:
            raise IndexError("Index out of range.")

    def save_to_file(self, file_path):
        dict_list = []
        for item in self.get_items():
            dict_list.append(item.to_dict())
        write_todo_list(file_path, dict_list)

    def load_from_file(self, file_path):
        dict_list = read_todo_list(file_path)
        items = []
        for d in dict_list:
            new_todo = Todo(d['task'], d['date'], d['completed'])
            items.append(new_todo)
        self.set_items(items)

    def __str__(self):
        to_return = f"--- {self.get_name()}'s To-Do List ({len(self.get_items())} Tasks) ---\n"
        if not self.get_items():
            return to_return + "The list is currently empty."

        for i, item in enumerate(self.get_items()):
            status_char = '+' if item.is_completed() else '-'
            date_str = item.get_date().strftime('%Y-%m-%d')
            to_return += f"[{i+1}] [{status_char}] {date_str}: {item.get_task()}\n"

        return to_return

# example use
if __name__ == '__main__':
    FILE_PATH = "my_daily_todo.txt"
    
    # 1. Create a new TodoList
    my_list = TodoList("John")
    
    # 2. Add tasks
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    my_list.add_task("Review project roadmap", today)
    my_list.add_task("Schedule dentist appointment", today)
    my_list.add_task("Draft email to the team", tomorrow)
    
    # 3. Mark the first task as complete (index 0)
    my_list.mark_complete(0, True)
    
    # 4. Display the current list
    print("\n--- Current List State ---")
    print(my_list)
    
    # 5. Save the list to a file
    my_list.save_to_file(FILE_PATH)
    
    # 6. Load the list back from the file into a new object
    loaded_list = TodoList("Can")
    loaded_list.load_from_file(FILE_PATH)
    
    # 7. Display the loaded list
    print("\n--- Loaded List State ---")
    print(loaded_list)
    
    # 8. Mark a task in the loaded list as complete by index (index 1 is 'Schedule dentist appointment')
    loaded_list.mark_complete(1)
    
    # 9. Toggle the first task's status (it was complete, now it's incomplete)
    loaded_list.mark_complete(0, False) 
    
    print("\n--- Loaded List State After Updates ---")
    print(loaded_list)
