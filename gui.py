import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import re
from datetime import datetime

from main import run_cyber_hygiene_check, send_email_report


class CyberHygieneApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Hygiene Tool")
        self.geometry("600x550")

        # Variables
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.directory_var = tk.StringVar()
        self.sender_email_var = tk.StringVar()
        self.sender_password_var = tk.StringVar()
        self.recipient_email_var = tk.StringVar()

        self.password_visible = False

        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # IP Address
        ttk.Label(self, text="IP Address to Scan:").grid(row=0, column=0, sticky="w", **padding)
        ttk.Entry(self, textvariable=self.ip_var, width=30).grid(row=0, column=1, **padding)

        # Directory to scan
        ttk.Label(self, text="Directory to Scan for Malware:").grid(row=1, column=0, sticky="w", **padding)
        dir_frame = ttk.Frame(self)
        dir_frame.grid(row=1, column=1, sticky="w", **padding)
        ttk.Entry(dir_frame, textvariable=self.directory_var, width=25).pack(side="left")
        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).pack(side="left", padx=5)

        # Sender Email
        ttk.Label(self, text="Sender Email:").grid(row=2, column=0, sticky="w", **padding)
        ttk.Entry(self, textvariable=self.sender_email_var, width=30).grid(row=2, column=1, **padding)

        # Sender Password
        ttk.Label(self, text="Sender Email Password:").grid(row=3, column=0, sticky="w", **padding)
        pwd_frame = ttk.Frame(self)
        pwd_frame.grid(row=3, column=1, sticky="w", **padding)
        self.sender_password_entry = ttk.Entry(pwd_frame, textvariable=self.sender_password_var, width=25, show="*")
        self.sender_password_entry.pack(side="left")
        ttk.Button(pwd_frame, text="Show", command=self.toggle_password).pack(side="left", padx=5)

        # Recipient Email
        ttk.Label(self, text="Recipient Email:").grid(row=4, column=0, sticky="w", **padding)
        ttk.Entry(self, textvariable=self.recipient_email_var, width=30).grid(row=4, column=1, **padding)

        # Status Text box
        ttk.Label(self, text="Status:").grid(row=5, column=0, sticky="nw", **padding)
        self.status_text = tk.Text(self, height=12, width=60, state="disabled")
        self.status_text.grid(row=5, column=1, **padding)

        # Start Button
        self.start_button = ttk.Button(self, text="Start Scan and Send Report", command=self.start_scan)
        self.start_button.grid(row=6, column=0, columnspan=2, pady=15)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory_var.set(directory)

    def log(self, message):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{timestamp} {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.sender_password_entry.config(show="" if self.password_visible else "*")

    def start_scan(self):
        self.start_button.config(state="disabled")
        self.status_text.config(state="normal")
        self.status_text.delete("1.0", tk.END)
        self.status_text.config(state="disabled")

        threading.Thread(target=self.scan_and_email).start()

    def scan_and_email(self):
        ip = self.ip_var.get().strip()
        directory = self.directory_var.get().strip()
        sender_email = self.sender_email_var.get().strip()
        sender_password = self.sender_password_var.get()
        recipient_email = self.recipient_email_var.get().strip()

        if not self.validate_inputs(ip, directory, sender_email, recipient_email):
            self.start_button.config(state="normal")
            return

        self.log(f"Starting scan for IP: {ip}")
        try:
            import main
            original_get_scan_directory = main.get_scan_directory
            main.get_scan_directory = lambda: directory

            report_path = run_cyber_hygiene_check(ip)
            main.get_scan_directory = original_get_scan_directory

            if not report_path:
                self.log("Report generation failed.")
                self.start_button.config(state="normal")
                return

            self.log(f"Report generated: {report_path}")
            self.log("Sending email...")

            send_email_report(sender_email, sender_password, recipient_email,
                              f"Cyber Hygiene Report for {ip}",
                              "Please find the attached cyber hygiene report.",
                              report_path)

            self.log("Email sent successfully.")
        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.start_button.config(state="normal")

    def validate_inputs(self, ip, directory, sender_email, recipient_email):
        if not ip:
            self.log("IP address cannot be empty.")
            return False

        if not directory or not os.path.isdir(directory):
            self.log("Invalid directory. Please select a valid directory for malware scan.")
            return False

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, sender_email) or not re.match(email_regex, recipient_email):
            self.log("Invalid email address format.")
            return False

        return True


if __name__ == "__main__":
    app = CyberHygieneApp()
    app.mainloop()
