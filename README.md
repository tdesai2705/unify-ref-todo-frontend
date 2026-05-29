# Frontend UI

Flask-based web UI for the 2-tier to-do application.

## Technology Stack

- **Framework**: Python Flask 3.0
- **Template Engine**: Jinja2
- **Styling**: CSS3 (custom responsive design)
- **JavaScript**: Vanilla JS
- **HTTP Client**: Python requests library

## Features

- ✅ Server-side rendered UI with Jinja2 templates
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Statistics dashboard with completion rate
- ✅ Priority-based task filtering
- ✅ Category organization
- ✅ Feature flag integration (due date, dark mode)
- ✅ Real-time flash messages
- ✅ Keyboard shortcuts (press 'N' for new todo)

## Feature Flags

### 1. Due Date Feature
- **Flag Name**: `due-date-feature`
- **Description**: Shows/hides due date field in add todo form
- **Default**: OFF

### 2. Dark Mode
- **Flag Name**: `dark-mode`
- **Description**: Toggles dark theme
- **Default**: OFF

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export BACKEND_API_URL="http://localhost:5000/api"
export SECRET_KEY="dev-secret-key"

# Run the server
python run.py
```

Server runs on `http://localhost:5001`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BACKEND_API_URL` | Backend REST API URL | `http://localhost:5000/api` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key-change-in-production` |
| `CASK_API_KEY` | CloudBees Feature Management API key | (empty) |
| `FEATURE_DUE_DATE` | Enable due date feature | `false` |
| `FEATURE_DARK_MODE` | Enable dark mode | `false` |

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home (redirects to todos) |
| `/todos` | Main todo list page |
| `/todos/add` | Add new todo (POST) |
| `/todos/:id/toggle` | Toggle completion (POST) |
| `/todos/:id/delete` | Delete todo (POST) |
| `/health` | Health check endpoint |

## Project Structure

```
frontend/
├── app/
│   ├── __init__.py       # Flask app factory
│   └── views.py          # Route handlers
├── templates/
│   ├── base.html         # Base template
│   └── todo_list.html    # Main UI
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styling
│   └── js/
│       └── app.js        # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── Dockerfile           # Multi-stage Docker build
```

## CloudBees Unify Integration

This frontend integrates with:
- ✅ Backend REST API (service discovery via K8s DNS)
- ✅ Feature Management (Cask) for feature flags
- ✅ CloudBees Unify CI/CD workflows
- ✅ Multi-environment deployment (Dev, QA, Prod)

Part of CloudBees Unify Reference Architecture project.

**Team**: Tejas Desai (2-tier), Dinesh Narlakanti (3-tier), Anudeep Nalla (Infrastructure)
**Lead**: Xhesi Galanxhi
