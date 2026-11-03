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

## Deploy to Vercel

Vercel runs this Django application; GitHub Pages cannot run the Django backend or save tasks. TaskMate is currently a public demo with no login, so do not enter personal or sensitive information.

1. Import [Div102/TaskMate](https://github.com/Div102/TaskMate) as a new project at [vercel.com/new](https://vercel.com/new). Vercel detects the Django app from `manage.py`.
2. In the Vercel project, add a PostgreSQL integration from the [Marketplace](https://vercel.com/marketplace?category=storage&search=postgres). Make sure it provides `DATABASE_URL` to the Production environment.
3. Set these Production environment variables:
   - `DJANGO_DEBUG` to `False`
   - `DJANGO_SECRET_KEY` to a newly generated, private value (for example, generate one locally with `python -c "import secrets; print(secrets.token_urlsafe(50))"`). Never commit it.
   - `DJANGO_ALLOWED_HOSTS` to `.vercel.app`, plus any custom domain you add, separated by commas.
4. Deploy the project. Vercel collects and serves static files from `STATIC_ROOT`.
5. After linking the project with the Vercel CLI and setting up its production database, run the initial schema migration from this project directory:

   ```powershell
   vercel env run -e production -- python manage.py migrate
   ```

`DATABASE_URL` is used for PostgreSQL in production; local development continues to use the ignored `db.sqlite3` file. Configure a separate database for Preview deployments if you enable them.
