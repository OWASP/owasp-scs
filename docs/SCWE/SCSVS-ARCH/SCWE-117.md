---
title: Proxy Implementation Selfdestruct Exposure
id: SCWE-117
alias: proxy-implementation-selfdestruct
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [284]
status: new
---

## Relationships
- CWE-284: Improper Access Control  
  [https://cwe.mitre.org/data/definitions/284.html](https://cwe.mitre.org/data/definitions/284.html)

## Description
If the proxy’s implementation contract exposes `selfdestruct` (or `SELFDESTRUCT` reachable through a function), an attacker or careless admin can destroy the implementation. The proxy then points to a non-existent code address, bricking upgrades or locking funds.

## Remediation
- Remove or disable `selfdestruct` in implementations; use `disableInitializers()` patterns.
- Gate any destruct-like functionality behind timelock + multisig and migration plans.
- Monitor implementation addresses and block upgrades that reduce code size to zero.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Impl {
    function kill() external {
        selfdestruct(payable(msg.sender));
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Impl {
    // no selfdestruct path; migrations use new proxy with state copy
}
```

