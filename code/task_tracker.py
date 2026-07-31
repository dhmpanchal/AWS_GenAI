"""CLI Task Tracker.

A command-line application to manage tasks with priority levels.
Tasks are held in memory for the duration of the session.
"""


class Task:
    """Represents a single task with a name and priority."""

    def __init__(self, name, priority):
        """
        Args:
            name (str): Task name.
            priority (int|str): Priority level between 1 and 5.
        """
        self.name = name
        self.priority = int(priority)

    def __str__(self):
        """Return a human-readable string representation of the task."""
        return f"[Priority {self.priority}] {self.name}"

class TaskManager:
    """Manages a collection of Task objects."""

    def __init__(self):
        """Initialize with an empty task list."""
        self.tasks = []

    def add_task(self, name, priority):
        """
        Create and add a task, keeping the list sorted by priority ascending.

        Args:
            name (str): Task name.
            priority (int|str): Priority level between 1 and 5.
        """
        task = Task(name, priority)
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x.priority)

    def list_tasks(self):
        """Print all tasks to stdout. Prints a message if no tasks exist."""
        if not self.tasks:
            print("No tasks found.")
        for i, task in enumerate(self.tasks):
            print(f"{i + 1}. {task}")

    def remove_task(self, index):
        """
        Remove a task by its zero-based index.

        Args:
            index (int): Zero-based position of the task to remove.

        Raises:
            IndexError: If the index is out of range or negative.
        """
        if index < 0 or index >= len(self.tasks):
            raise IndexError("Task index out of range.")
        self.tasks.pop(index)

def print_menu():
    print("\nTask Tracker")
    print("1. Add task")
    print("2. List tasks")
    print("3. Remove task")
    print("4. Exit")

def main():
    manager = TaskManager()
    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter task name: ").strip()
            if not name:
                print("Task name cannot be empty.")
                continue
            priority = input("Enter priority (1-5): ")
            try:
                if not (1 <= int(priority) <= 5):
                    raise ValueError
                manager.add_task(name, priority)
                print("Task added.")
            except ValueError:
                print("Invalid priority. Please enter an integer between 1 and 5.")

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            manager.list_tasks()
            try:
                index = int(input("Enter task number to remove: ")) - 1
                manager.remove_task(index)
                print("Task removed.")
            except (ValueError, IndexError):
                print("Invalid task number.")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()