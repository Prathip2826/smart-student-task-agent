import json
import os
from typing import List, Dict, Any

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'tasks.json')


def _ensure_data_file():
    """Ensure the data directory and file exist."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)


def load_tasks() -> List[Dict[str, Any]]:
    """Load all tasks from the JSON storage file."""
    _ensure_data_file()
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Save all tasks to the JSON storage file."""
    _ensure_data_file()
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
