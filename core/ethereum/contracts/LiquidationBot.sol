// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Mock Interfaces for Lending Protocols & DEXes
interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IAaveLendingPool {
    function liquidationCall(
        address collateralAsset,
        address debtAsset,
        address user,
        uint256 debtToCover,
        bool receiveAToken
    ) external;
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

// Flashloan Provider Interface (e.g. Aave or Balancer)
interface IFlashLoanProvider {
    function flashLoan(
        address receiverAddress,
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata modes,
        address onBehalfOf,
        bytes calldata params,
        uint16 referralCode
    ) external;
}

contract LiquidationBot {
    address public immutable owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not Authorized");
        _;
    }

    // 1. Entry Point: Request a Flashloan
    function executeFlashLiquidation(
        address flashProvider,
        address lendingPool,
        address debtAsset, // Asset to borrow via flashloan to repay the victim's debt
        address collateralAsset, // Asset we get as a reward
        address victim,
        uint256 debtToCover
    ) external onlyOwner {
        address[] memory assets = new address[](1);
        assets[0] = debtAsset;
        
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = debtToCover;
        
        uint256[] memory modes = new uint256[](1);
        modes[0] = 0; // 0 = no debt, purely flashloan
        
        // Encode parameters to pass context to the callback
        bytes memory params = abi.encode(lendingPool, collateralAsset, victim);
        
        // Take Flashloan
        IFlashLoanProvider(flashProvider).flashLoan(
            address(this),
            assets,
            amounts,
            modes,
            address(this),
            params,
            0
        );
    }

    // 2. Callback from Flashloan Provider (Must exactly match provider signature)
    function executeOperation(
        address[] calldata assets,
        uint256[] calldata amounts,
        uint256[] calldata premiums,
        address initiator,
        bytes calldata params
    ) external returns (bool) {
        // Decode context
        (address lendingPool, address collateralAsset, address victim) = abi.decode(params, (address, address, address));
        
        address debtAsset = assets[0];
        uint256 flashloanDebt = amounts[0] + premiums[0];
        
        // Approve LendingPool to take our flash-borrowed asset
        IERC20(debtAsset).approve(lendingPool, amounts[0]);
        
        // Trigger Liquidation
        IAaveLendingPool(lendingPool).liquidationCall(
            collateralAsset,
            debtAsset,
            victim,
            amounts[0],
            false // Receive underlying asset, not aTokens
        );
        
        // Now we hold the collateral asset + liquidation bonus!
        // We must swap the collateral back to the `debtAsset` to repay the flashloan.
        // E.g. using Uniswap or SushiSwap (Mocked here as an external call for simplicity)
        // __swapCollateralForDebt(collateralAsset, debtAsset);
        
        // Ensure we have enough debtAsset to repay the flashloan
        require(IERC20(debtAsset).balanceOf(address(this)) >= flashloanDebt, "Flashloan Repayment Failed");
        
        // Approve Flashloan Provider to take back the principal + fee
        IERC20(debtAsset).approve(msg.sender, flashloanDebt);
        
        return true;
    }

    function withdraw(address token) external onlyOwner {
        if (token == address(0)) {
            payable(owner).transfer(address(this).balance);
        } else {
            uint256 bal = IERC20(token).balanceOf(address(this));
            IERC20(token).transfer(owner, bal);
        }
    }
}
