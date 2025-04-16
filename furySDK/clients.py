"""
Client classes for each API category in the FURY API service.
"""
from typing import Dict, List, Optional, Any, Union


class BaseClient:
    """Base client class for API endpoints."""
    
    def __init__(self, sdk):
        """
        Initialize the client.
        
        Args:
            sdk: The FurySDK instance
        """
        self.sdk = sdk


class TokensClient(BaseClient):
    """Client for token-related operations."""
    
    def buy(self, wallet_addresses: List[str], token_address: str, sol_amount: float, 
            protocol: str = "auto", affiliate_address: Optional[str] = None, 
            affiliate_fee: Optional[str] = None, jito_tip_lamports: Optional[int] = None, 
            slippage_bps: Optional[int] = None) -> Dict:
        """
        Buy tokens through various protocols.
        
        Args:
            wallet_addresses: List of wallet addresses initiating the buy
            token_address: Address of the token to buy
            sol_amount: Amount of SOL to spend
            protocol: The protocol to use for buying ('raydium', 'jupiter', 'pumpfun', 'moonshot', 'pumpswap', 'auto')
            affiliate_address: Optional affiliate address for fee sharing
            affiliate_fee: Optional affiliate fee percentage (as a string, e.g., '2' for 2%)
            jito_tip_lamports: Optional Jito tip amount in lamports
            slippage_bps: Optional slippage tolerance in basis points
            
        Returns:
            Transaction information
        """
        data = {
            "walletAddresses": wallet_addresses,
            "tokenAddress": token_address,
            "solAmount": sol_amount,
            "protocol": protocol
        }
        
        if affiliate_address:
            data["affiliateAddress"] = affiliate_address
        
        if affiliate_fee:
            data["affiliateFee"] = affiliate_fee
            
        if jito_tip_lamports:
            data["jitoTipLamports"] = jito_tip_lamports
            
        if slippage_bps:
            data["slippageBps"] = slippage_bps
        
        return self.sdk.request('POST', '/api/tokens/buy', json=data)
    
    def sell(self, wallet_addresses: List[str], token_address: str, percentage: int = 100,
             protocol: str = "auto", affiliate_address: Optional[str] = None,
             affiliate_fee: Optional[str] = None, jito_tip_lamports: Optional[int] = None,
             slippage_bps: Optional[int] = None) -> Dict:
        """
        Sell tokens through various protocols.
        
        Args:
            wallet_addresses: List of wallet addresses initiating the sell
            token_address: Address of the token to sell
            percentage: Percentage of the token balance to sell (1-100)
            protocol: The protocol to use for selling ('raydium', 'jupiter', 'pumpfun', 'moonshot', 'pumpswap', 'auto')
            affiliate_address: Optional affiliate address for fee sharing
            affiliate_fee: Optional affiliate fee percentage (as a string, e.g., '2' for 2%)
            jito_tip_lamports: Optional Jito tip amount in lamports
            slippage_bps: Optional slippage tolerance in basis points
            
        Returns:
            Transaction information
        """
        data = {
            "walletAddresses": wallet_addresses,
            "tokenAddress": token_address,
            "percentage": percentage,
            "protocol": protocol
        }
        
        if affiliate_address:
            data["affiliateAddress"] = affiliate_address
        
        if affiliate_fee:
            data["affiliateFee"] = affiliate_fee
            
        if jito_tip_lamports:
            data["jitoTipLamports"] = jito_tip_lamports
            
        if slippage_bps:
            data["slippageBps"] = slippage_bps
        
        return self.sdk.request('POST', '/api/tokens/sell', json=data)
    
    def transfer(self, sender_public_key: str, receiver: str, token_address: str, amount: str) -> Dict:
        """
        Transfer tokens between wallets.
        
        Args:
            sender_public_key: Source wallet address
            receiver: Destination wallet address
            token_address: Address of the token to transfer (empty for SOL)
            amount: Amount of tokens to transfer (as a string)
            
        Returns:
            Transaction information
        """
        data = {
            "senderPublicKey": sender_public_key,
            "receiver": receiver,
            "tokenAddress": token_address,
            "amount": amount
        }
        
        return self.sdk.request('POST', '/api/tokens/transfer', json=data)
    
    def create(self, wallet_addresses: List[str], mint_pubkey: str, config: Dict, amounts: List[float]) -> Dict:
        """
        Create/mint a new token.
        
        Args:
            wallet_addresses: Array of wallet addresses that will receive initial token distribution
            mint_pubkey: Public key of the mint
            config: Configuration options for token creation
            amounts: Array of SOL amounts to be used for each wallet
            
        Returns:
            Transaction information
        """
        data = {
            "walletAddresses": wallet_addresses,
            "mintPubkey": mint_pubkey,
            "config": config,
            "amounts": amounts
        }
        
        return self.sdk.request('POST', '/api/tokens/create', json=data)
    
    def burn(self, wallet_public_key: str, token_address: str, amount: str) -> Dict:
        """
        Burn (destroy) tokens.
        
        Args:
            wallet_public_key: Wallet address
            token_address: Address of the token to burn
            amount: Amount of tokens to burn (as a string)
            
        Returns:
            Transaction information
        """
        data = {
            "walletPublicKey": wallet_public_key,
            "tokenAddress": token_address,
            "amount": amount
        }
        
        return self.sdk.request('POST', '/api/tokens/burn', json=data)
    
    def cleaner(self, seller_address: str, buyer_address: str, token_address: str,
                sell_percentage: float, buy_percentage: float) -> Dict:
        """
        Execute buy/sell operations in one call.
        
        Args:
            seller_address: Specific wallet address for selling
            buyer_address: Specific wallet address for buying
            token_address: Address of the token to operate on
            sell_percentage: Percentage of tokens to sell (can include decimals)
            buy_percentage: Percentage of available SOL to use for buying (can include decimals)
            
        Returns:
            Transaction information
        """
        data = {
            "sellerAddress": seller_address,
            "buyerAddress": buyer_address,
            "tokenAddress": token_address,
            "sellPercentage": sell_percentage,
            "buyPercentage": buy_percentage
        }
        
        return self.sdk.request('POST', '/api/tokens/cleaner', json=data)


