import os
import csv
import tempfile
import shutil
from typing import List, Any
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from create_todo import create_todo
from read_todos import read_todos
from update_todo import update_todo
from delete_todo import delete_todo


class TestTodoApp:

    def setup_method(self) -> None:
        """Setup method to create a temporary directory for each test"""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self) -> None:
        """Cleanup method to remove temporary directory after each test"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.test_dir)

    def create_test_csv(self, data: List[List[str]]) -> None:
        """Helper method to create a test CSV file"""
        os.makedirs("data", exist_ok=True)
        with open("data/todos.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def read_csv_content(self) -> List[List[str]]:
        """Helper method to read CSV content"""
        if not os.path.exists("data/todos.csv"):
            return []
        with open("data/todos.csv", "r", newline="") as file:
            reader = csv.reader(file)
            return list(reader)


class TestCreateTodo(TestTodoApp):

    def test_create_first_todo(self) -> None:
        """Test creating the first todo item"""
        result = create_todo("Buy groceries")

        # Check return value
        assert "ID: 1, Todo: Buy groceries" == result

        # Check CSV file was created with correct content
        content = self.read_csv_content()
        expected = [
            ["id", "todo"],
            ["1", "Buy groceries"]
        ]
        assert content == expected

    def test_create_multiple_todos(self) -> None:
        """Test creating multiple todo items with sequential IDs"""
        # Create first todo
        create_todo("Buy groceries")

        # Create second todo
        result = create_todo("Walk the dog")

        # Check return value
        assert "ID: 2, Todo: Walk the dog" == result

        # Check CSV content
        content = self.read_csv_content()
        expected = [
            ["id", "todo"],
            ["1", "Buy groceries"],
            ["2", "Walk the dog"]
        ]
        assert content == expected

    def test_create_todo_with_existing_csv(self) -> None:
        """Test creating todo when CSV already exists with data"""
        # Setup existing CSV
        existing_data = [
            ["id", "todo"],
            ["1", "Existing todo"],
            ["5", "Another todo"]
        ]
        self.create_test_csv(existing_data)

        # Create new todo
        result = create_todo("New todo")

        # Should use last ID (5) + 1 = 6
        assert "ID: 6, Todo: New todo" == result

        # Check CSV content
        content = self.read_csv_content()
        expected = existing_data + [["6", "New todo"]]
        assert content == expected

    def test_create_todo_creates_data_directory(self) -> None:
        """Test that data directory is created if it doesn't exist"""
        # Ensure data directory doesn't exist
        assert not os.path.exists("data")

        create_todo("Test todo")

        # Check data directory was created
        assert os.path.exists("data")
        assert os.path.exists("data/todos.csv")


class TestReadTodos(TestTodoApp):

    def test_read_todos_no_file(self, capsys: Any) -> None:
        """Test reading todos when no CSV file exists"""
        read_todos()

        captured = capsys.readouterr()
        assert "No todos found. Create some todos first!" in captured.out

    def test_read_todos_empty_file(self, capsys: Any) -> None:
        """Test reading todos when CSV file is empty or only has header"""
        self.create_test_csv([["id", "todo"]])

        read_todos()

        captured = capsys.readouterr()
        assert "No todos found. Create some todos first!" in captured.out

    def test_read_todos_with_data(self, capsys: Any) -> None:
        """Test reading todos when CSV file has data"""
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"],
            ["2", "Walk the dog"],
            ["3", "Do laundry"]
        ]
        self.create_test_csv(test_data)

        read_todos()

        captured = capsys.readouterr()
        output = captured.out

        # Check that output contains expected elements
        assert "TODO LIST" in output
        assert "Buy groceries" in output
        assert "Walk the dog" in output
        assert "Do laundry" in output
        assert "Total todos: 3" in output

    def test_read_todos_truncates_long_items(self, capsys: Any) -> None:
        """Test that long todo items are truncated in display"""
        long_todo = "This is a very long todo item that should be truncated when displayed"
        test_data = [
            ["id", "todo"],
            ["1", long_todo]
        ]
        self.create_test_csv(test_data)

        read_todos()

        captured = capsys.readouterr()
        output = captured.out

        # Should contain truncated version with "..."
        assert "This is a very long todo item that sh..." in output


