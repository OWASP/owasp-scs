---
title: Shared Proxy Admin and Logic Owner Key
id: SCWE-119
alias: shared-admin-logic-owner
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
Using the same key to control both the proxy admin (upgrade rights) and logic contract owner concentrates power. A single key compromise allows hostile upgrades and privileged function abuse with no separation of duties.

## Remediation
- Separate roles: proxy admin under multisig+timelock; logic owner under different multisig.
- Use role-based access (e.g., OZ AccessControl) and distinct keys for operational vs. upgrade actions.
- Document and monitor role boundaries; rotate keys periodically.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Proxy {
    address public admin; // same key for upgrades and logic owner
    address public implementation;

    modifier onlyAdmin() { require(msg.sender == admin, "not admin"); _; }

    function upgrade(address impl) external onlyAdmin { implementation = impl; }
    function setParam(uint256 x) external onlyAdmin { /* ... */ }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Proxy {
    address public proxyAdmin;   // timelock + multisig; upgrade rights only
    address public logicOwner;  // separate multisig; operational params only
    address public implementation;

    modifier onlyProxyAdmin() { require(msg.sender == proxyAdmin, "not proxy admin"); _; }
    modifier onlyLogicOwner() { require(msg.sender == logicOwner, "not logic owner"); _; }

    function upgrade(address impl) external onlyProxyAdmin { implementation = impl; }
    function setParam(uint256 x) external onlyLogicOwner { /* ... */ }
}
```

