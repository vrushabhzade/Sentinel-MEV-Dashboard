from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def analyze_transaction(self, tx: dict) -> bool:
        """
        Analyze a pending transaction.
        Returns True if an opportunity is found.
        """
        pass

    @abstractmethod
    async def execute_trade(self, opportunity_data: dict) -> bool:
        """
        Execute the MEV trade.
        """
        pass
