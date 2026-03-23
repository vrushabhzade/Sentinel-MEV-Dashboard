// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IUniswapV2Router {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
}

contract ArbitrageBot {
    address public immutable owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not Authorized");
        _;
    }

    // Example Cross-DEX Arbitrage: WETH -> Token A (DEX 1) -> Token A -> WETH (DEX 2)
    function executeArbitrage(
        address router1, // e.g. Uniswap V2
        address router2, // e.g. SushiSwap
        address token0,  // Base Token (WETH)
        address token1,  // Arbitrage Target Token
        uint256 amountIn,
        uint256 minProfit,
        uint256 minerBribe
    ) external onlyOwner {
        
        // 1. Snapshot our starting ETH/WETH balance to calculate final profit
        uint256 initialBalance = IERC20(token0).balanceOf(address(this));
        
        // Approve first DEX Router
        IERC20(token0).approve(router1, amountIn);

        // Path for Trade 1: Token0 -> Token1
        address[] memory path1 = new address[](2);
        path1[0] = token0;
        path1[1] = token1;

        // Execute Trade 1 on DEX 1
        uint256[] memory amounts1 = IUniswapV2Router(router1).swapExactTokensForTokens(
            amountIn,
            0, // We do not enforce min output here; we check final net profit at the end!
            path1,
            address(this),
            block.timestamp + 120
        );
        
        uint256 token1Received = amounts1[1];
        
        // Path for Trade 2: Token1 -> Token0
        address[] memory path2 = new address[](2);
        path2[0] = token1;
        path2[1] = token0;

        // Approve second DEX Router
        IERC20(token1).approve(router2, token1Received);

        // Execute Trade 2 on DEX 2
        IUniswapV2Router(router2).swapExactTokensForTokens(
            token1Received,
            0,
            path2,
            address(this),
            block.timestamp + 120
        );

        // 2. Mathematically verify profitability
        uint256 finalBalance = IERC20(token0).balanceOf(address(this));
        
        // If we lost money, this require statement will trigger and REVERT the entire transaction.
        // Because we use Flashbots, a reverted transaction costs 0 gas! It simply drops from the block.
        require(finalBalance > initialBalance, "Arbitrage resulted in a net loss");
        
        uint256 profit = finalBalance - initialBalance;
        require(profit >= minProfit, "Arbitrage not profitable enough! Reverting.");

        // Bribe block builder / validator directly from smart contract to guarantee execution
        if (minerBribe > 0) {
            block.coinbase.transfer(minerBribe);
        }
    }
    
    // Accept ETH
    receive() external payable {}
    
    // Emergency withdraw or pull operational profits
    function withdraw(address token) external onlyOwner {
        if (token == address(0)) {
            payable(owner).transfer(address(this).balance);
        } else {
            uint256 bal = IERC20(token).balanceOf(address(this));
            IERC20(token).transfer(owner, bal);
        }
    }
}