class TransactionsClient(BaseClient):
    """Client for transaction-related operations."""
    
    def send(self, transactions: List[Dict], use_rpc: bool = False) -> Dict:
        """
        Submit a bundle of transactions.
        
        Args:
            transactions: Array of transaction objects
            use_rpc: Whether to use RPC instead of bundle service
            
        Returns:
            Transaction results
        """
        data = {
            "transactions": transactions,
            "useRpc": use_rpc
        }
        
        return self.sdk.request('POST', '/api/transactions/send', json=data)


class AnalyticsClient(BaseClient):
    """Client for analytics-related operations."""
    
    def calculate_pnl(self, addresses: str, token_address: Optional[str] = None, 
                      include_timestamp: bool = False) -> Dict:
        """
        Calculate profit and loss for a wallet or token.
        
        Args:
            addresses: Comma-separated list of wallet addresses to calculate PnL for
            token_address: Token address to calculate PnL for
            include_timestamp: Include timestamp in the response
            
        Returns:
            PnL calculation results
        """
        data = {
            "addresses": addresses
        }
        
        if token_address:
            data["tokenAddress"] = token_address
            
        if include_timestamp:
            data["options"] = {"includeTimestamp": True}
        
        return self.sdk.request('POST', '/api/analytics/pnl', json=data)


class UtilitiesClient(BaseClient):
    """Client for utility operations."""
    
    def generate_mint(self) -> Dict:
        """
        Generate a new mint public key.
        
        Returns:
            Generated mint key information
        """
        return self.sdk.request('GET', '/api/utilities/generate-mint')


class WalletsClient(BaseClient):
    """Client for wallet-related operations."""
    
    def distribute(self, sender: str, recipients: List[Dict[str, str]]) -> Dict:
        """
        Distribute tokens to multiple wallets.
        
        Args:
            sender: Source wallet address
            recipients: Array of recipient objects with address and amount
            
        Returns:
            Transaction information
        """
        data = {
            "sender": sender,
            "recipients": recipients
        }
        
        return self.sdk.request('POST', '/api/wallets/distribute', json=data)
    
    def consolidate(self, source_addresses: List[str], receiver_address: str, 
                    percentage: int = 100, token_address: Optional[str] = None) -> Dict:
        """
        Consolidate tokens from multiple wallets into one.
        
        Args:
            source_addresses: Array of source wallet addresses
            receiver_address: Destination wallet address
            percentage: Percentage of tokens to consolidate (1-100)
            token_address: Address of the token to consolidate
            
        Returns:
            Transaction information
        """
        data = {
            "sourceAddresses": source_addresses,
            "receiverAddress": receiver_address,
            "percentage": percentage
        }
        
        if token_address:
            data["tokenAddress"] = token_address
        
        return self.sdk.request('POST', '/api/wallets/consolidate', json=data)