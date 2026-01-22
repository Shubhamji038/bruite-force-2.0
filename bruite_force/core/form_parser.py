"""
Module for parsing and analyzing login forms
"""

import logging
from urllib.parse import urljoin
from typing import List, Optional
from bs4 import BeautifulSoup

from .target_info import LoginForm
from ..utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class LoginFormParser:
    """Module for parsing and analyzing login forms"""
    
    def __init__(self, session, config_manager: ConfigManager = None):
        self.session = session
        self.config = config_manager or ConfigManager()
    
    def extract_login_forms(self, url: str) -> List[LoginForm]:
        """Extract login forms from a webpage"""
        try:
            timeout = self.config.get_timeout()
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            login_forms = []
            forms = soup.find_all('form')
            
            # First try traditional forms
            for form in forms:
                login_form = self._analyze_form(form, url)
                if login_form:
                    login_forms.append(login_form)
                    logger.info(f"Found traditional login form: {login_form.action_url}")
            
            # If no traditional forms found, look for modern JS-based login
            if not login_forms:
                js_forms = self._detect_js_login_forms(soup, url)
                login_forms.extend(js_forms)
            
            return login_forms
            
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return []
    
    def _analyze_form(self, form, base_url: str) -> Optional[LoginForm]:
        """Analyze a single form to determine if it's a login form"""
        try:
            # Get form action and method
            action = form.get('action', '')
            if action:
                action = urljoin(base_url, action)
            else:
                action = base_url
            
            method = form.get('method', 'get').lower()
            
            # Find input fields
            inputs = form.find_all('input')
            username_field = None
            password_field = None
            additional_fields = {}
            
            # Get patterns from config
            username_patterns = self.config.get_username_patterns()
            password_patterns = self.config.get_password_patterns()
            
            for input_tag in inputs:
                input_type = input_tag.get('type', '').lower()
                input_name = input_tag.get('name', '').lower()
                input_id = input_tag.get('id', '').lower()
                
                if input_type == 'password':
                    password_field = input_tag.get('name') or input_tag.get('id')
                elif any(pattern in input_name or pattern in input_id for pattern in username_patterns):
                    username_field = input_tag.get('name') or input_tag.get('id')
                else:
                    # Store additional fields
                    field_name = input_tag.get('name') or input_tag.get('id')
                    field_value = input_tag.get('value', '')
                    if field_name:
                        additional_fields[field_name] = field_value
            
            # Check if this looks like a login form
            if username_field and password_field:
                return LoginForm(
                    action_url=action,
                    method=method,
                    username_field=username_field,
                    password_field=password_field,
                    additional_fields=additional_fields,
                    form_data={}
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing form: {e}")
            return None
    
    def _detect_js_login_forms(self, soup, base_url: str) -> List[LoginForm]:
        """Detect JavaScript-based login forms by analyzing input elements"""
        login_forms = []
        
        try:
            # Look for input elements that suggest a login form
            all_inputs = soup.find_all('input')
            username_field = None
            password_field = None
            
            username_patterns = self.config.get_username_patterns()
            password_patterns = self.config.get_password_patterns()
            
            for input_tag in all_inputs:
                input_type = input_tag.get('type', '').lower()
                input_name = input_tag.get('name', '').lower()
                input_id = input_tag.get('id', '').lower()
                input_placeholder = input_tag.get('placeholder', '').lower()
                
                if input_type == 'password':
                    password_field = input_tag.get('name') or input_tag.get('id')
                elif any(pattern in input_name or pattern in input_id or pattern in input_placeholder 
                        for pattern in username_patterns):
                    username_field = input_tag.get('name') or input_tag.get('id')
            
            # If we found both username and password fields, create a form
            if username_field and password_field:
                # Try to find the login endpoint by analyzing JavaScript or common patterns
                login_endpoints = [
                    '/api/login',
                    '/auth/login', 
                    '/api/auth/login',
                    '/login',
                    '/signin',
                    '/api/signin',
                    '/auth/signin'
                ]
                
                for endpoint in login_endpoints:
                    login_url = urljoin(base_url, endpoint)
                    login_form = LoginForm(
                        action_url=login_url,
                        method='post',
                        username_field=username_field,
                        password_field=password_field,
                        additional_fields={},
                        form_data={}
                    )
                    login_forms.append(login_form)
                    logger.info(f"Detected potential JS login form: {login_url}")
        
        except Exception as e:
            logger.error(f"Error detecting JS login forms: {e}")
        
        return login_forms
