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
// single EOA controls everything
address constant ADMIN = 0x123...;
```

### Fixed
```solidity
// proxy admin = timelock multisig; logic owner = operations multisig
```

