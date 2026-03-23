import pytest
import asyncio
from unittest.mock import MagicMock
from core.strategies.sandwich_strategy import SandwichStrategy

@pytest.fixture
def mock_w3():
    # Mocking Web3 so we don't need real node connection for unit testing
    mock = MagicMock()
    return mock

@pytest.mark.asyncio
async def test_sandwich_analyze_ignores_empty_to_address(mock_w3):
    strategy = SandwichStrategy(w3=mock_w3)
    tx = {"hash": b"123", "value": 10} # Missing 'to'
    
    result = await strategy.analyze_transaction(tx)
    assert result is False

@pytest.mark.asyncio
async def test_sandwich_analyze_matches_target_router(mock_w3):
    strategy = SandwichStrategy(w3=mock_w3)
    
    # Mock a target router address
    target_router = strategy.target_routers[0]
    
    # Mock transaction matching the signature for swapExactETHForTokens
    tx = {
        "hash": b"0xabcdef",
        "to": target_router,
        "input": "0x7ff36ab500000000000000000", # Mocked swap signature
        "value": 6 * 10**18 # 6 ETH (above the 5 ETH mockup threshold)
    }
    
    # Mocking w3.from_wei return for 6 ETH validation logic
    mock_w3.from_wei.return_value = 6
    
    result = await strategy.analyze_transaction(tx)
    assert result is True
