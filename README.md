# Trekking Management System

An academic project (IIT Madras MAD2) built with Flask (REST API) and Vue 3.
Three roles: **Admin**, **Trek Staff**, **User**.

## Tech Stack
- Backend: Python, Flask, Flask-RESTful routing, SQLAlchemy, Flask-JWT-Extended, Flask-CORS
- Frontend: Vue 3, Vue Router, Axios, Bootstrap 5
- Database: SQLite
- Caching: Redis
- Batch Jobs: Celery + Redis

## Prerequisites
- Python 3.10+
- Node.js 18+
- Redis server installed and runnable locally (`redis-server`)

## Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API runs at `http://localhost:5000`.

On first run, a default Admin account is created automatically:
- Email: `admin@trek.com`
- Password: `admin123`

### Redis
Make sure Redis is running before starting the backend, otherwise caching is
silently skipped (the app still works without it):

```bash
redis-server
```

### Celery (optional, for batch jobs)
In separate terminals, from the `backend` folder (with the venv activated):

```bash
# Worker - executes tasks
celery -A tasks.celery worker --loglevel=info

# Beat - schedules the daily reminder and monthly report
celery -A tasks.celery beat --loglevel=info
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173` and talks to the API at
`http://localhost:5000/api`.

## Roles

| Role       | How the account is created         | Key abilities                                             |
|------------|-------------------------------------|-------------------------------------------------------------|
| Admin      | Auto-created on first backend run   | Manage treks, staff, users, view dashboard stats            |
| Trek Staff | Created by Admin only               | Manage assigned treks, update slots/status, view participants|
| User       | Self-registers                      | Browse/search/book treks, manage bookings, update profile    |

## Project Structure

```
mad2-trekking-management-system/
  backend/       Flask REST API
  frontend/      Vue 3 SPA
  report/        Project report (add your write-up here)
```

## Notes
- The database file is created automatically at `backend/instance/trekking.db`.
- JWT tokens are stored in the browser's localStorage on the frontend.
- Redis caching is used for the trek listing/search endpoint (60s TTL) and is
  invalidated whenever a trek or booking changes.
