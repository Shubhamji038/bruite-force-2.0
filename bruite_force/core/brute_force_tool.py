"""
Main tool class that coordinates all modules
"""

import logging
from typing import List, Optional

from .target_info import TargetInfo
from .reconnaissance import WebReconnaissance
from .form_parser import LoginFormParser
from .attack_engine import BruteForceEngine
from ..utils.config_manager import ConfigManager
from ..utils.logger import setup_colored_logger

logger = logging.getLogger(__name__)


class BruteForceTool:
    """Main tool class that coordinates all modules"""
    
    def __init__(self, 
                 target_url: str, 
                 wordlist_path: str, 
                 usernames: List[str],
                 config_path: str = None,
                 log_level: str = "INFO",
                 log_file: str = None):
        """
        Initialize the brute force tool
        
        Args:
            target_url: Target URL to test
            wordlist_path: Path to password wordlist
            usernames: List of usernames to test
            config_path: Path to configuration file
            log_level: Logging level
            log_file: Path to log file
        """
        self.target_url = target_url
        self.wordlist_path = wordlist_path
        self.usernames = usernames
        
        # Setup logging
        setup_colored_logger("bruite_force", log_level, log_file)
        
        # Initialize configuration
        self.config = ConfigManager(config_path)
        
        # Initialize modules
        self.reconnaissance = WebReconnaissance(target_url, self.config)
        self.form_parser = LoginFormParser(self.reconnaissance.session, self.config)
        
        logger.info(f"Initialized BruteForceTool for target: {target_url}")
    
    def run(self) -> bool:
        """Run the complete brute force attack"""
        try:
            # Step 1: Gather information about target
            logger.info("=== Phase 1: Target Reconnaissance ===")
            target_info = self.reconnaissance.get_basic_info()
            
            # Test connectivity
            if not self.reconnaissance.test_connectivity():
                logger.error("Target is not reachable!")
                return False
            
            # Step 2: Discover login pages
            login_pages = self.reconnaissance.discover_login_pages(self.target_url)
            
            # Step 3: Extract login forms
            logger.info("\n=== Phase 2: Login Form Analysis ===")
            all_forms = []
            for page in login_pages:
                forms = self.form_parser.extract_login_forms(page)
                all_forms.extend(forms)
            
            if not all_forms:
                logger.error("No login forms found!")
                return False
            
            target_info.login_forms = all_forms
            logger.info(f"Found {len(all_forms)} login form(s)")
            
            # Step 4: Load and prepare passwords
            logger.info("\n=== Phase 3: Password Preparation ===")
            engine = BruteForceEngine(target_info, self.config)
            base_passwords = engine.load_wordlist(self.wordlist_path)
            
            if not base_passwords:
                logger.error("No passwords loaded!")
                return False
            
            # Generate password variations
            passwords = engine.generate_password_variations(base_passwords, self.usernames)
            logger.info(f"Total passwords to test: {len(passwords)}")
            
            # Step 5: Run brute force attack
            logger.info("\n=== Phase 4: Brute Force Attack ===")
            result = engine.run_attack(self.usernames, passwords)
            
            if result:
                username, password = result
                logger.info(f"\n🎉 SUCCESS! Credentials found:")
                logger.info(f"Username: {username}")
                logger.info(f"Password: {password}")
                logger.info(f"Target: {self.target_url}")
                return True
            else:
                logger.info("\n❌ No valid credentials found.")
                return False
                
        except Exception as e:
            logger.error(f"Error during brute force attack: {e}")
            return False
    
    def get_target_info(self) -> Optional[TargetInfo]:
        """Get target information without running full attack"""
        try:
            return self.reconnaissance.get_basic_info()
        except Exception as e:
            logger.error(f"Error getting target info: {e}")
            return None
    
    def get_login_forms(self) -> List:
        """Get login forms without running full attack"""
        try:
            login_pages = self.reconnaissance.discover_login_pages(self.target_url)
            all_forms = []
            for page in login_pages:
                forms = self.form_parser.extract_login_forms(page)
                all_forms.extend(forms)
            return all_forms
        except Exception as e:
            logger.error(f"Error getting login forms: {e}")
            return []
