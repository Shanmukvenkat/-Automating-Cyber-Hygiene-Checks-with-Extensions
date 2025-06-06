# Contributing to Cybersecurity Automation Tool

Hey there! Thanks for your interest in contributing to my cybersecurity automation project. I built this during my graduate studies at Quinnipiac University, and I'm excited to have others help make it even better.

## Ways to Contribute

### 🐛 Bug Reports
Found something broken? Please report it!
- Check existing issues first to avoid duplicates
- Include your operating system and Python version
- Provide clear steps to reproduce the problem
- Share error messages and logs if available

### 💡 Feature Requests
Have an idea for improving the tool?
- Describe the feature and why it would be useful
- Explain the use case or problem it solves
- Consider if it fits the project's scope (cybersecurity hygiene checks)

### 🔧 Code Contributions
Want to submit code changes?
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Test thoroughly
- Submit a pull request

## Getting Started

### Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/Automating-Cyber-Hygiene-Checks-with-Extensions.git
cd Automating-Cyber-Hygiene-Checks-with-Extensions
```

2. **Set up your development environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Create your environment file**
```bash
cp .env.example .env
# Edit .env with your actual configuration
```

4. **Run the tests**
```bash
python -m pytest tests/
```

### Development Guidelines

#### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized

#### Testing
- Write tests for new features
- Ensure existing tests still pass
- Aim for good test coverage on critical security functions
- Test on different operating systems when possible

#### Security Considerations
- Never commit credentials or sensitive data
- Validate all inputs, especially for security scanning functions
- Follow secure coding practices
- Consider the principle of least privilege

## Project Structure

```
├── main.py                 # Main application entry point
├── gui.py                  # Graphical user interface
├── email_alerts.py         # Email notification system
├── config.py              # Configuration management
├── data/                  # Data files (passwords, ports, etc.)
├── tests/                 # Test suite
├── reports/               # Generated scan reports
├── checks/                # Individual security check modules
└── docs/                  # Documentation
```

## Coding Standards

### Adding New Security Checks

If you're adding a new security check module:

1. **Create a new file** in the `checks/` directory
2. **Follow the pattern**:
```python
class NewSecurityCheck:
    def __init__(self, config):
        self.config = config
    
    def run_check(self):
        """Run the security check and return results"""
        # Your implementation here
        return {
            'status': 'pass' or 'fail' or 'warning',
            'message': 'Description of findings',
            'details': {...}  # Additional data
        }
```

3. **Add tests** in `tests/test_new_check.py`
4. **Update documentation** in README.md

### Commit Messages

Use clear, descriptive commit messages:
```
Add password strength validation feature

- Implement NIST password guidelines
- Add entropy calculation
- Include common password detection
- Update tests and documentation
```

## Pull Request Process

1. **Create a descriptive PR title**
2. **Explain what you changed and why**
3. **Reference any related issues**
4. **Include screenshots for UI changes**
5. **Ensure all tests pass**
6. **Update documentation if needed**

### PR Checklist
- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No sensitive data is committed
- [ ] Security implications are considered

## Types of Contributions We're Looking For

### High Priority
- Additional security check modules
- Cross-platform compatibility improvements
- Performance optimizations
- Better error handling and logging

### Medium Priority
- GUI enhancements
- Additional output formats
- Integration with security tools
- Improved documentation

### Ideas for New Contributors
- Add support for checking SSL certificate validity
- Implement file integrity monitoring
- Create a web-based dashboard
- Add support for scanning network ranges
- Improve the scheduling system

## Recognition

Contributors will be recognized in:
- The project's README.md
- Release notes for significant contributions
- Academic presentations (with permission)

## Getting Help

Stuck on something? Here's how to get help:

- **GitHub Issues**: For bugs and feature requests
- **Email**: [shanmukvenkatad@gmail.com](mailto:shanmukvenkatad@gmail.com) for questions
- **Documentation**: Check the README.md and code comments

## Code of Conduct

This project follows basic principles of respect and collaboration:
- Be respectful and constructive in discussions
- Focus on the technical aspects of contributions
- Help maintain a welcoming environment for all contributors
- Remember that this is a learning project from a graduate student

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

This is my first major open-source project, so I'm learning too! If you have suggestions for improving this contribution process, please let me know.

**Shanmuk Venkat Davuluri**  
M.S. Cybersecurity Student  
Quinnipiac University  
[shanmukvenkatad@gmail.com](mailto:shanmukvenkatad@gmail.com)