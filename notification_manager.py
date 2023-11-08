import smtplib
import os

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

class NotificationManager:
    def send_mail(self, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message)
