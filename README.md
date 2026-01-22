# Bruite Force 2.0 - Educational Web Security Testing Tool

⚠️ **EDUCATIONAL USE ONLY** ⚠️

This tool is designed for educational purposes and authorized security testing only. Unauthorized access to computer systems is illegal and unethical. Only use this tool on systems you own or have explicit permission to test.

## 🚀 What's New in Version 2.0

- **Complete Package Restructure**: Now organized as a proper Python package
- **Modular Architecture**: Clean separation of concerns with core and utility modules
- **Enhanced Configuration**: Flexible configuration management system
- **Improved Logging**: Colored console output and configurable logging
- **Better CLI**: User-friendly command-line interface with multiple modes
- **Comprehensive Documentation**: Detailed usage guides and examples
- **Proper Installation**: Installable as a Python package with pip

## 📁 New Project Structure

```
bruite-force-2.0/
├── bruite_force/                 # Main package
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Command-line interface
│   ├── core/                    # Core functionality
│   │   ├── __init__.py
│   │   ├── target_info.py       # Data classes for targets and forms
│   │   ├── reconnaissance.py    # Target reconnaissance module
│   │   ├── form_parser.py       # Login form analysis
│   │   ├── attack_engine.py     # Brute force attack engine
│   │   └── brute_force_tool.py # Main tool coordinator
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── config_manager.py    # Configuration management
│       └── logger.py           # Logging utilities
├── examples/                    # Usage examples
│   └── basic_usage.py
├── docs/                        # Documentation
│   └── USAGE.md
├── wordlists/                   # Password and username wordlists
│   ├── common_passwords.txt
│   └── usernames.txt
├── main.py                      # Main entry point
├── config.json                  # Configuration file
├── requirements.txt             # Dependencies
├── setup.py                     # Package installation script
└── README.md                    # This file
```

## 🛠️ Installation

### Option 1: Run from Source
```bash
git clone <repository-url>
cd bruite-force-2.0
pip install -r requirements.txt
python main.py --help
```

### Option 2: Install as Package
```bash
git clone <repository-url>
cd bruite-force-2.0
pip install -e .
bruite-force --help
```

## 🎯 Usage

### Command Line Interface

#### Basic Attack
```bash
python main.py https://example.com/login -w wordlists/common_passwords.txt -u admin
```

#### Advanced Attack
```bash
python main.py https://example.com/admin \
    -w wordlists/common_passwords.txt \
    -u admin administrator root \
    -t 10 \
    -d 0.5 \
    --log-level DEBUG
```

#### Reconnaissance Only
```bash
python main.py https://example.com --recon-only -w wordlists/common_passwords.txt
```

#### Find Login Forms Only
```bash
python main.py https://example.com --forms-only -w wordlists/common_passwords.txt
```

### Python API

```python
from bruite_force import BruteForceTool

# Initialize the tool
tool = BruteForceTool(
    target_url="https://example.com/login",
    wordlist_path="wordlists/common_passwords.txt",
    usernames=["admin", "root"]
)

# Run the attack
success = tool.run()
```

## 📋 Command Line Options

### Required Arguments
- `target`: Target URL (e.g., http://example.com/login)
- `-w, --wordlist`: Path to password wordlist file

### Optional Arguments
- `-u, --usernames`: Usernames to test (default: admin)
- `-t, --threads`: Number of concurrent threads (default: 5)
- `-d, --delay`: Delay between attempts in seconds (default: 1.0)
- `--config`: Path to configuration file (default: config.json)
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--log-file`: Path to log file (default: brute_force.log)
- `--no-color`: Disable colored output
- `--recon-only`: Only perform reconnaissance, don't run attack
- `--forms-only`: Only find login forms, don't run attack

## 🔧 Configuration

The tool uses `config.json` for default settings. You can customize:

- Attack parameters (threads, delays, timeouts)
- Detection patterns (username/password field patterns)
- Response analysis (success/failure indicators)
- Password generation rules
- Rate limiting settings

## 📚 Documentation

- **[Detailed Usage Guide](docs/USAGE.md)**: Comprehensive documentation with examples
- **[Examples](examples/basic_usage.py)**: Code examples for different use cases

## 🎯 Key Features

### Smart Form Detection
- Automatically detects traditional HTML forms
- Identifies modern JavaScript-based login systems
- Handles JSON APIs and CSRF tokens

### Multi-Strategy Attacks
- Supports various brute force techniques
- Generates password variations based on usernames
- Applies common patterns and transformations

### Adaptive Rate Limiting
- Built-in delays to avoid detection
- Configurable attack parameters
- Support for multiple attack modes

### Comprehensive Logging
- Detailed attack progress and results
- Colored console output for better visibility
- Configurable logging levels and file output

### Modern Web App Support
- Handles JSON APIs and REST endpoints
- Supports JavaScript-rendered forms
- Compatible with various web frameworks

## 🛠️ System Requirements

- **Python 3.8+** (3.7 is no longer supported by GitHub Actions)
- Dependencies listed in `requirements.txt`:
  - `requests==2.31.0`
  - `beautifulsoup4==4.12.2`
  - `lxml==4.9.3`
  - `colorama==0.4.6`

## 🛡️ Supported Login Systems

### Traditional HTML Forms
- Standard POST/GET forms
- CSRF token protection
- Multiple input fields
- Hidden fields and parameters

### Modern Web Applications
- JSON API endpoints
- JavaScript-rendered forms
- Token-based authentication
- REST API authentication

### Framework-Specific Support
- WordPress
- Joomla
- Drupal
- Custom PHP applications
- Next.js applications
- React applications

## 📊 Example Output

```
=== Phase 1: Target Reconnaissance ===
Target: example.com
Server: nginx/1.18.0
Status Code: 200
Discovered login page: https://example.com/login

=== Phase 2: Login Form Analysis ===
Found traditional login form: https://example.com/login

=== Phase 3: Password Preparation ===
Loaded 200 passwords from wordlists/common_passwords.txt
Total passwords to test: 1200

=== Phase 4: Brute Force Attack ===
[1/1200] Failed: admin:123456
[2/1200] Failed: admin:password
...
[45/1200] SUCCESS: admin:admin123

🎉 SUCCESS! Credentials found:
Username: admin
Password: admin123
Target: https://example.com/login
```

## ⚠️ Legal Disclaimer

This tool is provided for educational and authorized security testing purposes only. Users are responsible for ensuring they have proper authorization before testing any system. The authors are not responsible for any misuse or illegal activities.

## 🔒 Security Considerations

- Always obtain proper authorization before testing
- Use rate limiting to avoid impacting target systems
- Be aware of legal implications in your jurisdiction
- Consider the ethical implications of security testing
- Never use on systems you don't own or have permission to test

## 🤝 Contributing

Contributions are welcome for educational improvements. Please ensure all contributions maintain the educational focus and include appropriate warnings.

## 📄 License

This project is provided for educational purposes. Please use responsibly and in accordance with applicable laws and regulations.

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.

## 🆘 Migration from v1.0

If you're upgrading from the original version:

1. **New Entry Point**: Use `python main.py` instead of `python brute_force.py`
2. **Package Structure**: The code is now organized in a proper Python package
3. **Enhanced CLI**: More command-line options and better help output
4. **Better Configuration**: Improved configuration management system
5. **Improved Logging**: Colored output and better log management

The core functionality remains the same, but the tool is now more user-friendly and maintainable.
