"""
FURY API SDK - A Python client library for interacting with the FURY API.

Simple usage example:
    
    from fury_sdk import FurySDK
    
    # Initialize the SDK
    fury = FurySDK("https://api.fury.bot")
    
    # Check API health
    health = fury.health_check()
    print(health)
    
    # Generate a new mint key
    mint_key = fury.utilities.generate_mint()
    print(f"Generated mint key: {mint_key['pubkey']}")
    
    # Buy tokens
    result = fury.tokens.buy(
        wallet_addresses=["FuRytmqsoo4mKQAhNXoB64JD4SsiVqxYkUKC6i1VaBot"],
        token_address="Bq5nFQ82jBYcFKRzUSximpCmCg5t8L8tVMqsn612pump",
        sol_amount=1.5,
        protocol="pumpfun"
    )
    print(f"Transaction signatures: {result['transactions']}")
"""

from furySDK import FurySDK
from .exceptions import FurySDKError, FuryAPIError, ValidationError
from .models import (
    TokenMetadata, 
    TokenCreationConfig, 
    Recipient, 
    Protocol, 
    create_token_config
)

__version__ = "1.0.0"
__all__ = [
    'FurySDK',
    'FurySDKError',
    'FuryAPIError',
    'ValidationError',
    'TokenMetadata',
    'TokenCreationConfig',
    'Recipient',
    'Protocol',
    'create_token_config',
]