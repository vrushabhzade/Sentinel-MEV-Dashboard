// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IUniswapV2Router {
    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);
    
    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        returns (uint[] memory amounts);
}

contract SandwichBot {
    address public immutable owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not Authorized");
        _;
    }

    receive() external payable {}

    // Bundle Step 1: Frontrun the victim by buying the token and driving the price up.
    function frontrunBuy(
        address router,
        address tokenOut,
        uint256 amountOutMin
    ) external payable onlyOwner {
        address[] memory path = new address[](2);
        path[0] = getWETH();
        path[1] = tokenOut;

        IUniswapV2Router(router).swapExactETHForTokens{value: msg.value}(
            amountOutMin,
            path,
            address(this),
            block.timestamp + 120
        );
    }

    // Bundle Step 3: Backrun the victim by dumping the token at the artificially inflated price.
    function backrunSell(
        address router,
        address tokenIn,
        uint256 amountOutMin,
        uint256 minerBribe
    ) external onlyOwner {
        uint256 balance = IERC20(tokenIn).balanceOf(address(this));
        
        // Approve router to sell tokens
        IERC20(tokenIn).approve(router, balance);

        address[] memory path = new address[](2);
        path[0] = tokenIn;
        path[1] = getWETH();

        IUniswapV2Router(router).swapExactTokensForETH(
            balance,
            amountOutMin,
            path,
            address(this), // Profit stays in the contract
            block.timestamp + 120
        );
        
        // Bribe the miner via block.coinbase to incentivize inclusion of the bundle
        if (minerBribe > 0) {
            block.coinbase.transfer(minerBribe);
        }
    }

    // Emergency withdraw or normal profit withdrawal
    function withdraw(address token) external onlyOwner {
        if (token == address(0)) {
            payable(owner).transfer(address(this).balance);
        } else {
            uint256 bal = IERC20(token).balanceOf(address(this));
            IERC20(token).transfer(owner, bal);
        }
    }

    function getWETH() internal pure returns (address) {
        // Mainnet WETH Address
        return 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    }
}
