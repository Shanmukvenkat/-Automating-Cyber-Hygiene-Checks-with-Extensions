import os
import re

def load_weak_passwords(file_path):
    weak_passwords = set()
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return weak_passwords

    with open(file_path, 'r') as file:
        for line in file:
            weak_passwords.add(line.strip())
    return weak_passwords

def load_passwords_to_check(file_path):
    passwords = []
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return passwords

    with open(file_path, 'r') as file:
        for line in file:
            passwords.append(line.strip())
    return passwords

def get_password_issues(password):
    issues = []
    if len(password) < 8:
        issues.append("Too short")
    if not re.search("[A-Z]", password):
        issues.append("Missing uppercase letter")
    if not re.search("[a-z]", password):
        issues.append("Missing lowercase letter")
    if not re.search("[0-9]", password):
        issues.append("Missing numeric digit")
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("Missing special character")
    return issues

def save_report(weak_passwords, failing_passwords, detailed_fails):
    os.makedirs("reports", exist_ok=True)
    report_path = "reports/weak_password_report.txt"

    with open(report_path, 'w') as report:
        report.write("Weak Passwords Detected:\n")
        for pwd in weak_passwords:
            report.write(f" - {pwd}\n")

        report.write("\nPasswords Failing Security Criteria:\n")
        for pwd, reasons in detailed_fails.items():
            report.write(f" - {pwd}: {', '.join(reasons)}\n")

    print(f"Report saved to {report_path}")

def main():
    weak_password_file = "data/weak_passwords.txt"
    passwords_file = "data/passwords_to_check.txt"

    weak_passwords = load_weak_passwords(weak_password_file)
    if not weak_passwords:
        print("No weak passwords loaded. Exiting.")
        return

    passwords = load_passwords_to_check(passwords_file)
    if not passwords:
        print("No passwords to check loaded. Exiting.")
        return

    weak_found = []
    failing_passwords = []
    detailed_fails = {}

    for pwd in passwords:
        if pwd in weak_passwords:
            weak_found.append(pwd)

        issues = get_password_issues(pwd)
        if issues:
            failing_passwords.append(pwd)
            detailed_fails[pwd] = issues

    if weak_found:
        print("Weak passwords detected:")
        for w in weak_found:
            print(f" - {w}")
    else:
        print("No weak passwords detected.")

    print("\nPasswords failing security criteria:")
    if failing_passwords:
        for pwd, reasons in detailed_fails.items():
            print(f" - {pwd}: {', '.join(reasons)}")
    else:
        print("None")

    save_report(weak_found, failing_passwords, detailed_fails)

if __name__ == "__main__":
    main()
