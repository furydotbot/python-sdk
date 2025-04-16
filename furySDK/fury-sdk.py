"""
Main FURY SDK class that serves as the entry point for all API operations.
"""
import requests
from typing import Dict, Optional, List, Any, Union

from .clients import (
    TokensClient,
    TransactionsClient,
    AnalyticsClient,
    UtilitiesClient,
    WalletsClient,
)
from .exceptions import FuryAPIError


class FurySDK:
    """
    FURY API SDK main class.
    
    Provides access to all API endpoints through client classes.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the FURY SDK.
        
        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        
        self._session = requests.Session()
        if api_key:
            self._session.headers.update({'Authorization': f'Bearer {api_key}'})
        
        # Initialize clients
        self.tokens = TokensClient(self)
        self.transactions = TransactionsClient(self)
        self.analytics = AnalyticsClient(self)
        self.utilities = UtilitiesClient(self)
        self.wallets = WalletsClient(self)
    
    def request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            API response as a dictionary
            
        Raises:
            FuryAPIError: If the API returns an error
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self._session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    raise FuryAPIError(
                        status_code=e.response.status_code,
                        message=error_data.get('message', str(e)),
                        error_data=error_data
                    )
                except ValueError:
                    pass
            
            raise FuryAPIError(
                status_code=getattr(e, 'response', None) and e.response.status_code, 
                message=str(e)
            )
    
    def health_check(self) -> Dict:
        """
        Check if the API is healthy.
        
        Returns:
            Health status information
        """
        return self.request('GET', '/health')