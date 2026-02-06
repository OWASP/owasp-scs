---
title: Unauthenticated Beacon Upgrade
id: SCWE-118
alias: unauthenticated-beacon-upgrade
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [306]
status: new
---

## Relationships
- CWE-306: Missing Authentication for Critical Function  
  [https://cwe.mitre.org/data/definitions/306.html](https://cwe.mitre.org/data/definitions/306.html)

## Description
Beacon proxies rely on a beacon address that determines implementation. If the beacon upgrade function lacks proper access control or timelock, an attacker can point all proxies to malicious code, taking over state and funds.

## Remediation
- Restrict beacon upgrades to multisig+timelock and emit events on change.
- Validate new implementation bytecode (e.g., initializer disabled, interfaces intact).
- Monitor beacon address changes on-chain with alerts.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Beacon {
    address public impl;
    function upgradeTo(address newImpl) external { // no auth
        impl = newImpl;
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Beacon {
    address public impl;
    address public admin;
    function upgradeTo(address newImpl) external {
        require(msg.sender == admin, "not admin");
        impl = newImpl;
    }
}
```

