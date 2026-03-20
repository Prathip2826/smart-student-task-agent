<div align="center">

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        ◆  SMART STUDENT TASK AGENT  ◆                    ║
║           AI-Powered Academic OS                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_App-6366F1?style=for-the-badge&labelColor=0D0D0D)](https://smart-student-task-agent.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0D0D0D)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=0D0D0D)](https://flask.palletsprojects.com)
[![Claude AI](https://img.shields.io/badge/Claude-Anthropic-CC785C?style=for-the-badge&logoColor=white&labelColor=0D0D0D)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge&labelColor=0D0D0D)](#license)

<br/>

> *An AI-native task manager built to understand how students actually work —*
> *deadlines, pressure, procrastination and all.*

<br/>

**Built by [Prathip Munusamy](https://github.com/Prathip2826) & [Sujitha Shanmugam](https://github.com/suji2826)**
*as a hands-on project to master frontend development, agentic AI, and version control*

</div>

---

## ◈ What is This?

Most task managers treat a student assignment the same as a grocery list. This one doesn't.

**Smart Student Task Agent** is a full-stack academic productivity tool powered by Claude AI. It doesn't just store your tasks — it *thinks* about them. It reads your workload, figures out what's urgent, suggests priorities, and breaks down complex assignments into manageable steps. When you're stuck, StudyBot is there to talk it through.

Think of it as a calm, always-available academic co-pilot.

---

## ◈ Feature Breakdown

### Core Task Engine

| Capability | Details |
|---|---|
| **Add Tasks** | Title, subject, description, due date, priority — all in one form |
| **Smart Filtering** | Filter by status, priority, or subject instantly |
| **Overdue Detection** | Automatically flags tasks past their deadline |
| **Upcoming View** | See everything due in the next 7 days at a glance |
| **Full CRUD** | Update any field, delete what you don't need |
| **Status Tracking** | Track completion across your entire workload |
| **Summary Dashboard** | Quick count of tasks by status and priority |

### AI Layer — Powered by Claude

| Feature | What It Does |
|---|---|
| **StudyBot** | Conversational AI for study help, concept explanation, and planning |
| **Priority Suggester** | AI evaluates deadline, complexity, and subject to recommend the right priority |
| **Subtask Generator** | Breaks any assignment into step-by-step subtasks automatically |
| **Daily Focus** | AI suggests what to work on today based on your current task list |

### Infrastructure

| Layer | Technology |
|---|---|
| **Storage** | JSON file persistence (`data/tasks.json`) — simple, portable, zero-config |
| **REST API** | Flask backend with clean endpoints for all task operations |
| **CLI Mode** | Full command-line interface for terminal lovers |

---

## ◈ Tech Stack

```
┌─────────────────────────────────────────────────────┐
│  Frontend        HTML · CSS · Vanilla JavaScript     │
│  Backend         Python · Flask                      │
│  AI Engine       Anthropic Claude API                │
│  Storage         JSON (local file persistence)       │
│  Version Control Git · GitHub                        │
└─────────────────────────────────────────────────────┘
```

---

## ◈ Getting Started

### Prerequisites

- Python 3.11 or higher
- An [Anthropic API key](https://console.anthropic.com/) — required for AI features
- Git

### 1 — Clone & Install

```bash
git clone https://github.com/Prathip2826/smart-student-task-agent.git
cd smart-student-task-agent

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2 — Set Your API Key

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=your_key_here

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your_key_here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your_key_here"
```

> **Tip:** Add this to your `.bashrc` / `.zshrc` so you don't have to set it every session. Or use a `.env` file with `python-dotenv`.

### 3 — Run

```bash
# Web app (recommended)
python server.py
# Open http://localhost:5000 in your browser

# CLI mode (optional)
python -m app.main
```

---

## ◈ Running Tests

```bash
# Run all tests
pytest tests/

# Verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

---

## ◈ Project Structure

```
smart-student-task-agent/
│
├── app/
│   ├── __init__.py          # Package initialisation
│   ├── main.py              # CLI entry point
│   ├── task_manager.py      # Core logic — CRUD, filtering, validation
│   ├── storage.py           # JSON file persistence layer
│   └── ai_agent.py          # Claude API integration & AI features
│
├── web/
│   └── index.html           # Full web UI (single-page)
│
├── data/
│   ├── tasks.json           # Local task storage (auto-created on first run)
│   └── .gitkeep
│
├── tests/
│   ├── __init__.py
│   └── test_task_manager.py # Unit tests for core task logic
│
├── server.py                # Flask web server + REST API routes
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project metadata
├── .gitignore
└── README.md
```

### Key Modules

**`task_manager.py`** — the brain of the operation. All business logic lives here: creating and validating tasks, sorting by priority and deadline, filtering by subject or status, and detecting overdue items.

**`ai_agent.py`** — the Claude integration layer. Handles prompt construction, API calls, and response parsing for StudyBot, the priority suggester, and the subtask generator.

**`storage.py`** — a thin wrapper around JSON read/write with atomic writes and error recovery.

**`server.py`** — Flask routes that expose everything as a clean REST API consumed by the web UI.

---

## ◈ REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/tasks` | Fetch all tasks |
| `POST` | `/api/tasks` | Create a new task |
| `PUT` | `/api/tasks/<id>` | Update a task by ID |
| `DELETE` | `/api/tasks/<id>` | Delete a task by ID |
| `GET` | `/api/tasks/upcoming` | Tasks due in the next 7 days |
| `GET` | `/api/tasks/summary` | Count by status and priority |
| `POST` | `/api/ai/chat` | StudyBot conversation |
| `POST` | `/api/ai/priority` | AI priority suggestion |
| `POST` | `/api/ai/subtasks` | AI subtask generation |

---

## ◈ Team

<table>
  <tr>
    <td align="center" width="50%">
      <b>Prathip Munusamy</b><br/>
      <a href="https://github.com/Prathip2826">@Prathip2826</a><br/>
      <sub>Backend · AI Integration · Architecture</sub>
    </td>
    <td align="center" width="50%">
      <b>Sujitha Shanmugam</b><br/>
      <a href="https://github.com/suji2826">@suji2826</a><br/>
      <sub>Frontend · UX · Testing</sub>
    </td>
  </tr>
</table>

---

## ◈ Roadmap

The foundation is solid. Here's what's next:

- [ ] **Auto study plan generation** — Claude builds a week-by-week plan from your task list
- [ ] **Productivity scores & streaks** — gamified consistency tracking
- [ ] **Mobile-responsive design** — full usability on phones and tablets
- [ ] **Notifications & reminders** — browser push + email digests before deadlines
- [ ] **Multi-user support** — shared workspaces for study groups
- [ ] **Calendar sync** — export tasks to Google Calendar / iCal
- [ ] **Pomodoro integration** — built-in focus timer linked to tasks

---

## ◈ Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

```bash
# 1. Fork the repo on GitHub
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Commit with a clear message
git commit -m "feat: add calendar sync support"

# 4. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please ensure all tests pass before submitting: `pytest tests/`

---

## ◈ License

```
MIT License — free to use, modify, and distribute.
See LICENSE file for full terms.
```

---

<div align="center">

**Smart Student Task Agent** — built with focus, shipped with care.

*If this project helped you, drop a ⭐ on the repo.*

</div>
