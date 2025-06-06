# Automating Cyber Hygiene Checks with Extensions - User Guide

**Author:** Shanmuk Venkat Davuluri  
**Student at:** Quinnipiac University (M.S. Cybersecurity)  
**Project Version:** 1.0  
**Documentation Updated:** June 2025

---

## About This Project

Hey there! Welcome to my cybersecurity automation project. I built this tool during my graduate studies because I got tired of manually checking for basic security issues on systems. You know how it is - weak passwords, sketchy open ports, potential malware - all the stuff that keeps security folks up at night.

This guide will walk you through everything you need to know to get this thing up and running. I've tried to make it as straightforward as possible, but if you run into issues, just hit me up through the contact info at the bottom.

## What's Inside This Guide

- Getting everything installed
- Setting up configurations  
- Actually running the tool
- Using the graphical interface I built
- Setting up automatic scans
- Making sense of the reports
- Fixing problems when they pop up
- Common questions people ask

---

## Getting Started - Installation

### Grab the Code

First thing - you need to download my project from GitHub:

```bash
git clone https://github.com/Shanmukvenkat/-Automating-Cyber-Hygiene-Checks-with-Extensions.git
cd -Automating-Cyber-Hygiene-Checks-with-Extensions
```

### Set Up Your Environment

I always recommend using a virtual environment. Trust me on this one - it saves you from dependency hell later:

```bash
# If you're on Windows
python -m venv venv
venv\Scripts\activate

# Mac or Linux folks
python3 -m venv venv
source venv/bin/activate
```

### Install What You Need

Once your virtual environment is active, install all the packages:

```bash
pip install -r requirements.txt
```

Make sure you've got Python 3.8 or newer. Anything older and you might run into weird issues.

---

## Setting Things Up

### Data Files You Need to Configure

Before you can actually use this tool, you need to set up a couple of text files:

**For Password Checking:**
- File: `data/weak_passwords.txt`
- What to do: Add common weak passwords you want to flag (one per line)
- Why: The tool checks against this list to identify risky passwords

**For Port Scanning:**
- File: `data/risky_ports.txt` 
- What to do: List port numbers that shouldn't normally be open (one per line)
- Why: Helps identify potentially dangerous open ports

### Email Notifications

Want to get alerts when the tool finds something? You'll need to configure email settings:

Open up `email_alerts.py` and update these settings:

```python
# SMTP server settings (I use Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Your email credentials
SENDER_EMAIL = "shanmukvenkat007@gmail.com"
SENDER_PASSWORD = "your-app-specific-password"

# Where to send alerts
RECIPIENT_EMAIL = "security-team@yourcompany.com"
```

Pro tip: Don't use your regular Gmail password. Set up an app-specific password instead - it's way more secure.

---

## Running the Tool

### Command Line Method

The simplest way to run a scan:

```bash
python main.py
```

Want more control? I built in some options:

```bash
# Full scan with email alerts
python main.py --scan-type full --email --output json

# Quick scan for daily checks
python main.py --scan-type quick --output text
```

### Using the GUI

If you're more of a point-and-click person, I built a graphical interface:

```bash
python gui.py
```

The GUI has three main sections:
- **Main dashboard** - Start scans and see progress
- **Reports viewer** - Look at past scan results  
- **Settings panel** - Configure email alerts and scan preferences

Pretty straightforward stuff. The interface updates in real-time so you can see what's happening.

---

## Automatic Scheduling

Nobody wants to remember to run security scans manually. Here's how to automate it:

### Windows Users

Use Task Scheduler:
1. Search for "Task Scheduler" in your start menu
2. Create a new basic task
3. Set it to run daily (or however often you want)
4. Point it to your Python executable and main.py file
5. Save and you're done

### Mac/Linux Users

Use cron jobs. Edit your crontab:

```bash
crontab -e
```

Add this line to run daily at 2 AM:
```bash
0 2 * * * /path/to/your/venv/bin/python /path/to/main.py
```

### Built-in Scheduler

I also included a scheduler in the tool itself. You can configure it in the settings or directly in `config.py`:

```python
SCHEDULE_ENABLED = True
SCHEDULE_FREQUENCY = "daily"
SCHEDULE_TIME = "02:00"
```

---

## Understanding Your Reports

Every scan creates a report in the `reports/` folder. The filename includes the date and time so you can track them easily: `report_20250606_143022.txt`

### What's in a Report

Each report has several sections:

