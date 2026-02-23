"""
AI Agent — uses Groq API (free tier) for smart student task assistance.
Get your free API key at: https://console.groq.com
Set environment variable: GROQ_API_KEY
Free tier: 14,400 requests/day — plenty for StudyBot!
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"  # Free, fast, great for chat

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


def _groq_request(messages: list, max_tokens: int = 1024) -> str:
    """Make a raw request to the Groq API using only stdlib."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }).encode("utf-8")

    req = urllib.request.Request(
        GROQ_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Groq API error {e.code}: {body}")


def ask_ai(user_message: str, tasks: list, conversation_history: Optional[list] = None) -> str:
    """Send a message to Groq with the current task list as context."""
    if conversation_history is None:
        conversation_history = []

    task_context = f"\n\n--- STUDENT'S CURRENT TASKS ---\n{json.dumps(tasks, indent=2)}\n---"

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in conversation_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message + task_context})

    return _groq_request(messages, max_tokens=1024)


def suggest_priority(task: dict) -> str:
    """Ask Groq to suggest a priority level for a single task."""
    prompt = (
        f"For this student task: title='{task['title']}', subject='{task.get('subject','')}', "
        f"due='{task.get('due_date', 'no deadline')}', description='{task.get('description', '')}'. "
        f"Reply with ONLY one word: low, medium, or high."
    )
    messages = [
        {"role": "system", "content": "You are a task prioritisation assistant. Reply with only one word: low, medium, or high."},
        {"role": "user", "content": prompt}
    ]
    try:
        word = _groq_request(messages, max_tokens=10).strip().lower()
        return word if word in ("low", "medium", "high") else "medium"
    except Exception:
        return "medium"


def generate_subtasks(task: dict) -> list:
    """Ask Groq to break a task into 3-5 subtasks."""
    prompt = (
        f"Break this student task into 3-5 concrete subtasks.\n"
        f"Task: {task['title']}\nSubject: {task.get('subject','')}\n"
        f"Notes: {task.get('description', '')}\n"
        f"Reply ONLY with a JSON array of short strings, no explanation, no markdown."
    )
    messages = [
        {"role": "system", "content": "You are a study planning assistant. Reply only with a JSON array of strings."},
        {"role": "user", "content": prompt}
    ]
    try:
        text = _groq_request(messages, max_tokens=300).strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        subtasks = json.loads(text)
        return subtasks if isinstance(subtasks, list) else []
    except Exception:
        return []