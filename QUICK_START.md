# 🚀 Quick Start Guide

## New to the tool? Start here! 🎯

### 🎯 Option 1: Just Run It! (Easiest)
Simply run the tool with no arguments and you'll get a friendly menu:

```bash
python main.py
```

You'll see an interactive menu with these options:
- 🎯 **Interactive Mode** - Step-by-step guidance (perfect for beginners)
- 🧙‍♂️ **Configuration Wizard** - First-time setup
- 📚 **Quick Examples** - See example commands
- 🔍 **Safe Testing Modes** - Learn about safe options
- ⚡ **Advanced Mode** - Full command-line options
- ❓ **Help & Documentation** - Learning resources

### Option 2: Interactive Mode (Recommended for Beginners)

```bash
python main.py --interactive
```

The interactive mode will:
- ✅ Guide you step-by-step
- ✅ Help you choose the right options
- ✅ Validate your inputs
- ✅ Show you what will happen before running

### Option 3: Configuration Wizard

First-time setup? Run the configuration wizard:

```bash
python main.py --wizard
```

This creates a personalized configuration file for you.

### Option 4: Quick Examples

#### Safe Reconnaissance (No Attack)
```bash
python main.py https://example.com --recon-only -w wordlists/common_passwords.txt
```

#### Find Login Forms Only
```bash
python main.py https://example.com --forms-only -w wordlists/common_passwords.txt
```

#### Basic Attack (Only on systems you own!)
```bash
python main.py http://localhost:8080/login -w wordlists/common_passwords.txt -u admin
```

## 🎯 What Each Mode Does

| Mode | Purpose | Safe for Testing? |
|------|---------|-------------------|
| `--recon-only` | Just gather information about target | ✅ Yes |
| `--forms-only` | Just find login forms | ✅ Yes |
| Default | Full brute force attack | ⚠️ Only on systems you own |

## 📚 Need Help?

- **Interactive Mode**: `python main.py --interactive`
- **Full Help**: `python main.py --help`
- **Documentation**: [docs/USAGE.md](docs/USAGE.md)
- **Examples**: [examples/basic_usage.py](examples/basic_usage.py)

## ⚠️ Important Rules

1. **NEVER** test on websites you don't own
2. **ALWAYS** get permission before testing
3. **USE** local test environments for practice
4. **FOLLOW** all laws and regulations

## 🛠️ Setup Your Own Test Lab

Want to practice safely? Set up a local test environment:

```bash
# Install a vulnerable web app for testing
# Examples: DVWA, WebGoat, OWASP Juice Shop

# Then test your local setup
python main.py http://localhost:8080/login -w wordlists/common_passwords.txt -u admin
```

## 📚 System Requirements

- **Python 3.8+** (3.7 is no longer supported by GitHub Actions)
- Dependencies listed in `requirements.txt`

---

**Remember**: Start with interactive mode for the best experience! 🎉
