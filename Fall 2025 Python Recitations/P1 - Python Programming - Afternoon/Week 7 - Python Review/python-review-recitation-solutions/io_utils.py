import datetime

def get_integer_input(prompt, min_val=1, max_val=float('inf')):
    while True:
        try:
            choice = input(prompt).strip()
            if not choice:
                return None  # None if you just press enter 
            val = int(choice)
            if min_val <= val <= max_val:
                return val
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_date_input(prompt):
    while True:
        date_str = input(prompt).strip()
        if not date_str:
            return None
        try:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-12-31).")

def write_todo_list(file_path, todos):
    with open(file_path, 'w') as f:
        f.write("To Do:\n")
        for item in todos:
            date_str = item['date'].strftime('%Y-%m-%d')
            status = 'x' if item['completed'] else 'o'
            f.write(f"{status} {date_str}: {item['task']}\n")

def read_todo_list(file_path):
    todos = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines or lines[0].strip() != "To Do:":
            raise ValueError("Invalid file format. 'To Do:' not found.")

        for line in lines[1:]:
            try:
                status_date, task = line.split(':')
                task = task.strip()
                
                parts = status_date.strip().split(' ')
                status_char = parts[0]
                date_str = parts[1]

                date_obj = datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
                completed = True if status_char == 'x' else False

                todos.append({
                    'task': task.strip(),
                    'date': date_obj,
                    'completed': completed
                })
            except (ValueError, IndexError):
                raise ValueError(f"Invalid line format: {line}")
    return todos

if __name__ == '__main__':    
    # example items
    todo_items_to_write = [
        {'task': 'Finish the report', 'date': datetime.date(2025, 10, 5), 'completed': False},
        {'task': 'Buy groceries', 'date': datetime.date(2025, 10, 4), 'completed': True},
        {'task': 'Call a friend', 'date': datetime.date(2025, 10, 5), 'completed': True}
    ]

    file_name = 'my_todo_list.txt'
    
    write_todo_list(file_name, todo_items_to_write)
    print(f"To-do list written to {file_name}")

    read_items = read_todo_list(file_name)
    print("\nTo-do list read from file:")
    for item in read_items:
        print(item)