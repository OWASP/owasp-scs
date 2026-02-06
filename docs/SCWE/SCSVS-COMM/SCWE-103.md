---
title: ERC20 Approval Double-Spend (Allowance Race)
id: SCWE-103
alias: erc20-approval-race
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [362]
status: new
---

## Relationships
- CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization (Race Condition)  
  [https://cwe.mitre.org/data/definitions/362.html](https://cwe.mitre.org/data/definitions/362.html)

## Description
Changing an ERC20 allowance from value `X` to `Y` with a single `approve` call allows a spender to front-run and spend `X` before the change, then spend `Y` after, effectively double-spending. Integrations that do not use `increaseAllowance`/`decreaseAllowance` are exposed.

## Remediation
- Follow the allowance reset pattern: set allowance to `0`, then set the new value.
- Prefer `increaseAllowance`/`decreaseAllowance` or EIP-2612 `permit` with nonces.
- For critical flows, pull tokens via `transferFrom` after verifying allowance updates.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;
interface IERC20 { function approve(address,uint256) external returns (bool); }

contract DApp {
    IERC20 public token;

    function changeSpender(address spender, uint256 newAmount) external {
        token.approve(spender, newAmount); // can be front-run
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";

contract DApp {
    using SafeERC20 for IERC20;
    IERC20 public token;

    function changeSpender(address spender, uint256 newAmount) external {
        token.safeApprove(spender, 0);      // reset first; SafeERC20 handles non-standard tokens (e.g. USDT)
        token.safeApprove(spender, newAmount);
    }
}
```

