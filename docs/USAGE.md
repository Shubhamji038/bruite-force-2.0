# Bruite Force Tool - Usage Guide

## Overview

The Bruite Force tool is a comprehensive Python package for educational web security testing. This guide covers how to use the tool effectively and responsibly.

⚠️ **EDUCATIONAL USE ONLY** ⚠️
This tool is designed for educational purposes and authorized security testing only.

## Installation

### From Source

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### As a Package

```bash
pip install -e .
```

This will install the tool with console scripts:
- `bruite-force`
- `bruite_force`

## Basic Usage

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

#### Basic Usage
```python
from bruite_force import BruteForceTool

tool = BruteForceTool(
    target_url="https://example.com/login",
    wordlist_path="wordlists/common_passwords.txt",
    usernames=["admin", "root"]
)

success = tool.run()
```

#### Advanced Usage
```python
from bruite_force import BruteForceTool, ConfigManager, setup_logger

# Setup custom logging
setup_logger("my_attack", log_level="DEBUG", log_file="attack.log")

# Load custom configuration
config = ConfigManager("custom_config.json")

# Initialize tool
tool = BruteForceTool(
    target_url="https://example.com/admin",
    wordlist_path="wordlists/common_passwords.txt",
    usernames=["admin"],
    config_path="custom_config.json",
    log_level="DEBUG"
)

# Run reconnaissance only
target_info = tool.get_target_info()
forms = tool.get_login_forms()

# Run full attack
success = tool.run()
```

## Command Line Options

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

## Configuration

### Default Configuration File (config.json)

The tool uses `config.json` for default settings:

```json
{
  "default_settings": {
    "max_workers": 5,
    "delay_between_attempts": 1.0,
    "timeout": 10,
    "max_retries": 3,
    "user_agents": [
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
    ]
  },
  "login_detection": {
    "username_patterns": ["username", "user", "email", "login"],
    "password_patterns": ["password", "pass", "pwd", "userpass"],
    "common_login_paths": ["/login", "/signin", "/auth", "/admin"]
  },
  "response_analysis": {
    "success_indicators": ["dashboard", "welcome", "logout", "profile"],
    "failure_indicators": ["invalid", "incorrect", "failed", "error"],
    "success_status_codes": [200, 302, 303],
    "failure_status_codes": [401, 403, 404]
  },
  "password_generation": {
    "common_suffixes": ["123", "1234", "2023", "2024", "admin"],
    "common_prefixes": ["admin", "user", "test"]
  },
  "rate_limiting": {
    "default_delay": 1.0,
    "adaptive_delay": true,
    "max_delay": 10.0
  }
}
```

### Custom Configuration

Create a custom configuration file and use it with `--config` option:

```python
from bruite_force import ConfigManager

config = ConfigManager("my_config.json")
config.update_config("default_settings.max_workers", 10)
config.update_config("default_settings.delay_between_attempts", 0.5)
config.save_config()
```

## Wordlists

### Included Wordlists

- `wordlists/common_passwords.txt`: Common passwords for testing
- `wordlists/usernames.txt`: Common usernames to try

### External Wordlists

For comprehensive testing, consider using:

- [SecLists](https://github.com/danielmiessler/SecLists) - Large collection of wordlists
- [RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) - Real-world password dump

### Custom Wordlists

Create custom wordlists based on target information:

```bash
# Create a custom wordlist
echo -e "admin\npassword\n123456\nwelcome" > custom_passwords.txt

# Use with the tool
python main.py https://example.com/login -w custom_passwords.txt -u admin
```

## Attack Phases

The tool operates in four phases:

### Phase 1: Target Reconnaissance
- Connects to the target website
- Gathers basic information (server, headers, etc.)
- Tests connectivity

### Phase 2: Login Form Analysis
- Discovers potential login pages using common paths
- Parses HTML to find traditional login forms
- Detects JavaScript-based login systems
- Identifies username, password fields, and CSRF tokens

### Phase 3: Password Preparation
- Loads passwords from wordlist
- Generates password variations based on usernames
- Applies common patterns and transformations

### Phase 4: Brute Force Attack
- Tests credential combinations systematically
- Analyzes responses to determine success/failure
- Handles JSON APIs and traditional HTML responses
- Implements rate limiting to avoid detection

## Output Examples

### Successful Attack
```
=== Phase 1: Target Reconnaissance ===
Target: example.com
Server: nginx/1.18.0
Status Code: 200

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

### Reconnaissance Only
```
=== Phase 1: Target Reconnaissance ===
Target: example.com
Server: nginx/1.18.0
Status Code: 200

Target Information:
URL: https://example.com
Domain: example.com
Server: nginx/1.18.0
Status: Reachable
```

## Best Practices

### 1. Rate Limiting
- Use appropriate delays between attempts
- Consider adaptive delay for stealth
- Monitor for IP blocking

### 2. Wordlist Selection
- Start with small, targeted wordlists
- Use custom wordlists based on target information
- Consider password variations and common patterns

### 3. Target Selection
- Only test systems you own or have permission to test
- Start with reconnaissance to understand the target
- Be aware of legal and ethical implications

### 4. Logging and Monitoring
- Enable detailed logging for analysis
- Monitor attack progress and results
- Keep logs for educational purposes

## Troubleshooting

### Common Issues

1. **No login forms found**
   - Check if the target is reachable
   - Verify the URL is correct
   - Try reconnaissance mode first

2. **Wordlist not found**
   - Verify the wordlist file path
   - Check file permissions
   - Ensure wordlist is not empty

3. **Connection timeouts**
   - Increase timeout in configuration
   - Check network connectivity
   - Verify target is accessible

4. **Rate limiting detected**
   - Increase delay between attempts
   - Reduce number of threads
   - Use adaptive delay

### Debug Mode

Enable debug logging for detailed information:

```bash
python main.py https://example.com/login -w wordlist.txt -u admin --log-level DEBUG
```

## Legal and Ethical Considerations

1. **Authorization**: Only test systems you own or have explicit permission to test
2. **Legal Compliance**: Ensure compliance with local laws and regulations
3. **Responsible Use**: Use the tool ethically and responsibly
4. **Education**: Focus on learning and improving security knowledge

## Support and Contributing

For issues, questions, or contributions:
- Check the documentation
- Review the examples
- Follow ethical guidelines
- Contribute responsibly

---

**Remember**: With great power comes great responsibility. Use this tool ethically and legally.
