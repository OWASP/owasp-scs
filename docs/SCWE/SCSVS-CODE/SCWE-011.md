---
title: Insecure ABI Encoding and Decoding
id: SCWE-011
alias: insecure-abi-encoding-decoding
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-3]
  cwe: [937]
status: new
---

## Relationships
- CWE-116: Improper Encoding or Escaping of Output 
  [https://cwe.mitre.org/data/definitions/116.html](https://cwe.mitre.org/data/definitions/116.html)

## Description
Insecure ABI encoding and decoding occur when a smart contract improperly handles data serialization and deserialization, leading to vulnerabilities such as data corruption, type confusion, or reentrancy attacks. Solidity provides ABI encoding functions like `abi.encode()`, `abi.encodePacked()`, and `abi.decode()`, but improper usage can cause unexpected behavior.

Common issues with insecure ABI handling:
- **Collision Risks in `abi.encodePacked()`**: Multiple concatenated parameters can lead to ambiguous encoding, making it vulnerable to hash collisions.
- **Unchecked Decoding**: Improper use of `abi.decode()` can result in unintended memory corruption or type confusion.
- **Lack of Input Validation**: Encoding user inputs without verification can introduce security flaws.
- **Mismatched Data Types**: Decoding an incorrectly encoded data structure can lead to invalid memory access.

## Remediation
- **Use `abi.encode()` Instead of `abi.encodePacked()` for Hashing**: Prevent collision risks by ensuring unique encoding.
- **Validate Data Before Decoding**: Ensure the encoded data conforms to the expected structure before decoding.
- **Match Encoding and Decoding Types**: Always use the correct type structure when decoding to avoid unintended behavior.
- **Avoid Direct ABI Decoding of External Calls**: Use strict validation mechanisms when handling data from external contracts.

## Examples

### Example of Insecure ABI Encoding:

```solidity
pragma solidity ^0.8.0;

contract InsecureABI {
    function hashValues(string memory str, uint256 num) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(str, num)); // ❌ Collision risk
    }
}
```

- In this example, `abi.encodePacked()` creates a collision risk because different input combinations can produce the same hash.

### Refactored to Secure ABI Encoding:

```solidity
pragma solidity ^0.8.0;

contract SecureABI {
    function hashValues(string memory str, uint256 num) public pure returns (bytes32) {
        return keccak256(abi.encode(str, num)); // ✅ Unique encoding, no collision
    }
}
```

- In this improved version, `abi.encode()` ensures a unique encoding structure, preventing hash collision attacks.
