---
title: Insecure Multicall Context Forwarding
id: SCWE-128
alias: insecure-multicall-context
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [841]
status: new
---

## Relationships
- CWE-841: Improper Enforcement of Behavioral Workflow  
  [https://cwe.mitre.org/data/definitions/841.html](https://cwe.mitre.org/data/definitions/841.html)

## Description
Multicall-style aggregators that forward calls without guarding against reentrancy or context changes let attackers reorder actions within one tx (e.g., deposit then withdraw) or impersonate `msg.sender` when inner calls use `tx.origin` or cached sender state.

## Remediation
- Apply reentrancy guards around multicall entrypoints.
- Avoid caching `msg.sender` across calls; pass explicit sender/context to internal functions.
- Restrict callable selectors/targets or enforce allowlists.

## Examples

### Vulnerable
```solidity
function multicall(bytes[] calldata data) external {
    for (uint i; i < data.length; i++) {
        (bool ok, ) = address(this).delegatecall(data[i]);
        require(ok, "fail");
    }
}
```

### Fixed
```solidity
function multicall(bytes[] calldata data) external nonReentrant {
    for (uint i; i < data.length; i++) {
        _dispatch(msg.sender, data[i]); // explicit context, no delegatecall loops
    }
}
```

