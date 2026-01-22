#!/usr/bin/env python3
"""
Basic usage examples for the Bruite Force tool
"""

import sys
import os

# Add the package to Python path for examples
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bruite_force import BruteForceTool, ConfigManager, setup_logger

def example_basic_usage():
    """Example of basic tool usage"""
    print("=== Basic Usage Example ===")
    
    # Initialize the tool
    tool = BruteForceTool(
        target_url="https://example.com/login",
        wordlist_path="wordlists/common_passwords.txt",
        usernames=["admin", "root"],
        log_level="INFO"
    )
    
    # Run the attack
    success = tool.run()
    
    if success:
        print("Attack completed successfully!")
    else:
        print("Attack failed or no credentials found.")

def example_reconnaissance_only():
    """Example of reconnaissance only"""
    print("\n=== Reconnaissance Only Example ===")
    
    tool = BruteForceTool(
        target_url="https://example.com",
        wordlist_path="wordlists/common_passwords.txt",
        usernames=["admin"]
    )
    
    # Get target information
    target_info = tool.get_target_info()
    if target_info:
        print(f"Target: {target_info.url}")
        print(f"Domain: {target_info.domain}")
        print(f"Server: {target_info.headers.get('Server', 'Unknown')}")
    
    # Get login forms
    forms = tool.get_login_forms()
    print(f"Found {len(forms)} login form(s)")
    for i, form in enumerate(forms, 1):
        print(f"{i}. {form.action_url} ({form.method})")

def example_custom_config():
    """Example with custom configuration"""
    print("\n=== Custom Configuration Example ===")
    
    # Load custom config
    config = ConfigManager("custom_config.json")
    
    # Update some settings
    config.update_config("default_settings.max_workers", 10)
    config.update_config("default_settings.delay_between_attempts", 0.5)
    
    # Initialize tool with custom config
    tool = BruteForceTool(
        target_url="https://example.com/admin",
        wordlist_path="wordlists/common_passwords.txt",
        usernames=["admin"],
        config_path="custom_config.json"
    )
    
    print("Tool initialized with custom configuration")

def example_logging():
    """Example of custom logging setup"""
    print("\n=== Custom Logging Example ===")
    
    # Setup custom logger
    logger = setup_logger(
        name="custom_brute_force",
        log_level="DEBUG",
        log_file="custom_attack.log",
        console_output=True
    )
    
    logger.info("Custom logging setup complete")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")

if __name__ == "__main__":
    print("Bruite Force Tool - Usage Examples")
    print("=" * 50)
    
    # Note: These examples are for demonstration purposes only
    # They won't actually run without valid targets and wordlists
    
    try:
        example_basic_usage()
    except Exception as e:
        print(f"Basic usage example failed: {e}")
    
    try:
        example_reconnaissance_only()
    except Exception as e:
        print(f"Reconnaissance example failed: {e}")
    
    try:
        example_custom_config()
    except Exception as e:
        print(f"Custom config example failed: {e}")
    
    try:
        example_logging()
    except Exception as e:
        print(f"Logging example failed: {e}")
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("Note: These are demonstration examples only.")
    print("Use with actual targets and proper authorization.")
