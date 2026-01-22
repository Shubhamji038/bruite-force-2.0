#!/usr/bin/env python3
"""
Test utility modules of Bruite Force tool
"""

import unittest
import os
import sys
import tempfile
import json

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bruite_force.utils.config_manager import ConfigManager
from bruite_force.utils.logger import setup_logger


class TestConfigManager(unittest.TestCase):
    """Test ConfigManager class"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.json")
    
    def tearDown(self):
        # Clean up temporary files
        try:
            if os.path.exists(self.config_path):
                os.remove(self.config_path)
            if os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            # Ignore cleanup errors on Windows
            pass
    
    def test_default_config_creation(self):
        """Test default configuration creation"""
        config = ConfigManager(self.config_path)
        
        # Should have default values
        self.assertEqual(config.get_max_workers(), 5)
        self.assertEqual(config.get_default_delay(), 1.0)
        self.assertEqual(config.get_timeout(), 10)
    
    def test_config_loading(self):
        """Test configuration loading from file"""
        # Create a test config file with unique name
        test_config = {
            "default_settings": {
                "max_workers": 10,
                "delay_between_attempts": 2.0,
                "timeout": 15
            },
            "rate_limiting": {
                "default_delay": 2.0
            }
        }
        
        # Use a different config path for testing
        test_config_path = os.path.join(self.temp_dir, "test_config.json")
        
        with open(test_config_path, 'w') as f:
            json.dump(test_config, f)
        
        # Now create ConfigManager with the test config path
        config = ConfigManager(test_config_path)
        
        self.assertEqual(config.get_max_workers(), 10)
        self.assertEqual(config.get_default_delay(), 2.0)
        self.assertEqual(config.get_timeout(), 15)
    
    def test_config_update(self):
        """Test configuration updates"""
        config = ConfigManager(self.config_path)
        
        config.update_config("default_settings.max_workers", 20)
        self.assertEqual(config.get_max_workers(), 20)
    
    def test_get_patterns(self):
        """Test getting detection patterns"""
        config = ConfigManager(self.config_path)
        
        username_patterns = config.get_username_patterns()
        password_patterns = config.get_password_patterns()
        
        self.assertIsInstance(username_patterns, list)
        self.assertIsInstance(password_patterns, list)
        self.assertIn("username", username_patterns)
        self.assertIn("password", password_patterns)
    
    def test_get_indicators(self):
        """Test getting response indicators"""
        config = ConfigManager(self.config_path)
        
        success_indicators = config.get_success_indicators()
        failure_indicators = config.get_failure_indicators()
        
        self.assertIsInstance(success_indicators, list)
        self.assertIsInstance(failure_indicators, list)
        self.assertIn("success", success_indicators)
        self.assertIn("error", failure_indicators)


class TestLogger(unittest.TestCase):
    """Test logger utilities"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
    
    def tearDown(self):
        # Clean up temporary files
        try:
            if os.path.exists(self.log_file):
                os.remove(self.log_file)
            if os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir)
        except (PermissionError, OSError):
            # Ignore cleanup errors on Windows
            pass
    
    def test_setup_logger(self):
        """Test logger setup"""
        logger = setup_logger("test_logger", "INFO", self.log_file, console_output=False)
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_logger")
        
        # Check if log file was created
        self.assertTrue(os.path.exists(self.log_file))
    
    def test_setup_colored_logger(self):
        """Test colored logger setup"""
        logger = setup_logger("test_colored", "INFO", self.log_file)
        
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test_colored")
        
        # Check if log file was created
        self.assertTrue(os.path.exists(self.log_file))


if __name__ == '__main__':
    unittest.main()
