"""
Flask web server for the Smart Student Task Agent.
Run with: python server.py
"""

from flask import Flask, request, jsonify, send_from_directory
import os, sys

sys.path.insert(0, os.path.dirname(__file__))

import app.task_manager as task_manager
import app.ai_agent as ai_agent

app = Flask(__name__, static_folder="web")


# ── Static Files ──────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("web", "index.html")


# ── Tasks API ─────────────────────────────────────────────────
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    priority = request.args.get("priority")
    subject = request.args.get("subject")
    if any([status, priority, subject]):
        tasks = task_manager.filter_tasks(status=status, priority=priority, subject=subject)
    else:
        tasks = task_manager.get_all_tasks()
    return jsonify(tasks)


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.json
    try:
        task = task_manager.create_task(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date") or None,
            priority=data.get("priority", "medium"),
            subject=data.get("subject", ""),
        )
        return jsonify(task), 201
    except (ValueError, KeyError) as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    try:
        allowed = {"title", "description", "due_date", "priority", "status", "subject"}
        fields = {k: v for k, v in data.items() if k in allowed}
        task = task_manager.update_task(task_id, **fields)
        return jsonify(task)
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = task_manager.delete_task(task_id)
    if deleted:
        return jsonify({"deleted": True})
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/summary")
def summary():
    return jsonify(task_manager.get_summary())


@app.route("/api/upcoming")
def upcoming():
    days = int(request.args.get("days", 7))
    return jsonify(task_manager.get_upcoming_tasks(days=days))


# ── AI API ────────────────────────────────────────────────────
@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    data = request.json
    message = data.get("message", "")
    history = data.get("history", [])
    tasks = task_manager.get_all_tasks()
    try:
        reply = ai_agent.ask_ai(message, tasks, history)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai/suggest-priority/<task_id>", methods=["POST"])
def suggest_priority(task_id):
    task = task_manager.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    try:
        priority = ai_agent.suggest_priority(task)
        return jsonify({"priority": priority})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai/subtasks/<task_id>", methods=["POST"])
def generate_subtasks(task_id):
    task = task_manager.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    try:
        subtasks = ai_agent.generate_subtasks(task)
        return jsonify({"subtasks": subtasks})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("🚀 Smart Student Task Agent running at http://localhost:5000")
    app.run(debug=True, port=5000)