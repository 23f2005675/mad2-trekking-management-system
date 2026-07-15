import csv
import io
import os
import logging
from datetime import datetime, timedelta

from celery import Celery
from celery.schedules import crontab
from flask import current_app

from config import Config

logger = logging.getLogger(__name__)

# Initialize the global Celery instance (configuration will be loaded in init_celery)
celery = Celery("trekking_tasks")

# Define the scheduled beat tasks on the celery instance
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
    Configure Celery using Flask application configuration and attach Flask application context.
    """
    celery.conf.update(
        broker_url=app.config.get("CELERY_BROKER_URL"),
        result_backend=app.config.get("CELERY_RESULT_BACKEND"),
        timezone=app.config.get("CELERY_TIMEZONE", "UTC"),
        beat_schedule=celery.conf.beat_schedule,
    )

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
    from mailer import send_email

    tomorrow = datetime.utcnow().date() + timedelta(days=1)

    bookings = Booking.query.filter_by(
        status="Booked"
    ).all()

    success_count = 0
    failure_count = 0

    for booking in bookings:
        if booking.trek and booking.trek.start_date == tomorrow:
            user = booking.user
            trek = booking.trek

            if not user or not user.email:
                logger.warning(f"Booking {booking.id} has no valid user or email address.")
                continue

            subject = "Trek Reminder - Your Trek Starts Tomorrow"
            body = f"""Hello {user.name},

This is a reminder that your trek:

{trek.name}

starts tomorrow.

Location:
{trek.location}

Start Date:
{trek.start_date}

Please report on time and carry all required trekking equipment.

Have a safe and enjoyable trek!

Regards,
Trekking Management Team"""

            try:
                # Actually send the email using SMTP configuration
                sent = send_email(user.email, subject, body)
                if sent:
                    success_count += 1
                    logger.info(f"Successfully sent daily trek reminder email to {user.email} (Booking ID: {booking.id})")
                else:
                    failure_count += 1
                    logger.error(f"Failed to send daily trek reminder email to {user.email} (Booking ID: {booking.id})")
            except Exception as e:
                failure_count += 1
                logger.error(f"Error while sending daily trek reminder email to {user.email}: {e}")

    return f"Sent {success_count} reminder(s) successfully, failed {failure_count} reminder(s)."


# ---------------------------------------------------------
# Monthly Report
# ---------------------------------------------------------

@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():
    from models import Trek, Booking, User
    from mailer import send_email

    total_users = User.query.filter_by(role="User").count()
    total_staff = User.query.filter_by(role="Trek Staff").count()
    total_treks = Trek.query.count()
    total_bookings = Booking.query.count()

    generation_date = datetime.utcnow().strftime("%d-%m-%Y %H:%M")

    html = f"""<html>
<head>
    <title>Monthly Report</title>
</head>

<body>

    <h1>Trekking Management System</h1>

    <h2>Monthly Report</h2>

    <p>
        Generated On :
        {generation_date}
    </p>

    <hr>

    <ul>
        <li>Total Users : {total_users}</li>
        <li>Total Staff : {total_staff}</li>
        <li>Total Treks : {total_treks}</li>
        <li>Total Bookings : {total_bookings}</li>
    </ul>

</body>
</html>
"""

    reports_dir = os.path.join(
        current_app.instance_path,
        "reports"
    )

    os.makedirs(reports_dir, exist_ok=True)

    filename = (
        "monthly_report_"
        + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        + ".html"
    )

    filepath = os.path.join(reports_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(html)
        logger.info(f"Successfully generated and saved local monthly report at {filepath}")
    except Exception as e:
        logger.error(f"Failed to write local copy of monthly report: {e}")

    admin_email = "admin@trek.com"
    email_subject = "Monthly Trekking Report"
    email_body = f"""Hello Admin,

Please find attached the Monthly Trekking Report for the Trekking Management System.

Report Details:
- Generated On: {generation_date}
- Total Users: {total_users}
- Total Staff: {total_staff}
- Total Treks: {total_treks}
- Total Bookings: {total_bookings}

Regards,
Trekking Management Team"""

    try:
        sent = send_email(
            to_email=admin_email,
            subject=email_subject,
            body=email_body,
            attachment_path=filepath
        )
        if sent:
            logger.info(f"Successfully emailed monthly report to {admin_email}")
        else:
            logger.error(f"Failed to email monthly report to {admin_email}")
    except Exception as e:
        logger.error(f"Error while emailing monthly report to {admin_email}: {e}")

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
            booking.trek.name if booking.trek else None,
            booking.booking_date,
            booking.status,
            booking.payment_status
        ])

    export_dir = os.path.join(
        current_app.instance_path,
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