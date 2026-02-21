"""
Smart Student Task Agent — CLI Entry Point
Usage: python -m app.main
"""

import sys
from typing import Optional
from app import task_manager


def print_task(task: dict) -> None:
    print(f"""
  ID       : {task['id']}
  Title    : {task['title']}
  Subject  : {task['subject'] or '—'}
  Priority : {task['priority']}
  Status   : {task['status']}
  Due Date : {task['due_date'] or '—'}
  Notes    : {task['description'] or '—'}
  Created  : {task['created_at']}
""")


def cmd_add():
    print("\n── Add New Task ──")
    title = input("Title: ").strip()
    subject = input("Subject (e.g. Math, History): ").strip()
    description = input("Notes/Description: ").strip()
    due_date = input("Due date (YYYY-MM-DD or leave blank): ").strip() or None
    priority = input("Priority [low/medium/high] (default: medium): ").strip() or "medium"

    try:
        task = task_manager.create_task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            subject=subject,
        )
        print(f"\n✅ Task created! ID: {task['id']}")
    except ValueError as e:
        print(f"\n❌ Error: {e}")


def cmd_list():
    print("\n── All Tasks ──")
    tasks = task_manager.get_all_tasks()
    if not tasks:
        print("  No tasks found.")
        return
    for task in tasks:
        print_task(task)


def cmd_filter():
    print("\n── Filter Tasks ──")
    status = input("Filter by status [pending/in-progress/completed] (leave blank to skip): ").strip() or None
    priority = input("Filter by priority [low/medium/high] (leave blank to skip): ").strip() or None
    subject = input("Filter by subject keyword (leave blank to skip): ").strip() or None

    tasks = task_manager.filter_tasks(status=status, priority=priority, subject=subject)
    if not tasks:
        print("  No tasks match your filter.")
    for task in tasks:
        print_task(task)


def cmd_update():
    print("\n── Update Task ──")
    task_id = input("Enter Task ID: ").strip()
    print("Leave any field blank to keep current value.")
    fields = {}
    for field in ["title", "description", "due_date", "priority", "status", "subject"]:
        val = input(f"  New {field}: ").strip()
        if val:
            fields[field] = val

    if not fields:
        print("  No changes made.")
        return
    try:
        task = task_manager.update_task(task_id, **fields)
        print(f"\n✅ Task updated!")
        print_task(task)
    except (KeyError, ValueError) as e:
        print(f"\n❌ Error: {e}")


def cmd_delete():
    print("\n── Delete Task ──")
    task_id = input("Enter Task ID to delete: ").strip()
    confirm = input(f"Are you sure you want to delete task '{task_id}'? [y/N]: ").strip().lower()
    if confirm == 'y':
        deleted = task_manager.delete_task(task_id)
        print("✅ Task deleted." if deleted else "❌ Task not found.")
    else:
        print("  Cancelled.")


def cmd_upcoming():
    print("\n── Upcoming Tasks (next 7 days) ──")
    tasks = task_manager.get_upcoming_tasks(days=7)
    if not tasks:
        print("  No upcoming tasks in the next 7 days.")
    for task in tasks:
        print_task(task)


def cmd_summary():
    print("\n── Task Summary ──")
    s = task_manager.get_summary()
    print(f"  Total tasks : {s['total']}")
    print(f"  By status   : {s['by_status']}")
    print(f"  By priority : {s['by_priority']}")


MENU = """
╔══════════════════════════════════╗
║   Smart Student Task Agent 📚   ║
╠══════════════════════════════════╣
║  1. Add task                     ║
║  2. List all tasks               ║
║  3. Filter tasks                 ║
║  4. Update task                  ║
║  5. Delete task                  ║
║  6. Upcoming (next 7 days)       ║
║  7. Summary                      ║
║  0. Exit                         ║
╚══════════════════════════════════╝
"""

COMMANDS = {
    "1": cmd_add,
    "2": cmd_list,
    "3": cmd_filter,
    "4": cmd_update,
    "5": cmd_delete,
    "6": cmd_upcoming,
    "7": cmd_summary,
}


def main():
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("👋 Goodbye! Stay on top of your studies!")
            sys.exit(0)
        handler = COMMANDS.get(choice)
        if handler:
            handler()
        else:
            print("  ❓ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
