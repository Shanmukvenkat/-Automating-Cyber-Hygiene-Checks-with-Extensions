# Security Policy

## Supported Versions

Currently supported versions of this cybersecurity automation tool:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this cybersecurity tool, please report it responsibly:

### How to Report

**Please DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, please email security reports to: **shanmukvenkatad@gmail.com**

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes (if you have them)

### What to Expect

- **Response Time**: I will acknowledge receipt within 48 hours
- **Investigation**: I will investigate and respond with my findings within 7 days
- **Resolution**: Critical issues will be patched within 14 days when possible
- **Credit**: Security researchers will be credited in the changelog (unless they prefer to remain anonymous)

### Security Best Practices for Users

When using this tool:

1. **Keep credentials secure**: Never commit real passwords or API keys to version control
2. **Use environment variables**: Store sensitive configuration in `.env` files
3. **Regular updates**: Keep dependencies updated to patch known vulnerabilities
4. **Principle of least privilege**: Run scans with minimal required permissions
5. **Secure communications**: Use encrypted channels for sending security reports
6. **Validate inputs**: Be cautious when scanning untrusted systems or networks

### Scope

This security policy covers:
- The main application code
- Configuration handling
- Email notification system
- Report generation functionality
- GUI components

### Out of Scope

- Third-party dependencies (report directly to their maintainers)
- Issues in systems being scanned (this tool is for detection, not exploitation)
- Social engineering or physical security issues

## Contact

**Shanmuk Venkat Davuluri**  
Cybersecurity Graduate Student  
Quinnipiac University  
Email: [shanmukvenkatad@gmail.com](mailto:shanmukvenkatad@gmail.com)

---

*This security policy is effective as of June 2025 and may be updated as the project evolves.*