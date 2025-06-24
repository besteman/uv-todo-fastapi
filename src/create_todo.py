import csv
import os

def create_todo(todo_item: str) -> str:
    """
    Adds a new todo item to the todo list.

    Parameters:
    todo_item (str): The todo item to be added.

    Returns:
    str: The created todo item with ID.
    """
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # CSV file path
    csv_file = "data/todos.csv"

    # Determine the next ID
    if os.path.exists(csv_file):
        # Read existing CSV to get the last ID
        with open(csv_file, "r", newline="") as file:
            reader = csv.reader(file)
            rows = list(reader)

            if len(rows) <= 1:  # Only header or empty file
                todo_id = 1
            else:
                # Get the last row and extract the ID
                last_row = rows[-1]
                if len(last_row) > 0:
                    try:
                        last_id = int(last_row[0])
                        todo_id = last_id + 1
                    except ValueError:
                        # If last ID is not a valid number, start from 1
                        todo_id = 1
                else:
                    todo_id = 1
    else:
        # File doesn't exist, start with ID 1
        todo_id = 1

    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(csv_file)

    # Write to CSV file
    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)

        # Write header if file is new
        if not file_exists:
            writer.writerow(["id", "todo"])

        # Write the todo item
        writer.writerow([todo_id, todo_item])

    print(f"Creating todo item: {todo_item} (ID: {todo_id})")
    return f"ID: {todo_id}, Todo: {todo_item}"
