"""
Configuration management module
"""

import json
import os
from typing import List, Dict, Any


class ConfigManager:
    """Manages configuration settings for the brute force tool"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), '..', '..', 'config.json')
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default configuration if file doesn't exist
                return self._get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "default_settings": {
                "max_workers": 5,
                "delay_between_attempts": 1.0,
                "timeout": 10,
                "max_retries": 3,
                "user_agents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                ]
            },
            "login_detection": {
                "username_patterns": ["username", "user", "email", "login", "userid", "user_name"],
                "password_patterns": ["password", "pass", "pwd", "userpass"],
                "common_login_paths": ["/login", "/signin", "/auth", "/admin", "/wp-admin"]
            },
            "response_analysis": {
                "success_indicators": ["dashboard", "welcome", "logout", "profile", "success"],
                "failure_indicators": ["invalid", "incorrect", "failed", "error", "wrong"],
                "success_status_codes": [200, 302, 303],
                "failure_status_codes": [401, 403, 404]
            },
            "password_generation": {
                "common_suffixes": ["123", "1234", "2023", "2024", "admin"],
                "common_prefixes": ["admin", "user", "test"]
            },
            "rate_limiting": {
                "default_delay": 1.0,
                "adaptive_delay": True,
                "max_delay": 10.0
            }
        }
    
    def get_max_workers(self) -> int:
        """Get maximum number of worker threads"""
        return self.config_data.get("default_settings", {}).get("max_workers", 5)
    
    def get_timeout(self) -> int:
        """Get request timeout in seconds"""
        return self.config_data.get("default_settings", {}).get("timeout", 10)
    
    def get_user_agents(self) -> List[str]:
        """Get list of user agents"""
        return self.config_data.get("default_settings", {}).get("user_agents", [])
    
    def get_default_user_agent(self) -> str:
        """Get default user agent"""
        return self.get_user_agents()[0] if self.get_user_agents() else "Mozilla/5.0"
    
    def get_username_patterns(self) -> List[str]:
        """Get username field patterns"""
        return self.config_data.get("login_detection", {}).get("username_patterns", [])
    
    def get_password_patterns(self) -> List[str]:
        """Get password field patterns"""
        return self.config_data.get("login_detection", {}).get("password_patterns", [])
    
    def get_common_login_paths(self) -> List[str]:
        """Get common login paths"""
        return self.config_data.get("login_detection", {}).get("common_login_paths", [])
    
    def get_success_indicators(self) -> List[str]:
        """Get success response indicators"""
        return self.config_data.get("response_analysis", {}).get("success_indicators", [])
    
    def get_failure_indicators(self) -> List[str]:
        """Get failure response indicators"""
        return self.config_data.get("response_analysis", {}).get("failure_indicators", [])
    
    def get_success_status_codes(self) -> List[int]:
        """Get success HTTP status codes"""
        return self.config_data.get("response_analysis", {}).get("success_status_codes", [200, 302, 303])
    
    def get_failure_status_codes(self) -> List[int]:
        """Get failure HTTP status codes"""
        return self.config_data.get("response_analysis", {}).get("failure_status_codes", [401, 403, 404])
    
    def get_common_suffixes(self) -> List[str]:
        """Get common password suffixes"""
        return self.config_data.get("password_generation", {}).get("common_suffixes", [])
    
    def get_common_prefixes(self) -> List[str]:
        """Get common password prefixes"""
        return self.config_data.get("password_generation", {}).get("common_prefixes", [])
    
    def get_default_delay(self) -> float:
        """Get default delay between attempts"""
        return self.config_data.get("rate_limiting", {}).get("default_delay", 1.0)
    
    def is_adaptive_delay_enabled(self) -> bool:
        """Check if adaptive delay is enabled"""
        return self.config_data.get("rate_limiting", {}).get("adaptive_delay", False)
    
    def get_max_delay(self) -> float:
        """Get maximum delay for adaptive delay"""
        return self.config_data.get("rate_limiting", {}).get("max_delay", 10.0)
    
    def update_config(self, key: str, value: Any):
        """Update a configuration value"""
        keys = key.split('.')
        current = self.config_data
        
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        current[keys[-1]] = value
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
