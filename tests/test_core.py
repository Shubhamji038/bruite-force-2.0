#!/usr/bin/env python3
"""
Test core functionality of Bruite Force tool
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bruite_force.core.target_info import TargetInfo, LoginForm
from bruite_force.core.reconnaissance import WebReconnaissance
from bruite_force.core.form_parser import LoginFormParser
from bruite_force.core.attack_engine import BruteForceEngine
from bruite_force.core.brute_force_tool import BruteForceTool


class TestTargetInfo(unittest.TestCase):
    """Test TargetInfo and LoginForm data classes"""
    
    def test_login_form_creation(self):
        """Test LoginForm creation and validation"""
        form = LoginForm(
            action_url="https://example.com/login",
            method="post",
            username_field="username",
            password_field="password",
            additional_fields={"csrf_token": "abc123"},
            form_data={}
        )
        
        self.assertEqual(form.action_url, "https://example.com/login")
        self.assertEqual(form.method, "post")
        self.assertEqual(form.username_field, "username")
        self.assertEqual(form.password_field, "password")
    
    def test_login_form_validation(self):
        """Test LoginForm validation"""
        # Valid form should not raise exception
        LoginForm(
            action_url="https://example.com/login",
            method="post",
            username_field="username",
            password_field="password",
            additional_fields={},
            form_data={}
        )
        
        # Invalid method should raise exception
        with self.assertRaises(ValueError):
            LoginForm(
                action_url="https://example.com/login",
                method="invalid",
                username_field="username",
                password_field="password",
                additional_fields={},
                form_data={}
            )
    
    def test_target_info_creation(self):
        """Test TargetInfo creation and methods"""
        target = TargetInfo(
            url="https://example.com",
            domain="example.com",
            login_forms=[],
            session_cookies={},
            headers={},
            success_indicators=["success"],
            failure_indicators=["error"]
        )
        
        self.assertEqual(target.url, "https://example.com")
        self.assertEqual(target.domain, "example.com")
        self.assertEqual(target.get_form_count(), 0)
        
        # Test adding a form
        form = LoginForm(
            action_url="https://example.com/login",
            method="post",
            username_field="username",
            password_field="password",
            additional_fields={},
            form_data={}
        )
        target.add_login_form(form)
        self.assertEqual(target.get_form_count(), 1)


class TestWebReconnaissance(unittest.TestCase):
    """Test WebReconnaissance class"""
    
    def setUp(self):
        self.recon = WebReconnaissance("https://example.com")
    
    @patch('bruite_force.core.reconnaissance.requests.Session.get')
    def test_get_basic_info_success(self, mock_get):
        """Test successful basic info gathering"""
        # Mock successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Server": "nginx", "X-Powered-By": "PHP"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        target_info = self.recon.get_basic_info()
        
        self.assertIsInstance(target_info, TargetInfo)
        self.assertEqual(target_info.url, "https://example.com")
        self.assertEqual(target_info.domain, "example.com")
    
    @patch('bruite_force.core.reconnaissance.requests.Session.get')
    def test_get_basic_info_failure(self, mock_get):
        """Test failed basic info gathering"""
        mock_get.side_effect = Exception("Connection error")
        
        with self.assertRaises(Exception):
            self.recon.get_basic_info()
    
    def test_discover_login_pages(self):
        """Test login page discovery"""
        pages = self.recon.discover_login_pages("https://example.com")
        
        # Should always return at least the base URL
        self.assertIn("https://example.com", pages)


class TestLoginFormParser(unittest.TestCase):
    """Test LoginFormParser class"""
    
    def setUp(self):
        self.mock_session = Mock()
        self.parser = LoginFormParser(self.mock_session)
    
    @patch('bruite_force.core.form_parser.BeautifulSoup')
    def test_extract_login_forms_success(self, mock_soup):
        """Test successful login form extraction"""
        # Mock HTML response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<html><body></body></html>"
        self.mock_session.get.return_value = mock_response
        
        # Mock BeautifulSoup parsing
        mock_soup_instance = Mock()
        mock_soup_instance.find_all.return_value = []
        mock_soup.return_value = mock_soup_instance
        
        forms = self.parser.extract_login_forms("https://example.com")
        
        self.assertIsInstance(forms, list)


class TestBruteForceEngine(unittest.TestCase):
    """Test BruteForceEngine class"""
    
    def setUp(self):
        self.target_info = TargetInfo(
            url="https://example.com",
            domain="example.com",
            login_forms=[],
            session_cookies={},
            headers={},
            success_indicators=["success"],
            failure_indicators=["error"]
        )
        self.engine = BruteForceEngine(self.target_info)
    
    def test_load_wordlist_success(self):
        """Test successful wordlist loading"""
        # Create a temporary wordlist file
        wordlist_path = "test_wordlist.txt"
        with open(wordlist_path, 'w') as f:
            f.write("password1\npassword2\npassword3\n")
        
        try:
            passwords = self.engine.load_wordlist(wordlist_path)
            self.assertEqual(len(passwords), 3)
            self.assertIn("password1", passwords)
        finally:
            os.remove(wordlist_path)
    
    def test_load_wordlist_failure(self):
        """Test wordlist loading failure"""
        passwords = self.engine.load_wordlist("nonexistent.txt")
        self.assertEqual(len(passwords), 0)
    
    def test_generate_password_variations(self):
        """Test password variation generation"""
        base_passwords = ["password"]
        usernames = ["admin"]
        
        variations = self.engine.generate_password_variations(base_passwords, usernames)
        
        # Should include original passwords and variations
        self.assertIn("password", variations)
        self.assertIn("admin", variations)
        self.assertIn("admin123", variations)


class TestBruteForceTool(unittest.TestCase):
    """Test BruteForceTool class"""
    
    def setUp(self):
        self.tool = BruteForceTool(
            target_url="https://example.com",
            wordlist_path="test_wordlist.txt",
            usernames=["admin"]
        )
    
    @patch('bruite_force.core.brute_force_tool.WebReconnaissance')
    def test_initialization(self, mock_recon):
        """Test tool initialization"""
        self.assertEqual(self.tool.target_url, "https://example.com")
        self.assertEqual(self.tool.wordlist_path, "test_wordlist.txt")
        self.assertEqual(self.tool.usernames, ["admin"])


if __name__ == '__main__':
    unittest.main()
