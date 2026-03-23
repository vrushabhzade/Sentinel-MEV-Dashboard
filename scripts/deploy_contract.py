import os
import sys
import json
import logging
from web3 import Web3
from dotenv import load_dotenv

# Ensure core config works if invoked from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings
from core.ethereum.connection import ethereum_conn

logger = logging.getLogger(__name__)

def deploy_sandwich_bot():
    logger.info("Starting SandwichBot Smart Contract Deployment...")
    
    w3 = ethereum_conn.get_http_provider()
    
    if not w3.is_connected():
        logger.error("Failed to connect to HTTP Provider. Check your ETH_HTTP_URL in .env")
        return

    # To deploy, you'd compile `core/ethereum/contracts/SandwichBot.sol`
    # You can use tools like `solc` or `Brownie`/`Hardhat` to get the ABI and Bytecode.
    # For now, we stub them. 
    # MOCK ABI & BYTECODE (Replace these after compiling the Solidity contract!)
    contract_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"router","type":"address"},{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint256","name":"minerBribe","type":"uint256"}],"name":"backrunSell","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"router","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"}],"name":"frontrunBuy","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
    contract_bytecode = "0x" # Replace with actual bytecode
    
    if contract_bytecode == "0x":
        logger.error("No bytecode found. Please compile SandwichBot.sol using solc/foundry and paste the hex here first!")
        return

    acc = w3.eth.account.from_key(settings.PRIVATE_KEY)
    logger.info(f"Deploying with account: {acc.address}")
    
    SandwichContract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    
    nonce = w3.eth.get_transaction_count(acc.address)
    tx = SandwichContract.constructor().build_transaction({
        'from': acc.address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=settings.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.info(f"Sent deployment transaction! Hash: {tx_hash.hex()}")
    
    logger.info("Waiting for transaction receipt...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    logger.info(f"Deployed successfully! Contract Address: {tx_receipt.contractAddress}")
    
    # Normally, you would write this address back into the `.env` file automatically
    return tx_receipt.contractAddress

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    deploy_sandwich_bot()
