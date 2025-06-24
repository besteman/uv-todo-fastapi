import csv
import os

def update_todo(todo_id: str, new_todo: str) -> bool:
    """
    Updates a todo item in the CSV file by ID.

    Parameters:
    todo_id (str): The ID of the todo item to update.
    new_todo (str): The new todo item text.

    Returns:
    bool: True if update was successful, False if ID not found.
    """
    csv_file = "data/todos.csv"

    # Check if file exists
    if not os.path.exists(csv_file):
        print("No todos found. Create some todos first!")
        return False

    # Read all rows from CSV
    rows = []
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if file has content
    if len(rows) <= 1:  # Only header or empty
        print("No todos found. Create some todos first!")
        return False

    # Find and update the todo with matching ID
    todo_found = False
    for i, row in enumerate(rows):
        if len(row) >= 2 and row[0] == todo_id:
            old_todo = row[1]
            rows[i][1] = new_todo
            todo_found = True
            print(f"Updated todo ID {todo_id}:")
            print(f"  Old: {old_todo}")
            print(f"  New: {new_todo}")
            break

    if not todo_found:
        print(f"Todo with ID {todo_id} does not exist!")
        return False

    # Write updated data back to CSV
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    return True