class TestUpdateTodo(TestTodoApp):

    def test_update_existing_todo(self, capsys: Any) -> None:
        """Test updating an existing todo item"""
        # Setup test data
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"],
            ["2", "Walk the dog"]
        ]
        self.create_test_csv(test_data)

        # Update todo
        result = update_todo("1", "Buy organic groceries")

        # Check return value
        assert result is True

        # Check console output
        captured = capsys.readouterr()
        assert "Updated todo ID 1:" in captured.out
        assert "Old: Buy groceries" in captured.out
        assert "New: Buy organic groceries" in captured.out

        # Check CSV was updated
        content = self.read_csv_content()
        expected = [
            ["id", "todo"],
            ["1", "Buy organic groceries"],
            ["2", "Walk the dog"]
        ]
        assert content == expected

    def test_update_nonexistent_todo(self, capsys: Any) -> None:
        """Test updating a todo that doesn't exist"""
        # Setup test data
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"]
        ]
        self.create_test_csv(test_data)

        # Try to update non-existent todo
        result = update_todo("999", "New todo")

        # Check return value
        assert result is False

        # Check console output
        captured = capsys.readouterr()
        assert "Todo with ID 999 does not exist!" in captured.out

        # Check CSV was not changed
        content = self.read_csv_content()
        assert content == test_data

    def test_update_todo_no_file(self, capsys: Any) -> None:
        """Test updating todo when no CSV file exists"""
        result = update_todo("1", "New todo")

        assert result is False
        captured = capsys.readouterr()
        assert "No todos found. Create some todos first!" in captured.out


class TestDeleteTodo(TestTodoApp):

    def test_delete_existing_todo(self, capsys: Any) -> None:
        """Test deleting an existing todo item"""
        # Setup test data
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"],
            ["2", "Walk the dog"],
            ["3", "Do laundry"]
        ]
        self.create_test_csv(test_data)

        # Delete todo
        result = delete_todo("2")

        # Check return value
        assert result is True

        # Check console output
        captured = capsys.readouterr()
        assert "Deleted todo ID 2: Walk the dog" in captured.out

        # Check CSV was updated (todo 2 should be removed)
        content = self.read_csv_content()
        expected = [
            ["id", "todo"],
            ["1", "Buy groceries"],
            ["3", "Do laundry"]
        ]
        assert content == expected

    def test_delete_nonexistent_todo(self, capsys: Any) -> None:
        """Test deleting a todo that doesn't exist"""
        # Setup test data
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"]
        ]
        self.create_test_csv(test_data)

        # Try to delete non-existent todo
        result = delete_todo("999")

        # Check return value
        assert result is False

        # Check console output
        captured = capsys.readouterr()
        assert "Todo with ID 999 does not exist!" in captured.out

        # Check CSV was not changed
        content = self.read_csv_content()
        assert content == test_data

    def test_delete_todo_no_file(self, capsys: Any) -> None:
        """Test deleting todo when no CSV file exists"""
        result = delete_todo("1")

        assert result is False
        captured = capsys.readouterr()
        assert "No todos found. Create some todos first!" in captured.out

    def test_delete_last_todo(self, capsys: Any) -> None:
        """Test deleting the last remaining todo"""
        # Setup test data with only one todo
        test_data = [
            ["id", "todo"],
            ["1", "Buy groceries"]
        ]
        self.create_test_csv(test_data)

        # Delete the only todo
        result = delete_todo("1")

        # Check return value
        assert result is True

        # Check CSV only contains header
        content = self.read_csv_content()
        expected = [["id", "todo"]]
        assert content == expected


class TestIntegration(TestTodoApp):

    def test_full_workflow(self, capsys: Any) -> None:
        """Test a complete workflow: create, read, update, delete"""
        # Create some todos
        create_todo("Buy groceries")
        create_todo("Walk the dog")
        create_todo("Do laundry")

        # Read todos
        read_todos()
        captured = capsys.readouterr()
        assert "Total todos: 3" in captured.out

        # Update a todo
        update_todo("2", "Walk the dog for 30 minutes")

        # Delete a todo
        delete_todo("1")

        # Clear previous output
        capsys.readouterr()

        # Read todos again
        read_todos()
        captured = capsys.readouterr()
        assert "Total todos: 2" in captured.out
        assert "Walk the dog for 30 minutes" in captured.out
        assert "Do laundry" in captured.out
        assert "Buy groceries" not in captured.out
