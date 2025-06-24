# Todo CLI App with uv

A simple command-line todo management application built to test and explore the new **uv** Python package manager.

## 📋 About This Project

This project was created specifically to experiment with and evaluate [uv](https://github.com/astral-sh/uv), the new ultra-fast Python package manager and project manager. The todo app serves as a practical testing ground for uv's features including:

- Fast dependency resolution and installation
- Virtual environment management
- Project structure and configuration
- Test execution and development workflows

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) installed

### Installation
```bash
git clone <your-repo-url>
cd uv-todo-fastapi
uv sync  # Install dependencies and create virtual environment
```

## 🖥️ Running the Todo App

The todo app is a command-line interface that supports four main operations:

### Basic Usage

```bash
# Run with uv (from project root)
uv run src/main.py create "New todo item"
uv run src/main.py read
uv run src/main.py update 1 "Updated todo"
uv run src/main.py delete 1
```

## 📝 Features

- ✅ **Create** new todo items with auto-incrementing IDs
- ✅ **Read** and display all todos in a formatted table
- ✅ **Update** existing todos by ID
- ✅ **Delete** todos by ID
- ✅ **Persistent storage** using CSV files
- ✅ **Error handling** for missing files and invalid IDs
- ✅ **Pretty output** with table formatting and truncation

## 🏗️ Project Structure

```
uv-todo-fastapi/
├── src/
│   ├── main.py           # CLI entry point
│   ├── create_todo.py    # Create todo functionality
│   ├── read_todos.py     # Read/display todos
│   ├── update_todo.py    # Update todo functionality
│   └── delete_todo.py    # Delete todo functionality
├── tests/
│   ├── test_todo_app.py  # Comprehensive test suite
│   └── README.md         # Testing documentation
├── data/
│   └── todos.csv         # CSV storage (created automatically)
├── pyproject.toml        # Project configuration
├── test.sh              # Test runner script
├── Makefile             # Build and test commands
└── README.md            # This file
```

## 🧪 Testing with uv

This project includes a comprehensive test suite to validate uv's testing capabilities:

### Run Tests

```bash
uvx pytest
```

### Test Coverage
- ✅ 16 comprehensive tests
- ✅ All CRUD operations
- ✅ Error handling scenarios
- ✅ File system operations
- ✅ Integration testing

## 🔧 uv Package Manager Experience

### What We Tested

**✅ Fast Installation**: uv's dependency resolution is noticeably faster than pip
**✅ Project Management**: `pyproject.toml` configuration works seamlessly
**✅ Virtual Environments**: Automatic venv creation and management
**✅ Test Execution**: Running pytest with `uv run` works perfectly
**✅ Isolation**: `--isolated` flag ensures clean test environments

### uv Commands Used
```bash
uv init                # Initialize project
uv add pytest ruff     # Add dependencies
uv sync                # Install all dependencies
uvx pytest             # Run tests
```

### Performance Notes
- **Dependency resolution**: ~10x faster than pip
- **Installation**: Significantly quicker cold starts
- **Project setup**: Streamlined configuration

## 🛠️ Dependencies

- **pytest**: Testing framework
- **ruff**: Fast Python linter (also built by Astral)

## 📊 Data Storage

Todos are stored in `data/todos.csv` with the following structure:
```csv
id,todo
1,Buy groceries
2,Walk the dog
3,Do laundry
```

## 🎯 Example Session

```bash
$ cd src
$ uv run src/main.py create "Learn about uv package manager"
Creating todo item: Learn about uv package manager (ID: 1)

$ uv run src/main.py create "Test uv with a real project"
Creating todo item: Test uv with a real project (ID: 2)

$ uv run src/main.py read

==================================================
               TODO LIST
==================================================
ID    | TODO ITEM
--------------------------------------------------
1     | Learn about uv package manager
2     | Test uv with a real project
==================================================
Total todos: 2

$ uv run src/main.py update 1 "Master uv package manager"
Updated todo ID 1:
  Old: Learn about uv package manager
  New: Master uv package manager

$ uv run src/main.py delete 2
Deleted todo ID 2: Test uv with a real project
```
