"""
AI Agent — wraps the Anthropic Claude API for smart student task assistance.
"""

import os
import json
from typing import Optional
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """You are StudyBot, an encouraging and intelligent AI assistant built into a student task manager.
You help students stay organised, manage their workload, and succeed academically.

You have access to the student's task data which will be provided in each message.
You can help with:
- Suggesting priorities for tasks based on urgency and importance
- Breaking large assignments into smaller, manageable subtasks
- Estimating how long tasks might take
- Giving study tips and motivational support
- Identifying which tasks to tackle first
- Spotting overdue or at-risk deadlines

Personality: warm, encouraging, practical. Use light emojis occasionally. Keep responses concise and actionable.
Never be preachy. Students are busy — get to the point."""


def ask_ai(user_message: str, tasks: list, conversation_history: Optional[list] = None) -> str:
    """
    Send a message to Claude with the current task list as context.
    conversation_history is a list of {role, content} dicts for multi-turn chat.
    """
    if conversation_history is None:
        conversation_history = []

    task_context = f"\n\n--- STUDENT'S CURRENT TASKS ---\n{json.dumps(tasks, indent=2)}\n---"

    messages = conversation_history + [
        {"role": "user", "content": user_message + task_context}
    ]

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )

    return response.content[0].text


def suggest_priority(task: dict) -> str:
    """Ask AI to suggest a priority level for a single task."""
    prompt = (
        f"For this task: title='{task['title']}', subject='{task['subject']}', "
        f"due='{task.get('due_date', 'no deadline')}', description='{task.get('description', '')}'. "
        f"Reply with ONLY one word: low, medium, or high."
    )
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=10,
        system="You are a task prioritisation assistant. Reply with only one word.",
        messages=[{"role": "user", "content": prompt}],
    )
    word = response.content[0].text.strip().lower()
    return word if word in ("low", "medium", "high") else "medium"


def generate_subtasks(task: dict) -> list[str]:
    """Ask AI to break a task into 3-5 subtasks."""
    prompt = (
        f"Break this student task into 3-5 concrete subtasks.\n"
        f"Task: {task['title']}\nSubject: {task['subject']}\nNotes: {task.get('description', '')}\n"
        f"Reply ONLY with a JSON array of short strings, no explanation."
    )
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=300,
        system="You are a study planning assistant. Reply only with a JSON array.",
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    try:
        subtasks = json.loads(text)
        return subtasks if isinstance(subtasks, list) else []
    except json.JSONDecodeError:
        return []
