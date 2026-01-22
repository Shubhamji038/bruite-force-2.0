# Contributing to Bruite Force

Thank you for your interest in contributing to Bruite Force! This educational tool is designed for authorized security testing and learning purposes.

## 🎯 Educational Mission

Bruite Force is an **educational tool** designed to help students and professionals learn about web security testing. All contributions should maintain this educational focus and include appropriate warnings about authorized use only.

## 🤝 How to Contribute

### Reporting Issues

1. **Bug Reports**: Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template
2. **Feature Requests**: Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template
3. **Security Issues**: For security vulnerabilities, please report privately

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/bruite-force.git
   cd bruite-force
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
5. Run tests:
   ```bash
   python -m pytest
   ```

### Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add tests if applicable
4. Update documentation
5. Ensure all tests pass
6. Submit a pull request

## 📝 Code Guidelines

### Python Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Educational Focus
- All code should be well-documented
- Include comments explaining security concepts
- Maintain clear warnings about authorized use only
- Focus on learning value

### Safety Considerations
- Never remove or weaken safety warnings
- Ensure all user inputs are validated
- Include rate limiting to prevent abuse
- Add appropriate error handling

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=bruite_force

# Run specific test file
python -m pytest tests/test_core.py
```

### Test Structure
- Unit tests for individual functions
- Integration tests for complete workflows
- Mock external dependencies (requests, etc.)
- Test error conditions and edge cases

## 📚 Documentation

### Updating Documentation
- Update README.md for user-facing changes
- Update docs/USAGE.md for technical changes
- Add inline code comments for complex logic
- Update CHANGELOG.md for version changes

### Educational Content
- Explain security concepts clearly
- Provide examples for educational use
- Include safety warnings
- Reference relevant security standards

## 🔒 Security Considerations

### Responsible Disclosure
- This tool is for educational purposes only
- All contributions must maintain this focus
- Include appropriate warnings and disclaimers
- Never facilitate unauthorized access

### Code Review
- All PRs require review
- Focus on security implications
- Check for potential misuse
- Ensure educational value

## 📦 Release Process

1. Update version number in `bruite_force/__init__.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Tag the release with version number

## 🎓 Educational Resources

Contributors should be familiar with:
- OWASP Top 10
- Web security fundamentals
- Authentication mechanisms
- Rate limiting and abuse prevention
- Legal and ethical considerations

## 📞 Getting Help

- Create an issue for questions
- Check existing documentation first
- Join discussions in issues
- Review existing PRs for examples

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for helping improve this educational security tool! 🎉

---

**⚠️ Important Reminder**: This tool is for educational purposes only. All contributors must ensure their changes maintain this focus and include appropriate warnings about authorized use.
