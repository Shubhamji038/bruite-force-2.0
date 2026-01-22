#!/usr/bin/env python3
"""
Configuration wizard for first-time users
Helps set up initial configuration and preferences
"""

import json
import os
from typing import Dict, Any


class ConfigWizard:
    """Configuration wizard for first-time setup"""
    
    def __init__(self):
        self.config_path = "config.json"
        
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🧙‍♂️ Bruite Force Configuration Wizard")
        print("="*60)
        print("\nThis wizard will help you configure the tool for first-time use.")
        print("You can always change these settings later by editing config.json")
        print("\nLet's get started!")
    
    def get_basic_settings(self) -> Dict[str, Any]:
        """Get basic configuration settings"""
        print("\n📋 Basic Settings")
        print("-" * 20)
        
        settings = {}
        
        # Max workers
        while True:
            try:
                workers = input("Default number of threads [5]: ").strip()
                settings['max_workers'] = int(workers) if workers else 5
                if settings['max_workers'] < 1:
                    print("❌ Must be at least 1")
                    continue
                break
            except ValueError:
                print("❌ Please enter a number")
        
        # Delay
        while True:
            try:
                delay = input("Default delay between attempts (seconds) [1.0]: ").strip()
                settings['delay_between_attempts'] = float(delay) if delay else 1.0
                if settings['delay_between_attempts'] < 0:
                    print("❌ Must be positive")
                    continue
                break
            except ValueError:
                print("❌ Please enter a number")
        
        # Timeout
        while True:
            try:
                timeout = input("Request timeout (seconds) [10]: ").strip()
                settings['timeout'] = int(timeout) if timeout else 10
                if settings['timeout'] < 1:
                    print("❌ Must be at least 1")
                    continue
                break
            except ValueError:
                print("❌ Please enter a number")
        
        return settings
    
    def get_detection_patterns(self) -> Dict[str, Any]:
        """Get login detection patterns"""
        print("\n🔍 Login Detection Patterns")
        print("-" * 30)
        print("These help the tool find login forms automatically")
        print("Press Enter to use defaults")
        
        patterns = {}
        
        # Username patterns
        username_input = input("Username patterns [username,user,email,login]: ").strip()
        if username_input:
            patterns['username_patterns'] = [p.strip() for p in username_input.split(',')]
        else:
            patterns['username_patterns'] = ['username', 'user', 'email', 'login']
        
        # Password patterns
        password_input = input("Password patterns [password,pass,pwd]: ").strip()
        if password_input:
            patterns['password_patterns'] = [p.strip() for p in password_input.split(',')]
        else:
            patterns['password_patterns'] = ['password', 'pass', 'pwd']
        
        # Login paths
        paths_input = input("Common login paths [/login,/admin,/auth]: ").strip()
        if paths_input:
            patterns['common_login_paths'] = [p.strip() for p in paths_input.split(',')]
        else:
            patterns['common_login_paths'] = ['/login', '/admin', '/auth']
        
        return patterns
    
    def get_response_analysis(self) -> Dict[str, Any]:
        """Get response analysis settings"""
        print("\n📊 Response Analysis")
        print("-" * 20)
        print("These help determine if login attempts succeed or fail")
        
        analysis = {}
        
        # Success indicators
        success_input = input("Success indicators [dashboard,welcome,logout]: ").strip()
        if success_input:
            analysis['success_indicators'] = [s.strip() for s in success_input.split(',')]
        else:
            analysis['success_indicators'] = ['dashboard', 'welcome', 'logout']
        
        # Failure indicators
        failure_input = input("Failure indicators [invalid,failed,error]: ").strip()
        if failure_input:
            analysis['failure_indicators'] = [f.strip() for f in failure_input.split(',')]
        else:
            analysis['failure_indicators'] = ['invalid', 'failed', 'error']
        
        # Status codes
        analysis['success_status_codes'] = [200, 302, 303]
        analysis['failure_status_codes'] = [401, 403, 404]
        
        return analysis
    
    def get_password_generation(self) -> Dict[str, Any]:
        """Get password generation settings"""
        print("\n🔐 Password Generation")
        print("-" * 22)
        print("These settings help generate password variations")
        
        generation = {}
        
        # Suffixes
        suffix_input = input("Common suffixes [123,admin,2024]: ").strip()
        if suffix_input:
            generation['common_suffixes'] = [s.strip() for s in suffix_input.split(',')]
        else:
            generation['common_suffixes'] = ['123', 'admin', '2024']
        
        # Prefixes
        prefix_input = input("Common prefixes [admin,user,test]: ").strip()
        if prefix_input:
            generation['common_prefixes'] = [p.strip() for p in prefix_input.split(',')]
        else:
            generation['common_prefixes'] = ['admin', 'user', 'test']
        
        return generation
    
    def get_rate_limiting(self) -> Dict[str, Any]:
        """Get rate limiting settings"""
        print("\n⏱️  Rate Limiting")
        print("-" * 16)
        print("These settings help avoid detection and IP blocking")
        
        limiting = {}
        
        # Adaptive delay
        adaptive_input = input("Enable adaptive delay? [Y/n]: ").strip().lower()
        limiting['adaptive_delay'] = adaptive_input != 'n'
        
        # Max delay
        if limiting['adaptive_delay']:
            while True:
                try:
                    max_delay = input("Maximum delay (seconds) [10.0]: ").strip()
                    limiting['max_delay'] = float(max_delay) if max_delay else 10.0
                    if limiting['max_delay'] < 0:
                        print("❌ Must be positive")
                        continue
                    break
                except ValueError:
                    print("❌ Please enter a number")
        else:
            limiting['max_delay'] = 10.0
        
        limiting['default_delay'] = 1.0
        
        return limiting
    
    def create_config(self) -> Dict[str, Any]:
        """Create complete configuration"""
        config = {
            "default_settings": self.get_basic_settings(),
            "login_detection": self.get_detection_patterns(),
            "response_analysis": self.get_response_analysis(),
            "password_generation": self.get_password_generation(),
            "rate_limiting": self.get_rate_limiting()
        }
        
        # Add user agents
        config["default_settings"]["user_agents"] = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        config["default_settings"]["max_retries"] = 3
        
        return config
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"\n✅ Configuration saved to {self.config_path}")
        except Exception as e:
            print(f"\n❌ Error saving configuration: {e}")
    
    def run(self):
        """Run the configuration wizard"""
        try:
            self.display_welcome()
            
            # Check if config already exists
            if os.path.exists(self.config_path):
                overwrite = input(f"\n⚠️  {self.config_path} already exists. Overwrite? [y/N]: ").strip().lower()
                if overwrite != 'y':
                    print("Configuration wizard cancelled.")
                    return
            
            # Create configuration
            config = self.create_config()
            
            # Save configuration
            self.save_config(config)
            
            print("\n🎉 Configuration complete!")
            print("You can now use the tool with:")
            print("  python main.py --help")
            print("  python main.py --interactive")
            
        except KeyboardInterrupt:
            print("\n\n❌ Configuration wizard cancelled")
        except Exception as e:
            print(f"\n❌ Error: {e}")


def main():
    """Main function for configuration wizard"""
    wizard = ConfigWizard()
    wizard.run()


if __name__ == "__main__":
    main()
