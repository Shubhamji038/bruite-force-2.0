"""
Module for gathering information about target websites
"""

import requests
import logging
from urllib.parse import urljoin, urlparse
from typing import List

from .target_info import TargetInfo
from ..utils.config_manager import ConfigManager

logger = logging.getLogger(__name__)


class WebReconnaissance:
    """Module for gathering information about target website"""
    
    def __init__(self, target_url: str, config_manager: ConfigManager = None):
        self.target_url = target_url
        self.config = config_manager or ConfigManager()
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """Setup session with headers and configuration"""
        user_agents = self.config.get_user_agents()
        self.session.headers.update({
            'User-Agent': user_agents[0] if user_agents else self.config.get_default_user_agent()
        })
    
    def get_basic_info(self) -> TargetInfo:
        """Gather basic information about the target"""
        try:
            timeout = self.config.get_timeout()
            response = self.session.get(self.target_url, timeout=timeout)
            response.raise_for_status()
            
            parsed_url = urlparse(self.target_url)
            domain = parsed_url.netloc
            
            # Extract server information
            server = response.headers.get('Server', 'Unknown')
            powered_by = response.headers.get('X-Powered-By', 'Unknown')
            
            logger.info(f"Target: {domain}")
            logger.info(f"Server: {server}")
            logger.info(f"Powered by: {powered_by}")
            logger.info(f"Status Code: {response.status_code}")
            
            return TargetInfo(
                url=self.target_url,
                domain=domain,
                login_forms=[],
                session_cookies=dict(self.session.cookies),
                headers=dict(response.headers),
                success_indicators=self.config.get_success_indicators(),
                failure_indicators=self.config.get_failure_indicators()
            )
            
        except requests.RequestException as e:
            logger.error(f"Failed to connect to {self.target_url}: {e}")
            raise
    
    def discover_login_pages(self, base_url: str) -> List[str]:
        """Discover potential login pages"""
        common_paths = self.config.get_common_login_paths()
        discovered_pages = [base_url]
        
        for path in common_paths:
            test_url = urljoin(base_url, path)
            try:
                response = self.session.get(test_url, timeout=5)
                if response.status_code == 200:
                    discovered_pages.append(test_url)
                    logger.info(f"Discovered login page: {test_url}")
            except requests.RequestException:
                continue
        
        return discovered_pages
    
    def test_connectivity(self) -> bool:
        """Test if target is reachable"""
        try:
            response = self.session.get(self.target_url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False
