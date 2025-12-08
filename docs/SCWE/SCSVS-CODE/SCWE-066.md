---
title: Incorrect Handling of Bitwise Operations  
id: SCWE-066  
alias: incorrect-bitwise-operations  
platform: []  
profiles: [L1]  
mappings:  
  scsvs-cg: [SCSVS-CODE]  
  scsvs-scg: [SCSVS-CODE-2]  
  cwe: [682]  
status: new  
---

## Relationships  
- **CWE-682: Incorrect Calculation**  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)  

## Description  
Bitwise operations (e.g., `&`, `|`, `^`, `<<`, `>>`) can be efficient alternatives to arithmetic operations but are prone to errors if not used correctly. Misusing bitwise shifts can cause unintended value changes, integer overflows, or precision loss. Solidity lacks native overflow checks for bitwise shifts, making incorrect handling particularly dangerous in financial calculations or cryptographic functions.

## Remediation  
- Ensure bitwise shifts do not exceed the size of the data type (e.g., shifting a `uint8` left by 8+ bits).  
- Validate input ranges before performing shifts to prevent overflow or precision loss.  
- Avoid unnecessary bitwise operations in financial calculations unless explicitly needed.  

### Vulnerable Contract Example  
```solidity
contract Example {
    function shiftLeft(uint8 input) public pure returns (uint8) {
        return input << 8;  // ❌ Shifting beyond `uint8` capacity leads to zero
    }

    function bitwiseAnd(uint8 a, uint8 b) public pure returns (uint8) {
        return a & b;  // ❌ Without proper validation, this could lead to unintended masking
    }
}
```
**Why is this vulnerable?**

- `input << 8` shifts a `uint8` completely out of range, resulting in a value of `0`.
- `a & b` can unintentionally mask critical bits if inputs are not properly validated.

### Fixed Contract Example

```solidity
contract SecureExample {
    function safeShiftLeft(uint8 input) public pure returns (uint8) {
        require(input < 32, "Shift too large");  // ✅ Validate shift range
        return input << 2;  // ✅ Safe shift within `uint8` bounds
    }

    function safeBitwiseAnd(uint8 a, uint8 b) public pure returns (uint8) {
        require(a > 0 && b > 0, "Invalid input");  // ✅ Ensure inputs are meaningful
        return a & b;
    }
}
```

**Why is this safe?**

- Restricts shift values to prevent unexpected overflows.
- Ensures bitwise operations do not unintentionally modify values in an unintended way.
- Protects contract logic from potential manipulation through poorly validated inputs.

**By correctly handling bitwise operations, developers can avoid unintended computation errors and ensure mathematical correctness in smart contracts.**