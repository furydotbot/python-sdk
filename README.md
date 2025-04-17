# FURY SDK for Python

A Python client library for interacting with the FURY API service - a comprehensive toolkit for Solana token operations.

## Features

- **Complete API Coverage** - Access to all FURY API endpoints
- **Type Hints** - Full Python type annotations for better IDE support
- **Helper Models** - Data classes for simpler request construction
- **Error Handling** - Custom exceptions with detailed error information
- **Validation** - Built-in parameter validation

## Installation

### Requirements

- Python 3.7+
- `requests` library for HTTP requests
- `solana-py` and `base58` for transaction signing (optional, only needed if signing transactions)

### Install Dependencies

```bash
pip install requests
pip install solana base58  # Only needed for transaction signing
```

### Install FURY SDK

```bash
# From PyPI (when published)
pip install fury-sdk

# From source
git clone https://github.com/your-username/fury-sdk.git
cd fury-sdk
pip install -e .
```

## Quick Start

```python
from fury_sdk import FurySDK

# Initialize the SDK
fury = FurySDK("https://api.fury.bot", api_key="your_api_key_here")  # API key is optional

# Check API health
health = fury.health_check()
print(health)

# Generate a new mint key
mint_key = fury.utilities.generate_mint()
print(f"Generated mint key: {mint_key['pubkey']}")
```

## Usage Examples

### Buy Tokens

```python
from fury_sdk import FurySDK, Protocol

fury = FurySDK("https://api.fury.bot")

# Buy tokens
result = fury.tokens.buy(
    wallet_addresses=["FuRytmqsoo4mKQAhNXoB64JD4SsiVqxYkUKC6i1VaBot"],
    token_address="Bq5nFQ82jBYcFKRzUSximpCmCg5t8L8tVMqsn612pump",
    sol_amount=1.5,
    protocol=Protocol.PUMPFUN,
    slippage_bps=9990
)
print(f"Transaction data: {result['transactions']}")
```

### Complete Buy Flow with Transaction Signing

```python
from fury_sdk import FurySDK, Protocol
from solana.keypair import Keypair
from solana.transaction import Transaction
import base58
import json

# Initialize SDK
fury = FurySDK("https://api.fury.bot")

# Load wallet
with open('wallet_keypair.json', 'r') as f:
    keypair_data = json.load(f)
keypair = Keypair.from_secret_key(bytes(keypair_data))

# Generate buy transaction
result = fury.tokens.buy(
    wallet_addresses=[base58.b58encode(keypair.public_key.to_bytes()).decode('ascii')],
    token_address="Bq5nFQ82jBYcFKRzUSximpCmCg5t8L8tVMqsn612pump",
    sol_amount=0.5,
    protocol=Protocol.PUMPFUN
)

# Sign transactions
signed_transactions = []
for tx_base64 in result['transactions']:
    tx_bytes = base58.b58decode(tx_base64)
    transaction = Transaction.deserialize(tx_bytes)
    transaction.sign([keypair])
    signed_tx_data = transaction.serialize()
    signed_transactions.append({
        "transaction": base58.b58encode(signed_tx_data).decode('ascii'),
        "options": {"skipPreflight": False, "preflightCommitment": "confirmed"}
    })

# Send signed transactions
send_result = fury.transactions.send(
    transactions=signed_transactions,
    use_rpc=False
)
print(f"Transaction signatures: {send_result['results']}")
```

### Create a New Token

```python
from fury_sdk import FurySDK, TokenMetadata, create_token_config

fury = FurySDK("https://api.fury.bot")

# Generate a mint key
mint_key = fury.utilities.generate_mint()
mint_pubkey = mint_key["pubkey"]

# Create token metadata
metadata = TokenMetadata(
    name="Test Token",
    symbol="TEST",
    description="A test token created with FURY SDK",
    file="https://example.com/logo.png",
    website="https://example.com"
)

# Create token
token_config = create_token_config(metadata)
result = fury.tokens.create(
    wallet_addresses=["5tqe3S1zsfAmT7L2Ru5gVJDaq4wUB7AbCpTLPaxaM6eG"],
    mint_pubkey=mint_pubkey,
    config=token_config,
    amounts=[0.1]
)
print(f"Token created: {result}")
```

### Distribute Tokens to Multiple Wallets

```python
from fury_sdk import FurySDK, Recipient

fury = FurySDK("https://api.fury.bot")

# Define recipients
recipients = [
    Recipient("8fwjXcyQrCCkG5k3vHUioVLNbPr72otA59mmR1w6CwpS", "0.01"),
    Recipient("68qzyqvqX3eEGEfwa2ajsDKmEjhmU9XRj1VjcUPJNwpq", "0.01")
]

# Distribute tokens
result = fury.wallets.distribute(
    sender="2chjSgQNmEkHWH6zmj1BgT8q1fSCzS6FcJiatYq4Atcs",
    recipients=[r.to_dict() for r in recipients]
)
print(f"Distribution transactions: {result['transactions']}")
```

## API Reference

### Main SDK Class

- `FurySDK(base_url, api_key=None)` - Initialize the SDK
- `health_check()` - Check API health

### Token Operations

- `tokens.buy(wallet_addresses, token_address, sol_amount, protocol="auto", ...)` - Buy tokens
- `tokens.sell(wallet_addresses, token_address, percentage=100, protocol="auto", ...)` - Sell tokens
- `tokens.transfer(sender_public_key, receiver, token_address, amount)` - Transfer tokens
- `tokens.create(wallet_addresses, mint_pubkey, config, amounts)` - Create a new token
- `tokens.burn(wallet_public_key, token_address, amount)` - Burn tokens
- `tokens.cleaner(seller_address, buyer_address, token_address, sell_percentage, buy_percentage)` - Execute buy/sell operations

### Transaction Operations

- `transactions.send(transactions, use_rpc=False)` - Submit transactions

### Analytics Operations

- `analytics.calculate_pnl(addresses, token_address=None, include_timestamp=False)` - Calculate profit and loss

### Utility Operations

- `utilities.generate_mint()` - Generate a new mint public key

### Wallet Operations

- `wallets.distribute(sender, recipients)` - Distribute tokens to multiple wallets
- `wallets.consolidate(source_addresses, receiver_address, percentage=100, token_address=None)` - Consolidate tokens from multiple wallets

## Error Handling

```python
from fury_sdk import FurySDK, FuryAPIError

fury = FurySDK("https://api.fury.bot")

try:
    result = fury.tokens.buy(...)
    print(f"Success: {result}")
except FuryAPIError as e:
    print(f"API Error ({e.status_code}): {e}")
    if e.error_data:
        print(f"Error details: {e.error_data}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.