# 🤖 Smart Student Task Agent

An AI-powered student task manager built by **Prathip Munusamy** & **Sujitha Shanmugam** as a hands-on project to learn frontend development, agentic AI logic, and version control.

---

## 🚀 Live Demo

🔗 **Try it now:**  
https://smart-student-task-agent.onrender.com/

---

## 📌 Project Description

Smart Student Task Agent helps students:
- Add assignments with deadline and priority
- Automatically sort and filter tasks
- Highlight urgent and overdue tasks
- Chat with an AI study assistant (StudyBot)
- Generate daily focus suggestions
- Track completed tasks

---

## 🛠 Tech Stack

- **Frontend** — HTML, CSS, JavaScript (Vanilla JS)
- **Backend** — Python, Flask
- **AI** — Anthropic Claude API (StudyBot)
- **Storage** — JSON file (local persistence)
- **Version Control** — Git & GitHub

---

## 🚀 Features

- Add tasks with title, subject, description, due date, and priority
- List & filter tasks by status, priority, or subject
- Update any task field (title, status, priority, due date, etc.)
- Delete tasks you no longer need
- Upcoming tasks — see what's due in the next 7 days
- Summary — quick overview of all tasks by status and priority
- **StudyBot AI** — chat assistant powered by Claude
- **AI Priority Suggestion** — let AI recommend the right priority
- **AI Subtask Generator** — break assignments into manageable steps
- Persistent storage via `data/tasks.json`

---

## ⚙️ Setup

```bash
# Clone the repo
git clone https://github.com/your-username/smart-student-task-agent.git
cd smart-student-task-agent

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here
```

---

## 🌐 Run the Web App

```bash
python server.py
# Open http://localhost:5000
```

## 🖥 Run the CLI (optional)

```bash
python -m app.main
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📁 Project Structure

```
smart-student-task-agent/
├── app/
│   ├── __init__.py         # Package init
│   ├── main.py             # CLI entry point
│   ├── task_manager.py     # Business logic (CRUD + filtering + validation)
│   ├── storage.py          # JSON file persistence
│   └── ai_agent.py         # Claude API integration
├── web/
│   └── index.html          # Full web UI
├── data/
│   ├── tasks.json          # Local task storage (auto-created)
│   └── .gitkeep
├── tests/
│   ├── __init__.py
│   └── test_task_manager.py
├── server.py               # Flask web server + REST API
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 👩‍💻 Team Members

| Name | GitHub |
|------|--------|
| Prathip Munusamy | @Prathip2826 |
| Sujitha Shanmugam | @suji2826 |

---

## 🔮 Future Improvements

- Auto study plan generation
- Productivity score & streaks
- Mobile-responsive design
- Notifications & reminders

---

## 📄 License

MIT
