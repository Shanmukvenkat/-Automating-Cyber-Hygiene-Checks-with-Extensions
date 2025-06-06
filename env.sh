# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password
RECIPIENT_EMAIL=security-team@yourcompany.com

# API Keys (if you add integrations later)
# SHODAN_API_KEY=your-shodan-api-key
# VIRUSTOTAL_API_KEY=your-virustotal-api-key

# Security Settings
ENCRYPTION_KEY=your-32-character-encryption-key-here
MAX_SCAN_THREADS=5
SCAN_TIMEOUT=300

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/security_scanner.log

# Database (if you add database support)
# DATABASE_URL=sqlite:///scanner.db

# Notification Settings
ENABLE_EMAIL_ALERTS=true
ALERT_THRESHOLD=medium