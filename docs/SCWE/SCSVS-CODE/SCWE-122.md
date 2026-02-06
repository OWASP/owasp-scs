---
title: Calldata Length Not Validated Before Decode
id: SCWE-122
alias: missing-calldata-length-check
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Functions that `abi.decode` calldata without first checking expected length can revert unpredictably or read malformed inputs. Attackers can craft short calldata to trigger reverts that lock functionality or bypass logic that runs before decode.

## Remediation
- Validate `msg.data.length` against expected sizes (including selector).
- Prefer Solidity typed arguments but still guard against undersized calldata on low-level entrypoints.
- Reject unexpected trailing data when strict parsing is required.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

function execute(bytes calldata data) external {
    (address to, uint256 amount) = abi.decode(data, (address, uint256));
    // ...
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

function execute(bytes calldata data) external {
    require(data.length == 64, "bad length"); // selector handled elsewhere
    (address to, uint256 amount) = abi.decode(data, (address, uint256));
}
```

