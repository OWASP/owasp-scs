---
title: Insecure Use of Storage
id: SCWE-044
alias: insecure-use-of-storage
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
Insecure use of storage refers to vulnerabilities that arise when storage variables are improperly managed. This can lead to:
- Unauthorized access to sensitive data.
- Loss of funds or data.
- Exploitation of vulnerabilities in contract logic.

## Remediation
- **Encrypt sensitive data:** Encrypt sensitive data before storing it.
- **Validate inputs:** Ensure all storage updates are properly validated.
- **Test thoroughly:** Conduct extensive testing to ensure storage is secure.

## Examples
- **Insecure Storage Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract InsecureStorage {
        uint public balance;

        function updateBalance(uint newBalance) public {
            balance = newBalance; // No validation
        }
    }
    ```

- **Secure Storage Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureStorage {
        uint public balance;

        function updateBalance(uint newBalance) public {
            require(newBalance > 0, "Invalid balance"); // Input validation
            balance = newBalance;
        }
    }
    ```

---