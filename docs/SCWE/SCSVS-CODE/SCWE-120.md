---
title: Missing Return Data Length Validation
id: SCWE-120
alias: missing-returndata-length-check
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [697]
status: new
---

## Relationships
- CWE-697: Incorrect Comparison  
  [https://cwe.mitre.org/data/definitions/697.html](https://cwe.mitre.org/data/definitions/697.html)

## Description
Low-level calls that decode return values without checking `returndatasize` can read zeroed or truncated data. Attackers can craft contracts that return short payloads so callers mis-interpret success flags, prices, or balances.

## Remediation
- Verify `returndatasize` matches expected length before decoding.
- Prefer high-level interfaces that perform ABI decoding checks.
- Revert on unexpected return sizes and log anomalies.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

(bool ok, bytes memory data) = token.staticcall(abi.encodeWithSignature("balanceOf(address)", user));
uint256 bal = abi.decode(data, (uint256)); // assumes length >= 32
```

### Fixed
```solidity
pragma solidity ^0.8.0;

(bool ok, bytes memory data) = token.staticcall(abi.encodeWithSignature("balanceOf(address)", user));
require(ok && data.length == 32, "bad returndata");
uint256 bal = abi.decode(data, (uint256));
```

