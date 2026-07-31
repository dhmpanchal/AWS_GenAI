# Task Tracker

A task management app with a CLI interface and a Flask web interface. Tasks are persisted to a local `tasks.json` file and sorted by priority in ascending order.

---

## Project Structure

```
code/
├── app.py                  # Flask backend (REST API)
├── task_tracker.py         # Original CLI app
├── requirements.txt        # Python dependencies
├── tasks.json              # Auto-generated task storage file
└── templates/
    └── index.html          # Web front-end
```

---

## Requirements

- Python 3.8+
- Flask 3.0+

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Web App

```bash
python app.py
```

Then open your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Running the CLI App

```bash
python task_tracker.py
```

---

## REST API Reference

### GET /tasks
Returns all tasks sorted by priority ascending.

**Response `200`**
```json
[
  { "name": "Fix bug", "priority": 1 },
  { "name": "Write docs", "priority": 3 }
]
```

---

### POST /tasks
Adds a new task.

**Request Body**
```json
{ "name": "Task name", "priority": 2 }
```

**Validation**
- `name` — required, non-empty string
- `priority` — integer between 1 and 5 (inclusive)

**Response `201`**
```json
{ "message": "Task added." }
```

**Response `400`**
```json
{ "error": "Task name cannot be empty." }
{ "error": "Priority must be an integer between 1 and 5." }
```

---

### DELETE /tasks/\<index\>
Removes a task by its zero-based index in the sorted list.

**Response `200`**
```json
{ "message": "Task removed." }
```

**Response `400`**
```json
{ "error": "Task index out of range." }
```

---

## Task Storage

Tasks are stored in `tasks.json` in the following format:

```json
[
  { "name": "Fix bug", "priority": 1 },
  { "name": "Write tests", "priority": 2 }
]
```

The file is created automatically on the first task addition and is always kept sorted by priority ascending.

---

## Priority Levels

| Value | Label |
|-------|-------|
| 1     | P1 — Highest |
| 2     | P2 |
| 3     | P3 — Default |
| 4     | P4 |
| 5     | P5 — Lowest |
