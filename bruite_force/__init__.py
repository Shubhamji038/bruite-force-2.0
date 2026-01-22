"""
Bruite Force - Educational Web Security Testing Tool

A comprehensive Python package for educational web security testing,
including brute force attacks, form analysis, and reconnaissance.

⚠️ EDUCATIONAL USE ONLY ⚠️
This tool is designed for educational purposes and authorized security testing only.
"""

__version__ = "2.0.0"
__author__ = "Educational Demo"
__email__ = "demo@example.com"

from .core.brute_force_tool import BruteForceTool
from .core.target_info import TargetInfo, LoginForm
from .core.reconnaissance import WebReconnaissance
from .core.form_parser import LoginFormParser
from .core.attack_engine import BruteForceEngine
from .utils.config_manager import ConfigManager
from .utils.logger import setup_logger
from .wizard import ConfigWizard

__all__ = [
    'BruteForceTool',
    'TargetInfo',
    'LoginForm', 
    'WebReconnaissance',
    'LoginFormParser',
    'BruteForceEngine',
    'ConfigManager',
    'setup_logger',
    'ConfigWizard'
]
