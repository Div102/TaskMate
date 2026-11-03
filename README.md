# TaskMate

TaskMate is a Django task manager for organizing assignments, tracking status, and monitoring deadlines.

## Run locally

From the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

For production, set `DJANGO_DEBUG=False` and provide a private `DJANGO_SECRET_KEY` through the environment.
