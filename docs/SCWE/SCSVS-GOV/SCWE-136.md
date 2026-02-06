---
title: Unbounded Proposal Execution Gas
id: SCWE-136
alias: unbounded-governance-execution-gas
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [400]
status: new
---

## Relationships
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)

## Description
Governance proposals that execute arbitrary call lists without gas limits or batching can exceed block gas, making proposals unexecutable (DoS). Attackers can submit proposals with expensive calls to jam governance or brick queued actions.

## Remediation
- Enforce per-call and total gas limits; split proposals into bounded batches.
- Allow graceful skipping of failed subcalls with clear status, or pre-validate gas cost.
- Add simulation checks before queuing and block proposals that exceed safe gas budgets.

## Examples

### Vulnerable
```solidity
function execute(bytes[] calldata calls) external {
    for (uint i; i < calls.length; i++) {
        target.call(calls[i]); // no gas limit
    }
}
```

### Fixed
```solidity
function execute(bytes[] calldata calls, uint256 gasPerCall) external {
    for (uint i; i < calls.length; i++) {
        (bool ok,) = target.call{gas: gasPerCall}(calls[i]);
        require(ok, "subcall failed");
    }
}
```

