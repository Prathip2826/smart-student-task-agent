import os
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock

# We patch storage so tests don't touch the real filesystem
MOCK_TASKS = []


def reset_mock():
    global MOCK_TASKS
    MOCK_TASKS = []


def mock_load():
    return list(MOCK_TASKS)


def mock_save(tasks):
    global MOCK_TASKS
    MOCK_TASKS = list(tasks)


@pytest.fixture(autouse=True)
def patch_storage():
    reset_mock()
    with patch("app.task_manager.load_tasks", side_effect=mock_load), \
         patch("app.task_manager.save_tasks", side_effect=mock_save):
        yield


from app.task_manager import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
    filter_tasks,
    get_summary,
    get_upcoming_tasks,
)


class TestCreateTask:
    def test_creates_task_with_required_fields(self):
        task = create_task(title="Read Chapter 5")
        assert task["title"] == "Read Chapter 5"
        assert task["status"] == "pending"
        assert task["priority"] == "medium"
        assert "id" in task

    def test_creates_task_with_all_fields(self):
        task = create_task(
            title="Essay Draft",
            description="Write 1000 words",
            due_date="2025-06-01",
            priority="high",
            subject="English",
        )
        assert task["subject"] == "English"
        assert task["due_date"] == "2025-06-01"
        assert task["priority"] == "high"

    def test_raises_on_empty_title(self):
        with pytest.raises(ValueError, match="empty"):
            create_task(title="   ")

    def test_raises_on_invalid_priority(self):
        with pytest.raises(ValueError, match="Priority"):
            create_task(title="Task", priority="urgent")

    def test_task_is_persisted(self):
        create_task(title="Persist me")
        all_tasks = get_all_tasks()
        assert len(all_tasks) == 1
        assert all_tasks[0]["title"] == "Persist me"


class TestGetTasks:
    def test_get_all_returns_empty_list(self):
        assert get_all_tasks() == []

    def test_get_task_by_id(self):
        task = create_task(title="Find me")
        found = get_task_by_id(task["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_get_task_by_id_not_found(self):
        assert get_task_by_id("nonexistent-id") is None


class TestUpdateTask:
    def test_update_title(self):
        task = create_task(title="Old Title")
        updated = update_task(task["id"], title="New Title")
        assert updated["title"] == "New Title"

    def test_update_status(self):
        task = create_task(title="Do homework")
        updated = update_task(task["id"], status="completed")
        assert updated["status"] == "completed"

    def test_update_invalid_status(self):
        task = create_task(title="Task")
        with pytest.raises(ValueError, match="Status"):
            update_task(task["id"], status="done")

    def test_update_invalid_priority(self):
        task = create_task(title="Task")
        with pytest.raises(ValueError, match="Priority"):
            update_task(task["id"], priority="critical")

    def test_update_nonexistent_task(self):
        with pytest.raises(KeyError):
            update_task("bad-id", title="Oops")

    def test_update_invalid_field(self):
        task = create_task(title="Task")
        with pytest.raises(ValueError, match="Cannot update"):
            update_task(task["id"], color="red")


class TestDeleteTask:
    def test_delete_existing_task(self):
        task = create_task(title="Delete me")
        result = delete_task(task["id"])
        assert result is True
        assert get_task_by_id(task["id"]) is None

    def test_delete_nonexistent_task(self):
        result = delete_task("ghost-id")
        assert result is False


class TestFilterTasks:
    def setup_method(self):
        create_task(title="Math HW", subject="Math", priority="high", status="pending" if False else "pending")
        t2 = create_task(title="History Essay", subject="History", priority="medium")
        update_task(t2["id"], status="completed")
        create_task(title="Physics Lab", subject="Physics", priority="low")

    def test_filter_by_status(self):
        results = filter_tasks(status="completed")
        assert all(t["status"] == "completed" for t in results)
        assert len(results) == 1

    def test_filter_by_priority(self):
        results = filter_tasks(priority="high")
        assert all(t["priority"] == "high" for t in results)

    def test_filter_by_subject(self):
        results = filter_tasks(subject="math")
        assert len(results) == 1
        assert results[0]["subject"] == "Math"

    def test_filter_combined(self):
        results = filter_tasks(status="pending", priority="low")
        assert all(t["status"] == "pending" and t["priority"] == "low" for t in results)


class TestSummary:
    def test_summary_counts(self):
        create_task(title="T1", priority="high")
        create_task(title="T2", priority="low")
        t3 = create_task(title="T3")
        update_task(t3["id"], status="completed")

        s = get_summary()
        assert s["total"] == 3
        assert s["by_status"]["completed"] == 1
        assert s["by_status"]["pending"] == 2
        assert s["by_priority"]["high"] == 1
        assert s["by_priority"]["low"] == 1
