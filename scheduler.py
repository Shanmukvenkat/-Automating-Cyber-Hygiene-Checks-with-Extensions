import schedule
import time
from main import run_cyber_hygiene_check, send_email_report # type: ignore

# === Configuration ===
IP_ADDRESS = "127.0.0.1"           # Target IP to scan
SCAN_DIRECTORY = None               # Directory to scan for malware, or specify a path

SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_email_password"
RECIPIENT_EMAIL = "recipient_email@example.com"

def job():
    print("Starting scheduled cyber hygiene check...")
    report_path = run_cyber_hygiene_check(IP_ADDRESS, SCAN_DIRECTORY)
    if report_path:
        subject = f"Scheduled Cyber Hygiene Report for {IP_ADDRESS}"
        body = "This is an automated scheduled report."
        success = send_email_report(SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL, subject, body, report_path)
        if success:
            print("Report emailed successfully.")
        else:
            print("Failed to send email.")
    else:
        print("Failed to generate report.")

# Schedule to run every day at 8:00 AM
schedule.every().day.at("08:00").do(job)

print("Scheduler started. Waiting for jobs...")

while True:
    schedule.run_pending()
    time.sleep(1)
