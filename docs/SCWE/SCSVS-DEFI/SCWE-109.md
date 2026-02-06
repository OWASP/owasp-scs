---
title: Unbounded Loops on Untrusted Input
id: SCWE-109
alias: unbounded-loops
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-1]
  cwe: [834]
status: new
---

## Relationships
- CWE-834: Excessive Iteration  
  [https://cwe.mitre.org/data/definitions/834.html](https://cwe.mitre.org/data/definitions/834.html)

## Description
Iterating over user-controlled arrays or mappings without bounds lets attackers submit large inputs that exhaust gas, causing denial of service. Functions like batch withdrawals, reward distribution, or liquidations may become permanently unusable.

## Remediation
- Impose upper bounds on loop iterations or batch sizes.
- Use pagination/iterative processing with checkpoints.
- Avoid on-chain iteration over untrusted lists; rely on off-chain aggregation with verifiable proofs (Merkle leaves).

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Distributor {
    function airdrop(address[] calldata users) external {
        for (uint256 i = 0; i < users.length; i++) {
            payable(users[i]).transfer(1 ether); // can run out of gas
        }
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Distributor {
    uint256 public last;

    function airdrop(address[] calldata users, uint256 max) external {
        uint256 end = last + max;
        if (end > users.length) end = users.length;
        for (uint256 i = last; i < end; i++) {
            payable(users[i]).transfer(1 ether);
        }
        last = end;
    }
}
```

