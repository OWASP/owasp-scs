---
title: Add/Remove Liquidity Without Minimum Output Validation
id: SCWE-151
alias: missing-slippage-protection-liquidity-operations
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-2]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Adding or removing liquidity in AMMs (e.g., Uniswap, Curve) without enforcing a minimum amount of LP tokens or underlying assets received can expose users to sandwich attacks or unfavorable execution. Similar to swap slippage (SCWE-090), LP operations can be front-run: an attacker manipulates the pool before the user's add/remove, then reverses after. Without `amountMin` or equivalent checks, users may receive far less than expected.

## Remediation
- Accept `amountMin` (or `minLPTokens`, `minAmounts`) from users and enforce it when adding/removing liquidity.
- Use deadline parameters (SCWE-141) in addition to slippage protection.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

interface IUniswapV2Router {
    function addLiquidity(address tokenA, address tokenB, uint256 amountADesired, uint256 amountBDesired, uint256 amountAMin, uint256 amountBMin, address to, uint256 deadline) external returns (uint256 amountA, uint256 amountB, uint256 liquidity);
}

contract LiquidityManager {
    function addLiquidity(address tokenA, address tokenB, uint256 amountA, uint256 amountB) external {
        IUniswapV2Router(router).addLiquidity(
            tokenA, tokenB,
            amountA, amountB,
            0, 0,  // amountAMin, amountBMin = 0: no slippage protection
            msg.sender,
            block.timestamp
        );
    }
}
```

### Fixed
```solidity
function addLiquidity(address tokenA, address tokenB, uint256 amountA, uint256 amountB, uint256 amountAMin, uint256 amountBMin, uint256 deadline) external {
    require(block.timestamp <= deadline, "Expired");
    IUniswapV2Router(router).addLiquidity(tokenA, tokenB, amountA, amountB, amountAMin, amountBMin, msg.sender, deadline);
}
```
