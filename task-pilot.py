#Any issues can be reported at github.com/pvk-96/to-do-CLI.
#Any suggestions are appreciated.
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# Load existing tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add a task
def add_task():
    description = input("Enter task description: ").strip()
    due_date = input("Enter due date (YYYY-MM-DD) [optional]: ").strip()
    priority = input("Enter priority (low/medium/high) [default: medium]: ").strip().lower() or "medium"
    task = {
        "description": description,
        "due_date": due_date or None,
        "priority": priority,
        "completed": False
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("Task added.")

# View all tasks
def view_tasks(filter_by=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        if filter_by == "completed" and not task["completed"]:
            continue
        if filter_by == "pending" and task["completed"]:
            continue
        if filter_by == "overdue":
            if not task["due_date"]:
                continue
            try:
                due = datetime.strptime(task["due_date"], "%Y-%m-%d")
                if due >= datetime.now():
                    continue
            except:
                continue
        status = "✓" if task["completed"] else "✗"
        print(f"[{i}] {status} {task['description']} (Due: {task['due_date'] or 'None'}, Priority: {task['priority']})")

# Mark task as complete
def mark_complete():
    view_tasks("pending")
    index = int(input("Enter task number to mark as complete: ")) - 1
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("Task marked as complete.")
    else:
        print("Invalid task number.")

# Delete task
def delete_task():
    view_tasks()
    index = int(input("Enter task number to delete: ")) - 1
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        del tasks[index]
        save_tasks(tasks)
        print("Task deleted.")
    else:
        print("Invalid task number.")

# Edit task
def edit_task():
    view_tasks()
    index = int(input("Enter task number to edit: ")) - 1
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        task = tasks[index]
        new_desc = input(f"New description [{task['description']}]: ").strip() or task['description']
        new_due = input(f"New due date (YYYY-MM-DD) [{task['due_date'] or 'None'}]: ").strip() or task['due_date']
        new_priority = input(f"New priority (low/medium/high) [{task['priority']}]: ").strip().lower() or task['priority']
        task.update({
            "description": new_desc,
            "due_date": new_due,
            "priority": new_priority
        })
        save_tasks(tasks)
        print("Task updated.")
    else:
        print("Invalid task number.")

# Search task
def search_task():
    keyword = input("Enter keyword to search: ").strip().lower()
    tasks = load_tasks()
    found = [t for t in tasks if keyword in t["description"].lower()]
    if not found:
        print("No tasks matched.")
        return
    for i, task in enumerate(found, 1):
        status = "✓" if task["completed"] else "✗"
        print(f"[{i}] {status} {task['description']} (Due: {task['due_date']}, Priority: {task['priority']})")

# Menu
def menu():
    while True:
        print("\n=== TO-DO LIST ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Completed Tasks")
        print("4. View Pending Tasks")
        print("5. View Overdue Tasks")
        print("6. Mark Task as Complete")
        print("7. Edit Task")
        print("8. Delete Task")
        print("9. Search Task")
        print("0. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks("completed")
        elif choice == "4":
            view_tasks("pending")
        elif choice == "5":
            view_tasks("overdue")
        elif choice == "6":
            mark_complete()
        elif choice == "7":
            edit_task()
        elif choice == "8":
            delete_task()
        elif choice == "9":
            search_task()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()
