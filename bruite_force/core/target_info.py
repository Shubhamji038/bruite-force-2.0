"""
Data classes for storing target and form information
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class LoginForm:
    """Data class to store login form information"""
    action_url: str
    method: str
    username_field: str
    password_field: str
    additional_fields: Dict[str, str]
    form_data: Dict[str, str]

    def __post_init__(self):
        """Validate form data after initialization"""
        if not self.action_url:
            raise ValueError("action_url cannot be empty")
        if not self.username_field:
            raise ValueError("username_field cannot be empty")
        if not self.password_field:
            raise ValueError("password_field cannot be empty")
        if self.method.lower() not in ['get', 'post']:
            raise ValueError("method must be either 'get' or 'post'")


@dataclass
class TargetInfo:
    """Data class to store target website information"""
    url: str
    domain: str
    login_forms: List[LoginForm]
    session_cookies: Dict[str, str]
    headers: Dict[str, str]
    success_indicators: List[str]
    failure_indicators: List[str]

    def __post_init__(self):
        """Validate target info after initialization"""
        if not self.url:
            raise ValueError("url cannot be empty")
        if not self.domain:
            raise ValueError("domain cannot be empty")

    def add_login_form(self, form: LoginForm):
        """Add a login form to the target"""
        self.login_forms.append(form)

    def get_form_count(self) -> int:
        """Get the number of login forms found"""
        return len(self.login_forms)
