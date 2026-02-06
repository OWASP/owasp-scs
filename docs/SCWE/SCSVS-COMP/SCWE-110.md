---
title: Fee-On-Transfer Token Misaccounting
id: SCWE-110
alias: fee-on-transfer-misaccounting
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
Assuming an ERC20 transfer moves the full requested amount fails with fee-on-transfer or deflationary tokens. Protocols that credit users for the requested amount instead of the received amount can be drained or mis-account balances.

## Remediation
- Measure token balances before and after transfers to calculate the actual received amount.
- Maintain allowlists/blocks for incompatible tokens or handle fee-on-transfer explicitly.
- Validate that accounting uses the net amount when updating shares or debts.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Vault {
    IERC20 public token;
    mapping(address => uint256) public deposits;

    function deposit(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        deposits[msg.sender] += amount; // credits full amount even if fee applied
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Vault {
    IERC20 public token;
    mapping(address => uint256) public deposits;

    function deposit(uint256 amount) external {
        uint256 beforeBal = token.balanceOf(address(this));
        token.transferFrom(msg.sender, address(this), amount);
        uint256 received = token.balanceOf(address(this)) - beforeBal;
        deposits[msg.sender] += received; // credit net amount
    }
}
```

