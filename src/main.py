from argparse import ArgumentParser
from create_todo import create_todo
# You'll need to import these modules when you create them
from read_todos import read_todos
from update_todo import update_todo
from delete_todo import delete_todo

def main():
    parser = ArgumentParser(description="Todo management CLI")
    parser.add_argument("action", choices=["create", "read", "update", "delete"],
                       help="Action to perform on todos")
    parser.add_argument("args", nargs="*", help="Additional arguments for the action")

    args = parser.parse_args()

    if args.action == "create":
        if len(args.args) < 1:
            print("Usage: create <todo_item>")
            return
        todo = args.args[0]
        create_todo(todo)
    elif args.action == "read":
        read_todos()
        # read_todo.main()
    elif args.action == "update":
        if len(args.args) < 2:
            print("Usage: update <todo_id> <new_todo>")
            return
        todo_id = args.args[0]
        new_todo = " ".join(args.args[1:])
        update_todo(todo_id, new_todo)
    elif args.action == "delete":
        if len(args.args) < 1:
            print("Usage: delete <todo_id>")
            return
        todo_id = args.args[0]
        delete_todo(todo_id)

if __name__ == "__main__":
    main()
