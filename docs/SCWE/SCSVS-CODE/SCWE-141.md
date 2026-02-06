---
title: Lack of Deadline Validation in Time-Sensitive External Calls
id: SCWE-141
alias: missing-deadline-external-calls
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Time-sensitive external calls (e.g., DEX swaps, limit orders) that use only `block.timestamp` as a deadline—or no user-supplied deadline—can be front-run or executed at unfavorable times. A user signs a transaction expecting execution within a short window, but miners/validators can delay inclusion. Without a `deadline` parameter, the transaction may execute when prices have moved adversely. SCWE-090 covers slippage; this weakness addresses the absence of explicit deadline validation.

## Remediation
- Accept a `deadline` parameter from users and enforce `require(block.timestamp <= deadline, "Expired")` before executing time-sensitive logic.
- Never rely solely on `block.timestamp` for user-intended time bounds without a user-supplied deadline.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

interface IRouter {
    function swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline) external returns (uint256[] memory);
}

contract Swapper {
    IRouter public router;

    function swap(address[] calldata path, uint256 amountIn, uint256 minOut) external {
        router.swapExactTokensForTokens(
            amountIn,
            minOut,
            path,
            msg.sender,
            block.timestamp  // No user deadline: tx can be delayed and executed at bad time
        );
    }
}
```

### Fixed
```solidity
function swap(address[] calldata path, uint256 amountIn, uint256 minOut, uint256 deadline) external {
    require(block.timestamp <= deadline, "Expired");
    router.swapExactTokensForTokens(amountIn, minOut, path, msg.sender, deadline);
}
```
