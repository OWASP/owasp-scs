---
title: Rebase Token Balance Drift
id: SCWE-111
alias: rebase-token-drift
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMP]
  scsvs-scg: [SCSVS-COMP-1]
  cwe: [682]
status: new
---

## Relationships
- CWE-682: Incorrect Calculation  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
Rebasing tokens change user balances over time. Protocols that track deposited amounts as fixed units (instead of shares) can become insolvent or let users withdraw more than their fair share after positive or negative rebases.

## Remediation
- Track user positions using share-based accounting that scales with total supply.
- Normalize balances on every interaction or use wrappers that expose a non-rebasing interface (e.g., wstETH).
- Validate integrations against tokens with elastic supply and document unsupported assets.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Savings {
    IERC20 public rebasingToken;
    mapping(address => uint256) public deposits;

    function deposit(uint256 amount) external {
        rebasingToken.transferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] += amount; // assumes static balance
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Savings {
    IERC20 public rebasingToken;
    mapping(address => uint256) public shares;
    uint256 public totalShares;

    function deposit(uint256 amount) external {
        uint256 supply = rebasingToken.totalSupply();
        uint256 share = totalShares == 0 ? amount : amount * totalShares / supply;
        shares[msg.sender] += share;
        totalShares += share;
        rebasingToken.transferFrom(msg.sender, address(this), amount);
    }
}
```

