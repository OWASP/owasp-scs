---
title: EIP-1559 Basefee Assumptions
id: SCWE-127
alias: basefee-assumptions
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BLOCK]
  scsvs-scg: [SCSVS-BLOCK-2]
  cwe: [841]
status: new
---

## Relationships
- CWE-841: Improper Enforcement of Behavioral Workflow  
  [https://cwe.mitre.org/data/definitions/841.html](https://cwe.mitre.org/data/definitions/841.html)

## Description
Hardcoding gas price/basefee assumptions (e.g., fixed `gasprice` limits or expecting refunds) can break on EIP-1559 chains. Contracts that require exact `block.basefee` ranges or reimburse fixed gas can become stuck or exploitable via gas griefing.

## Remediation
- Avoid relying on specific basefee values; parameterize and allow updates via governance with delays.
- Use robust gas estimation and caps on external calls; avoid refund-dependent logic.
- Simulate on mainnet forks with varying basefee to validate liveness.

## Examples

### Vulnerable
```solidity
require(tx.gasprice <= 30 gwei, "gas too high"); // fails as basefee rises
```

### Fixed
```solidity
uint256 maxGasPrice = governanceMaxGasPrice;
require(tx.gasprice <= maxGasPrice, "gas too high"); // upgradable with delays
```

