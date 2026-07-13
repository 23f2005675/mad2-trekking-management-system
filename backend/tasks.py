import csv
import io
import os
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab

from config import Config

celery = Celery(
    "trekking_tasks",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND
)

# Scheduled Tasks
celery.conf.beat_schedule = {
    "daily-reminder": {
        "task": "tasks.send_daily_reminders",
        "schedule": crontab(hour=8, minute=0),
    },
    "monthly-report": {
        "task": "tasks.generate_monthly_report",
        "schedule": crontab(day_of_month=1, hour=0, minute=0),
    },
}


def init_celery(app):
    """
    Attach Flask application context to Celery.
    """

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


# ---------------------------------------------------------
# Daily Reminder Task
# ---------------------------------------------------------

@celery.task(name="tasks.send_daily_reminders")
def send_daily_reminders():

    from models import Booking

    tomorrow = datetime.utcnow().date() + timedelta(days=1)

    bookings = Booking.query.filter_by(
        status="Booked"
    ).all()

    reminder_count = 0

    for booking in bookings:

        if booking.trek and booking.trek.start_date == tomorrow:

            print(
                f"[REMINDER] {booking.user.name} "
                f"- Trek '{booking.trek.name}' starts tomorrow."
            )

            reminder_count += 1

    return f"Sent {reminder_count} reminder(s)."


# ---------------------------------------------------------
# Monthly Report
# ---------------------------------------------------------

@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():

    from models import Trek, Booking, User

    html = f"""
    <html>
    <head>
        <title>Monthly Report</title>
    </head>

    <body>

        <h1>Trekking Management System</h1>

        <h2>Monthly Report</h2>

        <p>
            Generated On :
            {datetime.utcnow().strftime("%d-%m-%Y %H:%M")}
        </p>

        <hr>

        <ul>
            <li>Total Users : {User.query.filter_by(role="User").count()}</li>
            <li>Total Staff : {User.query.filter_by(role="Trek Staff").count()}</li>
            <li>Total Treks : {Trek.query.count()}</li>
            <li>Total Bookings : {Booking.query.count()}</li>
        </ul>

    </body>
    </html>
    """

    reports_dir = os.path.join(
        os.path.dirname(__file__),
        "instance",
        "reports"
    )

    os.makedirs(reports_dir, exist_ok=True)

    filename = (
        "monthly_report_"
        + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        + ".html"
    )

    filepath = os.path.join(reports_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html)

    return filepath


# ---------------------------------------------------------
# Booking History Export
# ---------------------------------------------------------

@celery.task(name="tasks.export_booking_history_task")
def export_booking_history_task(user_id):

    from models import Booking

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Booking ID",
        "Trek Name",
        "Booking Date",
        "Status",
        "Payment Status"
    ])

    for booking in bookings:

        writer.writerow([
            booking.id,
            booking.trek.name,
            booking.booking_date,
            booking.status,
            booking.payment_status
        ])

    export_dir = os.path.join(
        os.path.dirname(__file__),
        "instance",
        "exports"
    )

    os.makedirs(export_dir, exist_ok=True)

    filename = (
        f"booking_history_user_{user_id}_"
        + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    filepath = os.path.join(export_dir, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(output.getvalue())

    return filepath