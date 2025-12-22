import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apscheduler.schedulers.background import BackgroundScheduler
from database.fetchData import fetchCSV

# ==================================================
# global vars
# ==================================================

scheduler = BackgroundScheduler()

# ==================================================
# methods
# ==================================================

def send_html_email(html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Scheduled CSV Result"
    msg["From"] = "noreply@lastro1"
    msg["To"] = "thomasfresco@live.com"
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP("localhost", 25) as server:
        server.send_message(msg)

def jobToAppContext(app, jobFunction):
    with app.app_context():
        try:
            result = jobFunction()
            send_html_email(result)
            print("Scheduled CSV fetch completed.")
        except Exception as e:
            print(f"Error in scheduled CSV fetch: {e}")

# ==================================================
# init and clean methods
# ==================================================

def initScheduler(app):
    scheduler.add_job(
        func=lambda: jobToAppContext(app, fetchCSV),
        trigger='cron',
        hour=0, minute=10,
        timezone='Europe/Lisbon',
        id='fetchCSV_job',
        name='Fetch CSV Data',
        replace_existing=True
    )

    scheduler.start()

def cleanScheduler():
    if scheduler.running:
        scheduler.shutdown(wait=True)
