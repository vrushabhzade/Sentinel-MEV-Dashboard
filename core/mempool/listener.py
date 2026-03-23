import asyncio
import json
from loguru import logger
from web3 import Web3
from core.ethereum.connection import ethereum_conn
from core.strategies.sandwich_strategy import SandwichStrategy
from core.strategies.liquidation_strategy import LiquidationStrategy
from core.strategies.arbitrage_strategy import ArbitrageStrategy

class MempoolListener:
    def __init__(self):
        self.w3 = ethereum_conn.get_wss_provider()
        self.sandwich = SandwichStrategy(self.w3)
        self.liquidation = LiquidationStrategy(self.w3)
        self.arbitrage = ArbitrageStrategy(self.w3)

    async def transaction_filter(self):
        if not self.w3 or not self.w3.is_connected():
            logger.error("WSS Not connected. Cannot listen to mempool.")
            return

        logger.info("Starting Mempool Listener...")
        tx_filter = self.w3.eth.filter('pending')
        
        while True:
            try:
                new_entries = tx_filter.get_new_entries()
                for tx_hash in new_entries:
                    asyncio.create_task(self.handle_new_transaction(tx_hash))
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in mempool listener: {e}")
                await asyncio.sleep(2)

    async def handle_new_transaction(self, tx_hash):
        try:
            tx = self.w3.eth.get_transaction(tx_hash)
            
            # 1. Analyze for Sandwich opportunities
            if await self.sandwich.analyze_transaction(tx):
                logger.info(f"[!!] Profitable Sandwich target locked: {tx_hash.hex()}")
                await self.sandwich.execute_trade({"tx": tx})
                
            # 2. Analyze for Liquidation opportunities (Aave/Compound)
            if await self.liquidation.analyze_transaction(tx):
                mock_debt_cover = 100.0
                is_profitable, net_profit = await self.liquidation.calculate_profitability(tx.get('from'), mock_debt_cover)
                if is_profitable:
                    logger.info(f"[$$] Highly Profitable Liquidation target found: {tx_hash.hex()} expected: {net_profit} ETH")
                    await self.liquidation.execute_trade({"tx": tx, "profit": net_profit})

            # 3. Analyze for Cross-DEX Arbitrage opportunities
            if await self.arbitrage.analyze_transaction(tx):
                mock_amount_in = 5.0 # ETH
                is_profitable, net_profit, r1, r2 = await self.arbitrage.calculate_profitability("WETH", "TOKEN", mock_amount_in)
                if is_profitable:
                    logger.info(f"[▲] Triangular Arbitrage Discrepancy Found! expected: {net_profit} ETH")
                    await self.arbitrage.execute_trade({"tx": tx, "profit": net_profit, "routers": [r1, r2]})

        except Exception as e:
            logger.debug(f"Transaction dropped or already processed: {e}")

    def start(self):
        asyncio.run(self.transaction_filter())
