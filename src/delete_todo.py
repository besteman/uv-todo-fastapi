import csv
import os
from typing import List

def delete_todo(todo_id: str) -> bool:
    """
    Deletes a todo item from the CSV file by ID.

    Parameters:
    todo_id (str): The ID of the todo item to delete.

    Returns:
    bool: True if deletion was successful, False if ID not found.
    """
    csv_file = "data/todos.csv"

    # Check if file exists
    if not os.path.exists(csv_file):
        print("No todos found. Create some todos first!")
        return False

    # Read all rows from CSV
    rows: List[List[str]] = []
    with open(csv_file, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check if file has content
    if len(rows) <= 1:  # Only header or empty
        print("No todos found. Create some todos first!")
        return False

    # Find and remove the todo with matching ID
    todo_found = False
    deleted_todo = ""
    updated_rows: List[List[str]] = []

    for row in rows:
        if len(row) >= 2 and row[0] == todo_id:
            deleted_todo = row[1]
            todo_found = True
            print(f"Deleted todo ID {todo_id}: {deleted_todo}")
        else:
            # Keep all rows except the one to delete
            updated_rows.append(row)

    if not todo_found:
        print(f"Todo with ID {todo_id} does not exist!")
        return False

    # Write updated data back to CSV
    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    return True
