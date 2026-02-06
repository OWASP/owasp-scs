---
title: Swallowed Revert Reasons
id: SCWE-121
alias: swallowed-revert-reasons
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [388]
status: new
---

## Relationships
- CWE-388: Error Handling  
  [https://cwe.mitre.org/data/definitions/388.html](https://cwe.mitre.org/data/definitions/388.html)

## Description
Ignoring revert data (e.g., using `require(ok)` without bubbling reason) hides the root cause of failures. Protocols may proceed under incorrect assumptions, misprice risk, or block user funds without actionable errors.

## Remediation
- Bubble revert reasons from external calls (`(bool ok, bytes memory data)`, then `assembly { revert(add(data,32), mload(data)) }` when `!ok`).
- Standardize error handling with custom errors and propagate upstream.
- Emit diagnostics when external calls fail to aid monitoring.

## Examples

### Vulnerable
```solidity
(bool ok, ) = target.call(payload);
require(ok, "call failed"); // hides real reason
```

### Fixed
```solidity
(bool ok, bytes memory data) = target.call(payload);
if (!ok) {
    assembly {
        revert(add(data, 32), mload(data))
    }
}
```