**Summary at the top** - Quick overview of what was found and overall risk level

**Password Analysis** - Lists any weak passwords detected with strength ratings and suggestions for better ones

**Port Scan Results** - Shows open ports, what services are running, and potential security concerns

**Malware Detection** - Any suspicious files or activities found during the scan

**Recommendations** - My suggestions for fixing the issues, prioritized by risk level

### Report Formats

You can get reports in different formats depending on what you need:
- Text files for quick reading
- JSON for integrating with other tools
- HTML for viewing in a browser
- PDF for professional documentation

---

## Testing and Troubleshooting

### Running Tests

I included a test suite to make sure everything works correctly:

```bash
# Run all tests
python -m pytest tests/

# Test specific components
python -m pytest tests/test_password_checker.py
python -m pytest tests/test_port_scanner.py

# Verbose output to see what's happening
python -m pytest -v tests/
```

### Common Problems and How to Fix Them

**"Module not found" errors:**
This usually means the virtual environment isn't activated or dependencies aren't installed properly.

```bash
# Make sure virtual environment is active
source venv/bin/activate

# Reinstall everything
pip install -r requirements.txt
```

**Email alerts not working:**
Check your SMTP settings first. Gmail users need app-specific passwords, not regular passwords. Also make sure your firewall isn't blocking the connection.

**Slow performance:**
If scans are taking forever, try using quick scan mode for routine checks. You can also limit the port range or schedule intensive scans for off-hours.

**Permission errors on Linux/Mac:**
Make sure the script has execute permissions:
```bash
chmod +x main.py
```

---

## Questions People Ask Me

**Can I add my own security checks?**
Absolutely! The tool is modular. Just add new check modules to the `checks/` folder and integrate them into `main.py`. Follow the same pattern as the existing checks.

**How do I keep sensitive info secure?**
Use environment variables for credentials, encrypt config files if needed, and never commit passwords to version control. The `cryptography` library works well for encryption.

**Will this work on servers?**
Yes! It's lightweight and works great on Linux servers. You can containerize it with Docker or run it as a systemd service for production environments.

**What are the minimum requirements?**
Python 3.8+, about 512MB RAM, and 100MB disk space. Pretty minimal requirements.

**Can I integrate this with other security tools?**
Sure can! Use the JSON output format for API integration, set up webhooks for real-time alerts, or forward logs to your SIEM system.

**How do I whitelist certain findings?**
Create exception files in the config folder:
- `config/password_whitelist.txt` for approved passwords
- `config/port_whitelist.txt` for authorized ports
- `config/file_whitelist.txt` for trusted files

---

## My Story with This Project

I built this entire tool myself during my cybersecurity master's program at Quinnipiac University. It started as a simple script to check for weak passwords on lab systems, but I kept adding features as I encountered new security challenges.

Every piece of code, every test case, every feature was written with real-world usability in mind. I wanted something that actually works in practice, not just a theoretical exercise. The modular design means you can easily extend it for your specific needs.

This project represents months of late-night coding sessions, debugging mysterious errors, and testing on different systems. I'm proud of what it's become and hope it helps other people improve their security practices.

---

## Getting Help

If you run into problems or have suggestions:

**Bug reports and feature requests:** Open an issue at the [project repository](https://github.com/Shanmukvenkat/-Automating-Cyber-Hygiene-Checks-with-Extensions/issues)

**Direct contact:** Email me at [shanmukvenkatad@gmail.com](mailto:shanmukvenkatad@gmail.com)

**Check out my other work:** [github.com/Shanmukvenkat](https://github.com/Shanmukvenkat)

### Want to Contribute?

I welcome contributions from anyone interested in improving cybersecurity tools:
- Report bugs with detailed steps to reproduce
- Suggest new features with use cases
- Submit code improvements via pull requests
- Help improve documentation

---

**Contact Information:**

**Shanmuk Venkat Davuluri**  
M.S. Cybersecurity Student  
Quinnipiac University  
Email: [shanmukvenkatad@gmail.com](mailto:shanmukvenkatad@gmail.com)  
GitHub: [github.com/Shanmukvenkat](https://github.com/Shanmukvenkat)  
Project: [Automating Cyber Hygiene Checks](https://github.com/Shanmukvenkat/-Automating-Cyber-Hygiene-Checks-with-Extensions)

---

**Legal Stuff:** This project is open source under the MIT License. Use it responsibly and make sure you comply with your local laws and regulations. This tool is meant for legitimate security testing only.