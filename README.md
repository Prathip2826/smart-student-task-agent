# smart-student-task-agent
# 🤖 Smart Student Task Agent

A simple Agentic AI based web application built using HTML, CSS, and JavaScript.

## 📌 Project Description
Smart Student Task Agent helps students:
- Add assignments with deadline and priority
- Automatically sort tasks
- Highlight urgent tasks
- Generate daily focus suggestions
- Track completed tasks

This project is built to gain practical experience in frontend development and basic agent-based decision logic.

---

## 🛠 Tech Stack
- HTML
- CSS
- JavaScript (Vanilla JS)
- Git & GitHub (for collaboration)

---

## 🚀 Features (Phase 1)
- Add new task
- Set deadline
- Set priority (Low / Medium / High)
- Display task list
- Delete task
- Mark task as completed

---

## 🔮 Future Improvements (Phase 2 & 3)
- Auto study plan generation
- Productivity score
- LocalStorage integration
- AI-based suggestions (API integration)

---

## 👩‍💻👨‍💻 Team Members
- Prathip Munusamy
- Sujitha Shanmugam

---

## Features

- **Add tasks** with title, subject, description, due date, and priority
- **List & filter** tasks by status, priority, or subject
- **Update** any task field (title, status, priority, due date, etc.)
- **Delete** tasks you no longer need
- **Upcoming tasks** — see what's due in the next 7 days
- **Summary** — quick overview of all tasks by status and priority
- **Persistent storage** via a local `data/tasks.json` file

---

## Setup

```bash
# Clone the repo
git clone https://github.com/your-username/smart-student-task-agent.git
cd smart-student-task-agent

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python -m app.main
```

You'll see an interactive menu:

```
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
```

---

## Task Fields

| Field       | Description                                      |
|-------------|--------------------------------------------------|
| `title`     | Short name of the task (required)               |
| `subject`   | Course or subject (e.g. Math, History)          |
| `description` | Extra notes or details                        |
| `due_date`  | ISO format date: `YYYY-MM-DD`                   |
| `priority`  | `low`, `medium`, or `high`                      |
| `status`    | `pending`, `in-progress`, or `completed`        |

---

## Running Tests

```bash
pytest tests/
```

---

## 🎯 Purpose
This project is created for learning:
- Frontend development
- DOM manipulation
- Basic Agentic AI logic
- Version control using GitHub

---

## Project Structure

```
smart-student-task-agent/
├── app/
│   ├── __init__.py       # Package init
│   ├── main.py           # CLI entry point
│   ├── task_manager.py   # Business logic (CRUD + filtering)
│   └── storage.py        # JSON file persistence
├── data/
│   └── tasks.json        # Local task storage (auto-created)
├── tests/
│   └── test_task_manager.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## License

MIT
