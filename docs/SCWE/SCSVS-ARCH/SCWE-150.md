---
title: Storage Slot Collision When Upgrading Implementation
id: SCWE-150
alias: storage-layout-cross-contract-upgrade
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-2]
  cwe: [682]
status: new
---

## Relationships
- CWE-682: Incorrect Calculation  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
When upgrading a proxy's implementation, the new implementation's storage layout must be compatible with the proxy's storage. Appending variables in the implementation without accounting for the proxy's own storage (e.g., admin, implementation address) can cause slot collisions. Similarly, inherited contracts that add state variables can overwrite slots used by the base or proxy. SCWE-099 covers same-contract layout; this addresses cross-contract layout (proxy + implementation, inheritance chain).

## Remediation
- Use a single storage contract or follow a consistent storage layout convention (e.g., EIP-1967).
- Reserve gaps (`uint256[50] private __gap`) in base contracts for future expansion.
- Run storage layout diff tools before upgrading.

## Examples

### Vulnerable
```solidity
// Proxy
contract Proxy {
    address public implementation;  // slot 0
    address public admin;           // slot 1
}

// Implementation V2 - assumes it "owns" slots from 0
contract ImplV2 {
    address public owner;      // slot 0 - COLLIDES with proxy's implementation
    uint256 public newValue;   // slot 1 - COLLIDES with proxy's admin
}
```

### Fixed
```solidity
contract ImplV2 {
    // Storage in implementation must not overlap proxy slots
    // Use EIP-1967 or append after reserved slots
    bytes32 private constant IMPLEMENTATION_SLOT = 0x360894...;
    // Implementation state starts after proxy slots
    uint256 public newValue;
}
```
