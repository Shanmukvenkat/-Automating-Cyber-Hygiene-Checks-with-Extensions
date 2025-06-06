import socket
import threading
import os
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime
import getpass
import logging
import subprocess
from malware_scan import malware_scan
from software_check import get_installed_software, check_outdated_software  # type: ignore
import html

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global configurations
weak_passwords_path = "data/weak_passwords.txt"
report_folder = "reports"
port_scan_threads = 100
default_ip = "127.0.0.1"

# Helper functions
def scan_port(ip, port, results):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            results[port] = "Open" if result == 0 else "Closed"
    except Exception:
        results[port] = "Error"

def perform_port_scan(ip):
    results = {}
    threads = []
    for port in range(1, 1025):
        t = threading.Thread(target=scan_port, args=(ip, port, results))
        threads.append(t)
        t.start()
        if len(threads) >= port_scan_threads:
            for thread in threads:
                thread.join()
            threads = []
    for thread in threads:
        thread.join()
    return results

def check_weak_passwords(passwords, weak_passwords):
    weak_detected = []
    failed_criteria = []

    for pwd in passwords:
        criteria = []
        if len(pwd) < 8:
            criteria.append("Too short")
        if not any(c.isupper() for c in pwd):
            criteria.append("Missing uppercase letter")
        if not any(c.islower() for c in pwd):
            criteria.append("Missing lowercase letter")
        if not any(c.isdigit() for c in pwd):
            criteria.append("Missing numeric digit")
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in pwd):
            criteria.append("Missing special character")

        if pwd in weak_passwords:
            weak_detected.append(pwd)

        if criteria:
            failed_criteria.append(f"{pwd}: {', '.join(criteria)}")

    return weak_detected, failed_criteria

def check_firewall():
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True)
        if "State ON" in result.stdout:
            return "Enabled"
        else:
            return "Disabled"
    except Exception as e:
        return f"Error checking firewall: {e}"

def send_email_report(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    except Exception as e:
        logging.error(f"Failed to attach report file: {e}")
        return False

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        logging.info("Email sent successfully.")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

def get_scan_directory():
    while True:
        user_input = input("Enter the directory to scan: ").strip()
        if os.path.exists(user_input) and os.path.isdir(user_input):
            return user_input
        else:
            print("Invalid directory. Please enter a valid directory path.")

def generate_html_report(ip_address, port_results, weak_detected, failed_criteria,
                         firewall_status, malware_results, installed_software, outdated_software, report_file_path):

    # HTML escape all user data for security
    def esc(text):
        return html.escape(str(text))

    open_ports = [port for port, status in port_results.items() if status == "Open"]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Cyber Hygiene Report for {esc(ip_address)}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; color: #333; }}
            h1, h2 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
            th {{ background-color: #2980b9; color: white; }}
            tr:nth-child(even) {{ background-color: #ecf0f1; }}
            .none {{ font-style: italic; color: #888; }}
        </style>
    </head>
    <body>
        <h1>Cyber Hygiene Report</h1>
        <p><strong>IP Address:</strong> {esc(ip_address)}</p>
        <p><strong>Report Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2>Open Ports</h2>
        {"<ul>" + "".join(f"<li>Port {esc(port)}</li>" for port in sorted(open_ports)) + "</ul>" if open_ports else '<p class="none">None</p>'}

        <h2>Weak Passwords Detected</h2>
        {"<ul>" + "".join(f"<li>{esc(pwd)}</li>" for pwd in weak_detected) + "</ul>" if weak_detected else '<p class="none">None</p>'}

        <h2>Passwords Failing Security Criteria</h2>
        {"<ul>" + "".join(f"<li>{esc(pwd)}</li>" for pwd in failed_criteria) + "</ul>" if failed_criteria else '<p class="none">None</p>'}

        <h2>Firewall Status</h2>
        <p>{esc(firewall_status)}</p>

        <h2>Malware Scan Results</h2>
        <p><strong>Malicious Files:</strong> {esc(', '.join(malware_results['malicious']) if malware_results and malware_results.get('malicious') else 'None' )}</p>
        <p><strong>Suspicious Files:</strong> {esc(', '.join(malware_results['suspicious']) if malware_results and malware_results.get('suspicious') else 'None' )}</p>

        <h2>Installed Software</h2>
        {f"<table><thead><tr><th>Name</th><th>Version</th></tr></thead><tbody>" +
         "".join(f"<tr><td>{esc(name)}</td><td>{esc(version)}</td></tr>" for name, version in installed_software) +
         "</tbody></table>" if installed_software else '<p class="none">No installed software information available.</p>'}

        <h2>Outdated Software</h2>
        {f"<table><thead><tr><th>Name</th><th>Installed Version</th><th>Latest Version</th></tr></thead><tbody>" +
         "".join(f"<tr><td>{esc(name)}</td><td>{esc(installed_v)}</td><td>{esc(latest_v)}</td></tr>" for name, installed_v, latest_v in outdated_software) +
         "</tbody></table>" if outdated_software else '<p class="none">None</p>'}

    </body>
    </html>
    """

    try:
        with open(report_file_path, "w", encoding="utf-8") as report_file:
            report_file.write(html_content)
        logging.info(f"HTML report saved to {report_file_path}")
    except Exception as e:
        logging.error(f"Failed to write HTML report: {e}")
        return False

    return True

def run_cyber_hygiene_check(ip_address, directory_to_scan=None):
    logging.info(f"Starting cyber hygiene check for {ip_address}")

    # Perform port scan
    port_results = perform_port_scan(ip_address)

    # Check weak passwords
    passwords_to_check = ["123456", "password", "Welcome1", "Admin123", "qwerty", "letmein", "iloveyou"]
    weak_passwords = []
    try:
        with open(weak_passwords_path, "r") as f:
            weak_passwords = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logging.warning(f"{weak_passwords_path} not found. Skipping weak password list check.")

    weak_detected, failed_criteria = check_weak_passwords(passwords_to_check, weak_passwords)

    # Check firewall status
    firewall_status = check_firewall()

    # Malware scan
    if directory_to_scan is None:
        directory_to_scan = get_scan_directory()
    malware_results = malware_scan(directory_to_scan)

    # Software check
    installed_software = get_installed_software()
    outdated_software = check_outdated_software(installed_software)

    # Generate report filename
    os.makedirs(report_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file_path = os.path.join(report_folder, f"cyber_hygiene_report_{timestamp}.html")

    if not generate_html_report(ip_address, port_results, weak_detected, failed_criteria,
                                firewall_status, malware_results, installed_software,
                                outdated_software, report_file_path):
        logging.error("Failed to generate the HTML report.")
        return None

    return report_file_path

def main():
    ip_address = input(f"Enter the IP address to scan (default: {default_ip}): ").strip() or default_ip
    report_path = run_cyber_hygiene_check(ip_address)
    if not report_path:
        logging.error("Report generation failed, aborting email sending.")
        return

    sender_email = input("Enter your email address (for sending report): ").strip()
    sender_password = getpass.getpass("Enter your email password (input hidden): ")
    recipient_email = input("Enter recipient's email address: ").strip()

    subject = f"Cyber Hygiene Report for {ip_address}"
    body = "Please find the attached cyber hygiene report."

    if not send_email_report(sender_email, sender_password, recipient_email, subject, body, report_path):
        logging.error("Failed to send the email report.")

if __name__ == "__main__":
    main()
