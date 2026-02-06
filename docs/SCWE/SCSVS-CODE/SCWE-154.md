---
title: Calldata Decode Without Length Check
id: SCWE-154
alias: missing-array-length-before-decode
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Decoding calldata or bytes with `abi.decode` without first verifying the input length can cause unexpected reverts. In modern Solidity (0.4.22+), `abi.decode` with data shorter than expected reverts due to bounds checking; malformed or incorrectly typed data can produce wrong values. SCWE-122 covers calldata length validation; this weakness addresses the broader pattern of decoding without length checks.

## Remediation
- Validate `data.length >= expectedLength` before `abi.decode`.
- Use `abi.decode` with the correct type and ensure the encoded data matches.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Decoder {
    function decodeAndUse(bytes calldata data) external {
        (address recipient, uint256 amount) = abi.decode(data, (address, uint256));
        // If data is too short, decode reverts; malformed data can produce wrong values
        transfer(recipient, amount);
    }
}
```

### Fixed
```solidity
function decodeAndUse(bytes calldata data) external {
    require(data.length >= 32 + 32, "Invalid data length");
    (address recipient, uint256 amount) = abi.decode(data, (address, uint256));
    transfer(recipient, amount);
}
```
