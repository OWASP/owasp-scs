---
title: Incorrect Type Conversion  
id: SCWE-080  
alias: incorrect-type-conversion  
platform: []  
profiles: [L1]  
mappings:  
  scsvs-cg: [SCSVS-ARCH]  
  scsvs-scg: [SCSVS-ARCH-2]  
  cwe: [704]  
status: new  
---

## Relationships  
- **CWE-704: Incorrect Type Conversion or Cast**  
  [https://cwe.mitre.org/data/definitions/704.html](https://cwe.mitre.org/data/definitions/704.html)  

## Description  
Incorrect type conversion occurs when a value is cast or implicitly converted between incompatible types, potentially leading to precision loss, unexpected behavior, or security vulnerabilities. Solidity allows certain implicit conversions (e.g., from `uint256` to `uint8`), which can lead to silent truncation of data. Additionally, casting between types like `address` and `uint` can lead to unexpected security risks.

## Remediation  
- Avoid unsafe downcasts from larger to smaller types unless explicitly required.  
- Always validate the range before converting between numerical types.  
- Use explicit conversion functions where applicable, ensuring proper handling of edge cases.  

### Vulnerable Contract Example  
```solidity
contract Example {
    function unsafeDowncast(uint256 value) public pure returns (uint8) {
        return uint8(value);  // ❌ Truncates value if > 255
    }

    function unsafeAddressToUint(address addr) public pure returns (uint256) {
        return uint256(uint160(addr));  // ❌ May lead to unexpected behaviors
    }
}
```
**Why is this vulnerable?**

- `uint8(value)` will silently truncate values above 255, leading to unintended loss of data.
- `uint256(uint160(addr))` might be used incorrectly in arithmetic operations, potentially allowing address manipulation.

### Fixed Contract Example

```solidity
contract SecureExample {
    function safeDowncast(uint256 value) public pure returns (uint8) {
        require(value <= type(uint8).max, "Value exceeds uint8 range");  // ✅ Ensure valid range
        return uint8(value);
    }

    function safeAddressToUint(address addr) public pure returns (uint160) {
        return uint160(addr);  // ✅ Restrict conversion to valid 160-bit range
    }
}
```
**Why is this safe?**

- Ensures that values do not exceed the allowed range before downcasting.
- Re- stricts type conversion to avoid security risks from improper arithmetic operations.
- Prevents silent data loss that could lead to unintended contract behavior.

**By enforcing safe type conversions, developers can ensure contract logic remains reliable and free from unexpected truncation issues.**