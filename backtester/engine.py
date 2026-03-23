import logging
import pandas as pd
from typing import List, Dict, Any

from config.settings import settings
from core.strategies.sandwich_strategy import SandwichStrategy
from core.strategies.liquidation_strategy import LiquidationStrategy

logger = logging.getLogger(__name__)

class BacktestingEngine:
    def __init__(self, w3_mock=None):
        self.w3 = w3_mock
        # Load the strategies in simulated mode
        self.sandwich_strategy = SandwichStrategy(self.w3)
        self.liquidation_strategy = LiquidationStrategy(self.w3)
        
        self.results = []
        
    async def run_backtest(self, historical_txs: List[Dict[str, Any]]):
        """
        Feed a list of historical pending mempool transactions into the strategy logic
        to gauge their theoretical profitability without risking real capital.
        """
        logger.info(f"Starting backtest engine on {len(historical_txs)} historical records...")
        
        for idx, tx in enumerate(historical_txs):
            logger.debug(f"Processing TX {idx+1}/{len(historical_txs)}: {tx.get('hash')}")
            
            # --- Test Sandwich Logic ---
            is_sandwich = await self.sandwich_strategy.analyze_transaction(tx)
            if is_sandwich:
                # Mock a theoretical profit for backtest charting
                profit = 0.05 
                self.results.append({
                    "tx_hash": tx.get('hash', '').hex() if type(tx.get('hash')) == bytes else tx.get('hash'),
                    "strategy": "Sandwich",
                    "theoretical_profit_eth": profit
                })
                continue
                
            # --- Test Liquidation Logic ---
            is_liquidation = await self.liquidation_strategy.analyze_transaction(tx)
            if is_liquidation:
                profit = 0.20
                self.results.append({
                    "tx_hash": tx.get('hash', '').hex() if type(tx.get('hash')) == bytes else tx.get('hash'),
                    "strategy": "Liquidation",
                    "theoretical_profit_eth": profit
                })
                continue
                
        return self.generate_report()

    def generate_report(self) -> pd.DataFrame:
        """
        Compile the backtest results into a Pandas DataFrame for the UI.
        """
        if not self.results:
            logger.warning("No profitable trades found in backtest.")
            return pd.DataFrame()
            
        df = pd.DataFrame(self.results)
        total_profit = df['theoretical_profit_eth'].sum()
        
        logger.info("=== BACKTEST REPORT ===")
        logger.info(f"Total Trades Found: {len(df)}")
        logger.info(f"Total Theoretical Net Profit: {total_profit} ETH")
        
        return df

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    # Mock some historical Uniswap swap transactions
    mock_history = [
        {"hash": b"0xAAAA", "to": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "input": "0x7ff36ab5...", "value": 6*10**18},
        {"hash": b"0xBBBB", "to": "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9", "input": "0x", "value": 0},
        {"hash": b"0xCCCC", "to": "0xRandomAddress...", "input": "0x", "value": 0}
    ]
    
    engine = BacktestingEngine()
    asyncio.run(engine.run_backtest(mock_history))
