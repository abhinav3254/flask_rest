from flask import Flask, request, jsonify
import test

app = Flask(__name__)

tasks = [1, 2, 3, 4, 5]


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return {"tasks": tasks}


@app.route("/test", methods=["GET"])
def get_tasks1():
    return test.getNewTask()


@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = data.get("task")
    tasks.append(new_task)
    return jsonify({"message": "Task added successfully"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
