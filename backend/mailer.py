import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def send_email(to_email, subject, body, attachment_path=None):
    """
    Sends an email using SMTP configuration from Flask config.
    Supports attachments, SSL, and TLS.
    """
    smtp_server = current_app.config.get("SMTP_SERVER", "localhost")
    smtp_port = int(current_app.config.get("SMTP_PORT", 1025))
    smtp_username = current_app.config.get("SMTP_USERNAME", "")
    smtp_password = current_app.config.get("SMTP_PASSWORD", "")
    smtp_use_tls = current_app.config.get("SMTP_USE_TLS", False)
    smtp_use_ssl = current_app.config.get("SMTP_USE_SSL", False)
    sender = current_app.config.get("MAIL_DEFAULT_SENDER", "noreply@trek.com")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_email
    msg['Subject'] = subject

    # Body format
    if body.strip().startswith("<html") or body.strip().startswith("<!DOCTYPE html"):
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    # Attachment handling
    if attachment_path and os.path.exists(attachment_path):
        filename = os.path.basename(attachment_path)
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )
                msg.attach(part)
        except Exception as e:
            logger.error(f"Failed to attach file {attachment_path}: {e}")

    try:
        if smtp_use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)
            if smtp_use_tls:
                server.starttls()

        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)

        server.sendmail(sender, to_email, msg.as_string())
        server.quit()
        logger.info(f"Successfully sent email to {to_email} with subject: '{subject}'")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email} with subject: '{subject}'. Error: {e}")
        return False
