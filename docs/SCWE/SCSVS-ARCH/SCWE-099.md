---
title: Storage Layout Collision on Upgrade
id: SCWE-099
alias: storage-layout-collision
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [664]
status: new
---

## Relationships
- CWE-664: Improper Control of a Resource Through its Lifetime  
  [https://cwe.mitre.org/data/definitions/664.html](https://cwe.mitre.org/data/definitions/664.html)

## Description
Upgradeable contracts rely on stable storage slots. Reordering, removing, or inserting state variables (or changing inheritance order) between versions causes storage collisions when the proxy reuses the same slots, corrupting balances, roles, or configuration.

## Remediation
- Freeze variable ordering; only append new variables.
- Reserve gaps (`uint256[50] private __gap;`) to allow future expansion.
- Use automated storage layout diffing and follow upgrade-safe patterns (e.g., OZ Upgradeable tooling).

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract V1 {
    address public owner;   // slot 0
    uint256 public balance; // slot 1
}

contract V2 is V1 {
    uint256 public balance; // reuses slot 1, corrupts state
    address public treasury;
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract V1 {
    address public owner;   // slot 0
    uint256 public balance; // slot 1
    uint256[48] private __gap;
}

contract V2 is V1 {
    uint256 public treasuryFee; // slot 2 (after gap)
}
```

