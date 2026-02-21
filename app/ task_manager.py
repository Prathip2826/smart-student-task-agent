import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.storage import load_tasks, save_tasks

VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "in-progress", "completed"]


def _now() -> str:
    return datetime.now().isoformat()


def _validate_due_date(due_date: Optional[str]) -> None:
    """Validate that due_date is in YYYY-MM-DD format."""
    if due_date is None:
        return
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"due_date must be in YYYY-MM-DD format, got: '{due_date}'")


def create_task(
    title: str,
    description: str = "",
    due_date: Optional[str] = None,
    priority: str = "medium",
    subject: str = ""
) -> Dict[str, Any]:
    """Create a new task and persist it."""
    if not title.strip():
        raise ValueError("Task title cannot be empty.")
    if priority not in VALID_PRIORITIES:
        raise ValueError(f"Priority must be one of {VALID_PRIORITIES}.")
    _validate_due_date(due_date)

    task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "description": description.strip(),
        "subject": subject.strip(),
        "due_date": due_date,
        "priority": priority,
        "status": "pending",
        "created_at": _now(),
        "updated_at": _now(),
    }

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return task


def get_all_tasks() -> List[Dict[str, Any]]:
    """Return all tasks."""
    return load_tasks()


def get_task_by_id(task_id: str) -> Optional[Dict[str, Any]]:
    """Return a single task by ID, or None if not found."""
    tasks = load_tasks()
    return next((t for t in tasks if t["id"] == task_id), None)


def update_task(task_id: str, **fields) -> Dict[str, Any]:
    """Update fields of an existing task."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            allowed = {"title", "description", "due_date", "priority", "status", "subject"}
            for key, value in fields.items():
                if key not in allowed:
                    raise ValueError(f"Cannot update field: {key}")
                if key == "priority" and value not in VALID_PRIORITIES:
                    raise ValueError(f"Priority must be one of {VALID_PRIORITIES}.")
                if key == "status" and value not in VALID_STATUSES:
                    raise ValueError(f"Status must be one of {VALID_STATUSES}.")
                if key == "due_date":
                    _validate_due_date(value)
                task[key] = value
            task["updated_at"] = _now()
            save_tasks(tasks)
            return task
    raise KeyError(f"Task with id '{task_id}' not found.")


def delete_task(task_id: str) -> bool:
    """Delete a task by ID. Returns True if deleted, False if not found."""
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks)
    return True


def filter_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    subject: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Filter tasks by status, priority, and/or subject."""
    tasks = load_tasks()
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if subject:
        tasks = [t for t in tasks if subject.lower() in t["subject"].lower()]
    return tasks


def get_upcoming_tasks(days: int = 7) -> List[Dict[str, Any]]:
    """Return tasks due within the next `days` days."""
    from datetime import timedelta
    tasks = load_tasks()
    cutoff = datetime.now() + timedelta(days=days)
    upcoming = []
    for task in tasks:
        if task.get("due_date") and task["status"] != "completed":
            try:
                due = datetime.fromisoformat(task["due_date"])
                if datetime.now() <= due <= cutoff:
                    upcoming.append(task)
            except ValueError:
                pass
    upcoming.sort(key=lambda t: t["due_date"])
    return upcoming


def get_summary() -> Dict[str, Any]:
    """Return a summary of task counts by status and priority."""
    tasks = load_tasks()
    summary = {
        "total": len(tasks),
        "by_status": {s: 0 for s in VALID_STATUSES},
        "by_priority": {p: 0 for p in VALID_PRIORITIES},
    }
    for task in tasks:
        summary["by_status"][task["status"]] = summary["by_status"].get(task["status"], 0) + 1
        summary["by_priority"][task["priority"]] = summary["by_priority"].get(task["priority"], 0) + 1
    return summary
