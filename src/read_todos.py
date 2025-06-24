import csv
import os

def read_todos():
    """
    Reads and displays all todo items from the CSV file.
    """
    csv_file = "data/todos.csv"

    # Check if file exists
    if not os.path.exists(csv_file):
        print("No todos found. Create some todos first!")
        return

    # Read CSV file
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if file has content
    if len(rows) <= 1:  # Only header or empty
        print("No todos found. Create some todos first!")
        return

    # Display header
    print("\n" + "="*50)
    print("               TODO LIST")
    print("="*50)

    # Display todos in a table format
    print(f"{'ID':<5} | {'TODO ITEM':<40}")
    print("-" * 50)

    # Skip header row and display todos
    for row in rows[1:]:
        if len(row) >= 2:  # Make sure row has both id and todo
            todo_id = row[0]
            todo_item = row[1]
            # Truncate long todo items
            if len(todo_item) > 40:
                todo_item = todo_item[:37] + "..."
            print(f"{todo_id:<5} | {todo_item:<40}")

    print("="*50)
    print(f"Total todos: {len(rows) - 1}")
    print()
