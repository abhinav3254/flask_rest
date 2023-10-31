from flask import Flask, request, jsonify
import dbconnection
from datetime import datetime

app = Flask(__name__)


class Todo:
    def __init__(self, title, description, completed=False, due_date=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.due_date = due_date


# Sample list to store todos
todos = []


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/todos", methods=["GET"])
def get_todos():
    todos = dbconnection.get_todos_from_db()
    formatted_todos = [
        {
            "id": todo[0],
            "title": todo[1],
            "description": todo[2],
            "completed": todo[3],
            "due_date": todo[4],
        }
        for todo in todos
    ]
    return jsonify({"todos": formatted_todos})


@app.route("/add_todo", methods=["POST"])
def add_todo():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)
    due_date = data.get("due_date")

    new_todo = Todo(title, description, completed, due_date)
    dbconnection.add_todo_to_db(new_todo)
    return (
        jsonify({"message": "Todo added successfully", "todo": new_todo.__dict__}),
        201,
    )


# method to update a todo
@app.route("/update_todo/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    completed = data.get("completed", False)
    due_date = data.get("due_date")

    updated_todo = Todo(title, description, completed, due_date)
    dbconnection.update_todo_by_id(todo_id, updated_todo)

    return (
        jsonify({"message": f"Todo with ID {todo_id} updated successfully"}),
        200,
    )


# method to delete a todo
@app.route("/delete_todo/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    dbconnection.delete_todo_by_id(todo_id)

    return (
        jsonify({"message": f"Todo with ID {todo_id} deleted successfully"}),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
