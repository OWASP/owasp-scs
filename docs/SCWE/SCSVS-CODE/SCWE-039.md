---
title: Insecure Use of Inline Assembly
id: SCWE-039
alias: insecure-use-of-inline-assembly
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [704]
status: new
---

## Relationships
- CWE-704: Incorrect Type Conversion or Cast  
  [CWE-704 Link](https://cwe.mitre.org/data/definitions/704.html)

## Description  
Insecure use of inline assembly refers to vulnerabilities that arise when low-level assembly code is used improperly. This can lead to:
- Incorrect type conversions or casts.
- Exploitation of vulnerabilities in low-level operations.
- Loss of funds or data.

## Remediation
- **Avoid inline assembly:** Use high-level Solidity code whenever possible.
- **Validate inputs:** Ensure all inputs to assembly code are properly validated.
- **Test thoroughly:** Conduct extensive testing to ensure assembly code is secure.

## Examples
- **Insecure Inline Assembly- Unsafe Type Casting Leads to Exploitable Overflow**
    ```solidity
    pragma solidity ^0.8.0;

    contract InsecureAssembly {
        function unsafeCast(uint256 value) public pure returns (uint8) {
            uint8 result;
            assembly {
                result := value // Unsafe cast, truncating high bits
            }
            return result;
        }
    }
    ```
⚠️ Why is this Vulnerable?
- Casting a large uint256 into uint8 without bounds checking causes integer truncation.
- If value = 257, it becomes 1 (256 is lost).
- Attackers can bypass security checks if truncation affects authentication or balance checks.

- **Secure High-Level Code- Restricted Use of Assembly with Input Validation**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureAssembly {
        function safeCast(uint256 value) public pure returns (uint8) {
            require(value <= type(uint8).max, "Value too large"); // Prevent truncation
            return uint8(value);
        }
    }
    ```
Fixes
- Bounds checking (require) prevents unintended truncation.
- Uses inline assembly only when absolutely necessary.

---