"""
Example showing how to buy tokens on Solana using the FURY SDK,
including signing the transactions and sending them.
"""
from furySDK import FurySDK, FuryAPIError, Protocol
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.rpc.types import TxOpts
import base58
import json

def main():
    # Initialize the SDK with your API base URL
    # You can add your API key as the second parameter if required
    fury = FurySDK("https://solana.fury.bot")
    
    # Wallet address(es) that will be buying tokens
    wallet_addresses = ["FuRytmqsoo4mKQAhNXoB64JD4SsiVqxYkUKC6i1VaBot"]
    
    # Load private keys for signing transactions
    # This example assumes you have a JSON file with your private key
    # NEVER hardcode private keys in production code
    with open('wallet_keypair.json', 'r') as f:
        keypair_data = json.load(f)
    
    # Create keypair from private key bytes
    # In this example we use the first wallet from wallet_addresses
    private_key_bytes = bytes(keypair_data)
    keypair = Keypair.from_secret_key(private_key_bytes)
    
    # Verify the public key matches what we expect
    assert base58.b58encode(keypair.public_key.to_bytes()).decode('ascii') == wallet_addresses[0], \
        "Keypair doesn't match provided wallet address!"
    
    # The token you want to buy (token mint address)
    token_address = "Bq5nFQ82jBYcFKRzUSximpCmCg5t8L8tVMqsn612pump"
    
    # Amount of SOL to spend
    sol_amount = 0.5
    
    # Specify which protocol to use (or use "auto" to let the API choose the best one)
    protocol = Protocol.PUMPFUN  # Or use "pumpfun" string directly
    
    # Optional parameters
    slippage_bps = 9990  # 99.9% slippage tolerance
    jito_tip_lamports = 5000000  # Optional tip for Jito MEV block builders

    try:
        # 1. Generate the buy transaction (returns partially signed transactions)
        result = fury.tokens.buy(
            wallet_addresses=wallet_addresses,
            token_address=token_address,
            sol_amount=sol_amount,
            protocol=protocol,
            slippage_bps=slippage_bps,
            jito_tip_lamports=jito_tip_lamports
        )
        
        print(f"Generated {len(result['transactions'])} transaction(s) to sign")
        
        # 2. Sign the transactions
        signed_transactions = []
        
        for tx_base64 in result['transactions']:
            # Convert the base64 transaction to a Transaction object
            # This is pseudo-code - the exact implementation depends on your Solana library
            tx_bytes = base58.b58decode(tx_base64)
            transaction = Transaction.deserialize(tx_bytes)
            
            # Sign the transaction with our keypair
            transaction.sign([keypair])
            
            # Convert back to serialized format
            signed_tx_data = transaction.serialize()
            
            # Add to our list of signed transactions
            signed_transactions.append({
                "transaction": base58.b58encode(signed_tx_data).decode('ascii'),
                "options": {
                    "skipPreflight": False,
                    "preflightCommitment": "confirmed"
                }
            })
        
        # 3. Send the signed transactions
        send_result = fury.transactions.send(
            transactions=signed_transactions,
            use_rpc=False  # Use the bundle service for better chances of success
        )
        
        # Print transaction results
        print("Buy transaction successful!")
        print(f"Transaction signatures: {send_result['results']}")
        
        # You can now use the transaction signatures to check the status on a block explorer
        for tx in send_result['results']:
            print(f"View on Solana Explorer: https://solscan.io/tx/{tx}")
        
    except FuryAPIError as e:
        print(f"Error buying tokens: {e}")
        if hasattr(e, 'error_data') and e.error_data:
            print(f"Error details: {e.error_data}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()