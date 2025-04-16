"""
Data models and helper classes for the FURY SDK.
"""
from typing import Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class TokenMetadata:
    """Token metadata configuration."""
    name: str
    symbol: str
    description: str
    file: str  # Token logo image URL
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None


@dataclass
class TokenCreationConfig:
    """Configuration for token creation."""
    metadata: TokenMetadata
    default_sol_amount: float = 0.1

    def to_dict(self) -> Dict:
        """Convert to API-compatible dictionary format."""
        return {
            "tokenCreation": {
                "metadata": {
                    "name": self.metadata.name,
                    "symbol": self.metadata.symbol,
                    "description": self.metadata.description,
                    "file": self.metadata.file,
                    "telegram": self.metadata.telegram or "",
                    "twitter": self.metadata.twitter or "",
                    "website": self.metadata.website or ""
                },
                "defaultSolAmount": self.default_sol_amount
            }
        }


@dataclass
class Recipient:
    """Token recipient information."""
    address: str
    amount: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return {
            "address": self.address,
            "amount": self.amount
        }


class Protocol:
    """Supported trading protocols."""
    RAYDIUM = "raydium"
    JUPITER = "jupiter"
    PUMPFUN = "pumpfun"
    MOONSHOT = "moonshot"
    PUMPSWAP = "pumpswap"
    AUTO = "auto"
    
    @classmethod
    def values(cls) -> List[str]:
        """Get list of supported protocol values."""
        return [cls.RAYDIUM, cls.JUPITER, cls.PUMPFUN, cls.MOONSHOT, cls.PUMPSWAP, cls.AUTO]
    
    @classmethod
    def validate(cls, protocol: str) -> str:
        """
        Validate a protocol value.
        
        Args:
            protocol: Protocol name to validate
            
        Returns:
            Validated protocol name
            
        Raises:
            ValueError: If protocol is not supported
        """
        if protocol.lower() not in cls.values():
            raise ValueError(f"Invalid protocol: {protocol}. Must be one of: {', '.join(cls.values())}")
        return protocol.lower()


def create_token_config(metadata: TokenMetadata, default_sol_amount: float = 0.1) -> Dict:
    """
    Create a token configuration dictionary.
    
    Args:
        metadata: Token metadata
        default_sol_amount: Default SOL amount for creating token
        
    Returns:
        Token configuration dictionary for API request
    """
    return TokenCreationConfig(metadata, default_sol_amount).to_dict()