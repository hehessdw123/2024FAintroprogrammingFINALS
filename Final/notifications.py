from plyer import notification
import smtplib
from email.mime.text import MIMEText

def send_desktop_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

def send_email_notification(recipient, subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(config["email"], config["email_password"])

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = config["email"]
        msg["To"] = recipient

        server.sendmail(config["email"], recipient, msg.as_string())
