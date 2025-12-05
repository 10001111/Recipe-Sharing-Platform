# 🚀 Complete Setup Guide - Milestone 1.1

## Welcome, Beginner Developer! 👋

This guide will walk you through setting up your Recipe Sharing Platform development environment step by step. Think of this as building the foundation of a house - we need to get everything ready before we can start building features!

---

## 📚 Understanding What We're Building

Before we start, let's understand what each tool does:

### **Python** 🐍
- **What it is**: A programming language that's easy to learn and powerful
- **Why we use it**: Django (our web framework) is built with Python
- **Think of it as**: The language we'll write our code in

### **Django** 🎸
- **What it is**: A web framework - think of it as a toolkit for building websites
- **Why we use it**: It handles a lot of complex web stuff automatically (like database connections, user authentication, etc.)
- **Think of it as**: The foundation and tools for our website

### **PostgreSQL** 🐘
- **What it is**: A database system - where we store all our data (recipes, users, etc.)
- **Why we use it**: More powerful than SQLite (Django's default), better for real applications
- **Think of it as**: A filing cabinet for all our website's information

### **Supabase** ☁️
- **What it is**: A cloud service that gives us a PostgreSQL database online
- **Why we use it**: We don't have to install PostgreSQL locally, and it's free to start
- **Think of it as**: A filing cabinet in the cloud that we can access from anywhere

### **Virtual Environment** 📦
- **What it is**: An isolated space for our project's Python packages
- **Why we use it**: Keeps our project's dependencies separate from other projects
- **Think of it as**: A separate toolbox just for this project

### **Git** 📝
- **What it is**: Version control system - tracks changes to our code
- **Why we use it**: Saves our work history, lets us go back if something breaks
- **Think of it as**: A time machine for our code

---

## ✅ Step-by-Step Setup

### Step 1: Verify Python Installation

**What we're doing**: Checking if Python is installed correctly

**Command**:
```bash
python --version
```

**Expected output**: `Python 3.9.x` or higher (we saw 3.13.7, which is perfect!)

**If it doesn't work**: 
- Download Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

---

### Step 2: Create Virtual Environment ✅ (Already Done!)

**What we're doing**: Creating an isolated environment for our project

**Command** (already executed):
```bash
python -m venv venv
```

**What happened**: A folder called `venv` was created. This contains Python and will contain all our project's packages.

**Why it matters**: Without this, installing packages would affect your entire system. With it, each project stays separate.

---

### Step 3: Activate Virtual Environment

**What we're doing**: "Turning on" our virtual environment so we use the right Python

**Command** (Windows PowerShell):
```powershell
.\venv\Scripts\Activate.ps1
```

**Command** (Windows Command Prompt):
```cmd
venv\Scripts\activate.bat
```

**Command** (Mac/Linux):
```bash
source venv/bin/activate
```

**How you know it worked**: You'll see `(venv)` at the start of your command prompt, like this:
```
(venv) PS C:\Users\lll\.vscode\Recipe-Sharing-Platform>
```

**Important**: You need to activate the virtual environment every time you open a new terminal window!

---

### Step 4: Install Dependencies ✅ (Already Done!)

**What we're doing**: Installing all the Python packages our project needs

**Command** (already executed):
```bash
pip install -r requirements.txt
```

**What happened**: Python downloaded and installed:
- Django (our web framework)
- psycopg2-binary (lets Python talk to PostgreSQL)
- djangorestframework (for building APIs)
- And many more helpful tools

**Think of it as**: Unpacking all the tools we need for our project

---

### Step 5: Set Up Supabase Database

**What we're doing**: Creating a cloud database for our project

#### 5.1: Create Supabase Account
1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" or "Sign up"
3. Sign up with GitHub (easiest) or email

#### 5.2: Create a New Project
1. Click "New Project"
2. Fill in:
   - **Name**: `recipe-sharing-platform` (or any name you like)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to you
   - **Pricing Plan**: Free tier is fine for now
3. Click "Create new project"
4. Wait 2-3 minutes for setup to complete

#### 5.3: Get Your Database Credentials
1. In your Supabase project dashboard, click "Settings" (gear icon)
2. Click "Database" in the left sidebar
3. Scroll down to "Connection string"
4. You'll see something like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. Also note:
   - **Host**: `db.xxxxx.supabase.co`
   - **Database name**: Usually `postgres`
   - **User**: Usually `postgres`
   - **Port**: `5432`
   - **Password**: The one you created

#### 5.4: Get API Keys (for later use)
1. Still in Settings, click "API"
2. Note down:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon/public key**: Long string starting with `eyJ...`
   - **service_role key**: Another long string (keep this secret!)

---

### Step 6: Configure Environment Variables

**What we're doing**: Setting up configuration that Django will use

**Why**: We don't want to hardcode passwords and secrets in our code!

**🔒 IMPORTANT**: Read [SECURITY.md](SECURITY.md) first to understand why this matters!

1. Create a file named `.env` in the project root (same folder as `manage.py`)

2. Copy from `env.example` and fill in your Supabase details:

```bash
# Windows
copy env.example .env

# Mac/Linux
cp env.example .env
```

3. Edit `.env` and replace all the `your-...` values with your actual Supabase credentials

**Important**: The `.env` file is in `.gitignore`, so it won't be uploaded to Git (this is good for security!)

---

### Step 7: Generate SECRET_KEY

**What we're doing**: Creating a secure secret key for Django

**Command**:
```bash
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Or use our helper script**:
```bash
python scripts/generate_secret_key.py
```

**Copy the generated key** and paste it into your `.env` file as `SECRET_KEY=your-generated-key-here`

---

### Step 8: Test Database Connection

**What we're doing**: Making sure Django can talk to our Supabase database

**Command** (make sure venv is activated):
```bash
python manage.py check --database default
```

**Expected output**: Should say "System check identified no issues"

**If you get errors**: 
- Double-check your `.env` file
- Make sure all credentials are correct
- Ensure your Supabase project is fully set up (wait a few more minutes)

---

### Step 9: Run Database Migrations

**What we're doing**: Creating the initial database tables that Django needs

**Command**:
```bash
python manage.py migrate
```

**What happened**: Django created tables in your Supabase database for:
- Users
- Sessions
- Admin interface
- And more

**Think of it as**: Setting up the basic structure in your filing cabinet

---

### Step 10: Create a Superuser (Admin Account)

**What we're doing**: Creating an admin account so you can access Django's admin panel

**Command**:
```bash
python manage.py createsuperuser
```

**You'll be asked for**:
- Username: (choose anything, like `admin`)
- Email: (your email)
- Password: (create a password)

**Important**: Remember these credentials! You'll use them to log into the admin panel.

---

### Step 11: Run the Development Server

**What we're doing**: Starting Django's built-in web server so we can see our site

**Command**:
```bash
python manage.py runserver
```

**Expected output**: 
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**What to do**:
1. Open your web browser
2. Go to `http://127.0.0.1:8000`
3. You should see Django's welcome page! 🎉

**To see the admin panel**:
- Go to `http://127.0.0.1:8000/admin`
- Log in with your superuser credentials

**To stop the server**: Press `CTRL+C` in the terminal

---

### Step 12: Initialize Git Repository ✅ (Already Done!)

**What we're doing**: Setting up version control for our project

**Command** (already executed):
```bash
git init
```

**What happened**: Git started tracking changes in your project folder

**Next steps** (when you're ready):
```bash
git add .
git commit -m "Initial commit: Milestone 1.1 - Development environment setup"
```

---

## 🎯 Project Structure Explained

Let me explain what each folder/file does:

```
Recipe-Sharing-Platform/
├── config/              # Django project settings (like the brain of the project)
│   ├── settings.py      # All configuration (database, apps, etc.)
│   ├── urls.py          # URL routing (which URL goes to which page)
│   └── wsgi.py          # Server configuration
│
├── apps/                # Where we'll create our Django apps (recipes, users, etc.)
│   └── __init__.py      # Makes Python recognize this as a package
│
├── docs/                # All project documentation
│   ├── README.md        # Documentation index
│   ├── SETUP_GUIDE.md   # This file!
│   └── SECURITY.md      # Security best practices
│
├── static/              # CSS, JavaScript, images (frontend files)
├── media/               # User-uploaded files (recipe images, etc.)
├── templates/           # HTML templates (the structure of our web pages)
│
├── scripts/             # Helper scripts
│   └── generate_secret_key.py
│
├── venv/                # Virtual environment (don't edit this!)
├── .env                 # Environment variables (your secrets - not in Git!)
├── env.example          # Template for .env file (safe to commit)
├── .gitignore           # Tells Git what files to ignore
├── requirements.txt     # List of all Python packages we need
├── manage.py            # Django's command-line tool
└── README.md            # Project overview (in root)
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "python: command not found"
**Solution**: Python isn't in your PATH. Reinstall Python and check "Add to PATH"

### Issue 2: "pip: command not found"
**Solution**: Make sure your virtual environment is activated

### Issue 3: "Cannot connect to database"
**Solutions**:
- Check your `.env` file has correct credentials
- Make sure Supabase project is fully initialized (wait 2-3 minutes)
- Verify your IP is allowed in Supabase (Settings > Database > Connection Pooling)

### Issue 4: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and run `pip install -r requirements.txt`

### Issue 5: PowerShell execution policy error
**Solution**: Run this in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 6: "SECRET_KEY not found" error
**Solution**: Make sure you've created `.env` file and added `SECRET_KEY=your-key-here`

---

## ✅ Checklist: Are You Ready?

Before moving to the next milestone, make sure:

- [x] Python is installed and working
- [x] Virtual environment is created
- [x] All dependencies are installed
- [ ] Supabase account is created
- [ ] Supabase project is set up
- [ ] `.env` file is configured with correct credentials
- [ ] SECRET_KEY is generated and added to `.env`
- [ ] Database migrations ran successfully
- [ ] Superuser account is created
- [ ] Development server runs without errors
- [ ] You can access `http://127.0.0.1:8000`
- [ ] You can log into admin panel at `http://127.0.0.1:8000/admin`
- [x] Git repository is initialized

---

## 🎓 What You've Learned

Congratulations! You've just set up a professional development environment. Here's what you accomplished:

1. **Virtual Environment**: You learned why we isolate project dependencies
2. **Package Management**: You installed packages using `requirements.txt`
3. **Cloud Database**: You set up Supabase (PostgreSQL in the cloud)
4. **Environment Variables**: You learned to keep secrets out of code
5. **Django Basics**: You ran migrations and created a superuser
6. **Version Control**: You initialized Git for tracking changes

---

## 🚀 Next Steps

Once everything is working, you're ready for:
- **Milestone 1.2**: Creating your first Django app
- **Milestone 1.3**: Setting up models (database structure)
- **Milestone 1.4**: Creating views and templates

---

## 📖 Additional Resources

- [Django Official Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Supabase Documentation](https://supabase.com/docs)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [Security Best Practices](SECURITY.md) - Read this!

---

## 💡 Pro Tips

1. **Always activate your virtual environment** before working on the project
2. **Never commit `.env`** to Git (it's already in `.gitignore`)
3. **Test your setup** by running the server before moving on
4. **Keep your Supabase password safe** - you'll need it!
5. **Use the admin panel** - it's a great way to see your data
6. **Read SECURITY.md** - Understanding security is crucial!

---

**Questions?** Don't hesitate to ask! Every expert was once a beginner. 🎉

