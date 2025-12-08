---
title: Insecure Use of Modifiers
id: SCWE-045
alias: insecure-use-of-modifiers
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-2]
  cwe: [732]
status: new
---

## Relationships
- CWE-732: Incorrect Permission Assignment for Critical Resource  
  [CWE-732 Link](https://cwe.mitre.org/data/definitions/732.html)

## Description  
Insecure use of modifiers refers to vulnerabilities that arise when modifiers are used improperly. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data.
- Exploitation of vulnerabilities in contract logic.

## Remediation
- **Restrict access:** Ensure only authorized addresses can use the modifier.
- **Validate inputs:** Ensure all inputs to the modifier are properly validated.
- **Test thoroughly:** Conduct extensive testing to ensure modifiers are secure.

## Examples
- **Insecure Modifier Usage (With Storage Bug)**
    ```solidity
    pragma solidity ^0.8.0;

    contract InsecureModifier {
        address public admin;

        constructor(address _admin) {
            admin = _admin; // ❌ Storage bug: Allows setting admin to zero address.
        }

        modifier onlyAdmin() {
            require(admin == address(0), "Unauthorized"); // ❌ Wrong condition, only works if admin is zero!
            _;
        }

        function updateAdmin(address newAdmin) public onlyAdmin {
            admin = newAdmin; // ❌ Can set admin to zero address, breaking access control.
        }

        function updateBalance(uint newBalance) public onlyAdmin {
            // Update balance
        }
    }
    ```


**Why is this Insecure?**
- Wrong Condition in `onlyAdmin()`
    - `require(admin == address(0), "Unauthorized");` only allows function execution when admin is zero.
    - This means no valid admin can ever execute admin functions!
    - If admin is ever non-zero, all `onlyAdmin` functions become unusable.
    
- Loss of Control
    - If admin is accidentally set to `address(0)`, anyone can now execute admin functions, breaking security

- **Secure Modifier Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureModifier {
        address public admin;

        constructor(address _admin) {
            require(_admin != address(0), "Invalid admin address"); // ✅ Proper validation
            admin = _admin;
        }

        modifier onlyAdmin() {
            require(msg.sender == admin, "Unauthorized"); // ✅ Correctly restricts access
            _;
        }

        function updateAdmin(address newAdmin) public onlyAdmin {
            require(newAdmin != address(0), "New admin cannot be zero address"); // ✅ Prevents admin loss
            admin = newAdmin;
        }

        function updateBalance(uint newBalance) public onlyAdmin {
            // Update balance securely
        }
    }
    ```

**Why is this Secure?**
- Proper access control in `onlyAdmin()`
    - `require(msg.sender == admin, "Unauthorized");` ensures only the correct admin can execute admin functions.
        - Prevents privilege escalation
- `updateAdmin()` prevents setting `admin = address(0)`, avoiding unintended loss of access.

---