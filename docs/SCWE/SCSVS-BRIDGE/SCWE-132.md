---
title: Mismatched Token Decimals in Bridge Mint/Burn
id: SCWE-132
alias: bridge-decimal-mismatch
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-1]
  cwe: [682]
status: new
---

## Relationships
- CWE-682: Incorrect Calculation  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
Bridging tokens with differing decimals without normalization can over- or under-mint wrapped assets. Attackers can exploit decimal confusion to siphon value or lock funds when withdrawing back to the origin chain.

## Remediation
- Normalize amounts to a canonical precision before mint/burn.
- Store per-token decimal config and validate consistency during bridge operations.
- Add tests for round-trip conversions across chains with varying decimals.

## Examples

### Vulnerable
```solidity
// assumes 18 decimals on both sides; origin token has 6
_mint(user, amount);
```

### Fixed
```solidity
uint8 srcDec = 6;
uint8 dstDec = 18;
uint256 normalized = amount * 10**(dstDec - srcDec);
_mint(user, normalized);
```

