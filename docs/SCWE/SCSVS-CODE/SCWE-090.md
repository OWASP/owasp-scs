---
title: Missing Slippage Protection in Automated Token Swaps
id: SCWE-090
alias: Missing-Slippage-Protection-in-Automated-Token-Swaps
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20:  Improper Input Validation 
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
This weakness occurs when smart contracts execute token swaps through DEX routers (e.g., Uniswap, PancakeSwap, SushiSwap) with the amountOutMin parameter set to 0 or a hardcoded static value. This disables slippage protection and allows trades to execute regardless of adverse price movement. As a result, users or protocols may receive significantly fewer tokens than expected, especially under high volatility, front-running, or sandwich attack conditions.

## Remediation  
- Always validate amountOutMin based on live price quotes (e.g., using on-chain oracles or pre-trade estimates).
- Allow users to configure slippage tolerance (0.5%, 1%, etc.), and enforce it in contract logic.
- Never hardcode 0 or static values for amountOutMin.

## Examples  
- **Vulnerable Code (Missing Slippage Protection)**  
```solidity
function swapTokens(address tokenIn, address tokenOut, uint256 amountIn) external {
    IERC20(tokenIn).approve(address(uniswapRouter), amountIn);

    address ;
    path[0] = tokenIn;
    path[1] = tokenOut;

    // ❌ amountOutMin is set to 0 → no protection against slippage
    uniswapRouter.swapExactTokensForTokens(
        amountIn,
        0, // Vulnerable: accepts any output amount
        path,
        msg.sender,
        block.timestamp
    );
} 
```

- **Safe Code (With Slippage Protection)**
```solidity
function swapTokensWithSlippage(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 minAmountOut
) external {
    IERC20(tokenIn).approve(address(uniswapRouter), amountIn);

    address ;
    path[0] = tokenIn;
    path[1] = tokenOut;

    // ✅ Enforces user-provided slippage tolerance
    uniswapRouter.swapExactTokensForTokens(
        amountIn,
        minAmountOut, // Safe: requires a minimum output
        path,
        msg.sender,
        block.timestamp
    );
}
```
