"""Flask backend for the Task Tracker web app.

Provides a REST API to add, list, and remove tasks.
Tasks are persisted to a local tasks.json file and always
returned sorted by priority in ascending order.
"""
import json
import os
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    """Load tasks from tasks.json. Returns an empty list if the file does not exist."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Persist the task list to tasks.json."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


@app.route("/")
def index():
    """Serve the web front-end."""
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks as a JSON array, sorted by priority ascending."""
    return jsonify(load_tasks())


@app.route("/tasks", methods=["POST"])
def add_task():
    """
    Add a new task.

    Request JSON:
        name (str): Task name. Must be a non-empty string.
        priority (int): Priority level between 1 (highest) and 5 (lowest).

    Returns:
        201 with {message} on success.
        400 with {error} if validation fails.
    """
    data = request.get_json()
    name = data.get("name", "").strip()
    priority = data.get("priority")

    if not name:
        return jsonify({"error": "Task name cannot be empty."}), 400
    try:
        priority = int(priority)
        if not (1 <= priority <= 5):
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "Priority must be an integer between 1 and 5."}), 400

    tasks = load_tasks()
    tasks.append({"name": name, "priority": priority})
    tasks.sort(key=lambda x: x["priority"])
    save_tasks(tasks)
    return jsonify({"message": "Task added."}), 201


@app.route("/tasks/<int:index>", methods=["DELETE"])
def remove_task(index):
    """
    Remove a task by its zero-based index in the sorted task list.

    Args:
        index (int): Zero-based position of the task to remove.

    Returns:
        200 with {message} on success.
        400 with {error} if the index is out of range.
    """
    tasks = load_tasks()
    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Task index out of range."}), 400
    tasks.pop(index)
    save_tasks(tasks)
    return jsonify({"message": "Task removed."})


if __name__ == "__main__":
    app.run(debug=True)
