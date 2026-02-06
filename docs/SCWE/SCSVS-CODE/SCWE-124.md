---
title: Inconsistent Rounding Direction in Financial Math
id: SCWE-124
alias: inconsistent-rounding
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [682]
status: new
---

## Relationships
- CWE-682: Incorrect Calculation  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
Using mixed rounding strategies (floor vs. ceil vs. truncation) across mint/burn/withdraw logic causes value drift. Attackers can cycle operations to accumulate dust gains or trigger unfair liquidations due to asymmetry.

## Remediation
- Define and document a single rounding direction per invariant (e.g., always round in favor of the protocol or user).
- Centralize math helpers and reuse them across all financial paths.
- Add property-based tests to ensure invariant preservation under rounding.

## Examples

### Vulnerable
```solidity
shares = amount * totalShares / totalAssets;      // truncates
assets = shares * totalAssets / totalShares + 1;  // rounds up
```

### Fixed
```solidity
// consistently round down (or up) and state it explicitly
shares = amount * totalShares / totalAssets;
assets = shares * totalAssets / totalShares;
```

