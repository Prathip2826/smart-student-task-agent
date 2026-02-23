"""
AI Agent — uses Google Gemini API (free tier) for smart student task assistance.
Get your free API key at: https://aistudio.google.com/apikey
Set environment variable: GEMINI_API_KEY
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

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


def _gemini_request(contents: list, max_tokens: int = 1024) -> str:
    """Make a raw request to the Gemini API using only stdlib."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")

    payload = json.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7}
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"Gemini API error {e.code}: {body}")


def ask_ai(user_message: str, tasks: list, conversation_history: Optional[list] = None) -> str:
    """Send a message to Gemini with the current task list as context."""
    if conversation_history is None:
        conversation_history = []

    task_context = f"\n\n--- STUDENT'S CURRENT TASKS ---\n{json.dumps(tasks, indent=2)}\n---"

    contents = []
    for msg in conversation_history[-10:]:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    contents.append({"role": "user", "parts": [{"text": user_message + task_context}]})

    return _gemini_request(contents, max_tokens=1024)


def suggest_priority(task: dict) -> str:
    """Ask Gemini to suggest a priority level for a single task."""
    prompt = (
        f"For this student task: title='{task['title']}', subject='{task.get('subject','')}', "
        f"due='{task.get('due_date', 'no deadline')}', description='{task.get('description', '')}'. "
        f"Reply with ONLY one word: low, medium, or high."
    )
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    try:
        word = _gemini_request(contents, max_tokens=10).strip().lower()
        return word if word in ("low", "medium", "high") else "medium"
    except Exception:
        return "medium"


def generate_subtasks(task: dict) -> list:
    """Ask Gemini to break a task into 3-5 subtasks."""
    prompt = (
        f"Break this student task into 3-5 concrete subtasks.\n"
        f"Task: {task['title']}\nSubject: {task.get('subject','')}\n"
        f"Notes: {task.get('description', '')}\n"
        f"Reply ONLY with a JSON array of short strings, no explanation, no markdown."
    )
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    try:
        text = _gemini_request(contents, max_tokens=300).strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        subtasks = json.loads(text)
        return subtasks if isinstance(subtasks, list) else []
    except Exception:
        return []