# 🍳 Recipe Sharing Platform

A modern web application for sharing and discovering delicious recipes.

## 📋 Project Status

**Current Phase:** Phase 2 - Data Foundation  
**Current Milestone:** 2.1 - User System  
**Milestone 1.1 Status:** 🟢 90% Complete (Supabase setup pending)  
**Milestone 1.2 Status:** 🟢 95% Complete (Database test pending)  
**Milestone 2.1 Status:** 🟢 100% Complete (Ready for migration)

**Completion Checklist:** See [Milestone 1.1 Checklist](docs/getting-started/MILESTONE_1.1_CHECKLIST.md)

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have the following installed on your system:

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
   - Check your version: `python --version` or `python3 --version`
   
2. **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
   - For Windows: Use the official installer
   - For Mac: `brew install postgresql`
   - For Linux: `sudo apt-get install postgresql postgresql-contrib`
   
3. **Git** - [Download Git](https://git-scm.com/downloads)
   - Check your version: `git --version`

4. **Supabase Account** - [Sign up at Supabase](https://supabase.com)
   - We'll use Supabase as our cloud database (PostgreSQL)

### 🛠️ Setup Instructions

#### Step 1: Clone the Repository (if working with a team)

```bash
git clone <repository-url>
cd Recipe-Sharing-Platform
```

#### Step 2: Create a Virtual Environment

**Why?** A virtual environment isolates your project's dependencies from other Python projects on your computer. This prevents version conflicts.

```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

**Activate the virtual environment:**

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Mac/Linux
source venv/bin/activate
```

You'll know it's activated when you see `(venv)` at the beginning of your command prompt.

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all the Python packages listed in `requirements.txt`.

#### Step 4: Set Up Environment Variables

**🔒 SECURITY BEST PRACTICE**: Never commit your `.env` file to Git! It contains sensitive information like passwords and secret keys. The `.env` file is already in `.gitignore` to protect you.

1. Copy the example environment file:
   ```bash
   copy env.example .env  # Windows
   # or
   cp env.example .env    # Mac/Linux
   ```

2. Generate a secure SECRET_KEY:
   ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Copy the generated key.

3. Edit `.env` and fill in all the values:
   - Paste your generated SECRET_KEY
   - Add your Supabase database credentials (we'll get these next)

#### Step 5: Set Up Supabase Database

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Create a new project
3. Note down your:
   - Project URL
   - Database Password
   - API Keys (anon/public key)

#### Step 6: Initialize Django Project

```bash
django-admin startproject config .
python manage.py migrate
python manage.py createsuperuser
```

#### Step 7: Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser!

## 📁 Project Structure

```
Recipe-Sharing-Platform/
├── config/              # Django project settings
├── apps/                # Django applications
├── docs/                # Project documentation
│   ├── README.md        # Documentation index
│   ├── getting-started/ # Setup and onboarding guides
│   │   └── SETUP_GUIDE.md
│   ├── security/        # Security and best practices
│   │   └── SECURITY.md
│   └── development/     # Development resources
├── scripts/             # Helper scripts
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── templates/           # HTML templates
├── venv/                # Virtual environment (not in git)
├── .env                 # Environment variables (not in git)
├── env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 📚 Documentation

For detailed documentation, see the [`docs/`](docs/) folder:

### Getting Started
- **[Setup Guide](docs/getting-started/SETUP_GUIDE.md)** - Complete step-by-step setup instructions
- **[Quick Start](docs/getting-started/QUICK_START.md)** - Fast reference for completing Milestone 1.1
- **[Essential Setup](docs/getting-started/ESSENTIAL_SETUP.md)** - Essential information to get started
- **[Environment Variables Guide](docs/getting-started/ENV_VARIABLES_GUIDE.md)** - Complete API keys & credentials guide
- **[Milestone 1.1 Checklist](docs/getting-started/MILESTONE_1.1_CHECKLIST.md)** - Verification checklist
- **[Milestone Status](docs/getting-started/MILESTONE_STATUS.md)** - Current progress (90% complete)

### Security & Best Practices
- **[Security Best Practices](docs/security/SECURITY.md)** - How to handle secrets and environment variables

### Documentation Index
- **[Documentation Index](docs/README.md)** - Overview of all documentation

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)

## 📝 Notes for Beginners

### What is Django?
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It handles many common web development tasks for you.

### What is PostgreSQL?
PostgreSQL is a powerful, open-source relational database system. It's more robust than SQLite (Django's default) and better for production applications.

### What is Supabase?
Supabase is a backend-as-a-service platform that provides a PostgreSQL database in the cloud. It's like Firebase but uses PostgreSQL instead of NoSQL.

### Why Virtual Environment?
Think of it as a separate "workspace" for each project. Without it, all your Python projects would share the same packages, which can cause conflicts.

## 🤝 Contributing

This is a learning project. Feel free to experiment and ask questions!

## 📄 License

[Your License Here]

