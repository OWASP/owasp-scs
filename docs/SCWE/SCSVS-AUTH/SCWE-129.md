---
title: Single EOA Admin Without Rotation
id: SCWE-129
alias: single-admin-eoa
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [284]
status: new
---

## Relationships
- CWE-284: Improper Access Control  
  [https://cwe.mitre.org/data/definitions/284.html](https://cwe.mitre.org/data/definitions/284.html)

## Description
Relying on a single externally owned account (EOA) as contract admin creates a single point of failure. Key compromise, loss, or coercion can lead to irreversible upgrades, pauses, or fund drains with no recovery.

## Remediation
- Use multisig (>=2-of-3) with hardware keys and timelocks for admin roles.
- Document and test key rotation and recovery procedures.
- Limit admin powers by role (upgrade vs. ops) and enforce separation of duties.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Gov {
    address public admin; // single EOA — key loss or compromise = no recovery

    modifier onlyAdmin() { require(msg.sender == admin, "not admin"); _; }
    function upgrade(address impl) external onlyAdmin { /* ... */ }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Gov {
    IMultisig public admin;     // 2-of-3 multisig with hardware keys
    ITimelock public timelock;  // 48h delay for upgrades

    function proposeUpgrade(address impl) external {
        require(admin.isOwner(msg.sender), "not owner");
        timelock.schedule(impl);
    }
    function executeUpgrade() external {
        timelock.execute(); // only after delay; supports key rotation
    }
}
```

