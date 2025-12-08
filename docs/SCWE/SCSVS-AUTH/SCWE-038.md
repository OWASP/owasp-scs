---
title: Insecure Use of Selfdestruct
id: SCWE-038
alias: insecure-use-of-selfdestruct
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [732]
status: new
---

## Relationships
- CWE-732: Incorrect Permission Assignment for Critical Resource  
  [CWE-732 Link](https://cwe.mitre.org/data/definitions/732.html)

## Description  
Insecure use of selfdestruct refers to vulnerabilities that arise when the `selfdestruct` function is used without proper safeguards. This can lead to:
- Unauthorized destruction of the contract.
- Loss of funds or data.
- Exploitation of vulnerabilities in contract logic.

## Remediation
- **Restrict access:** Ensure only authorized addresses can call `selfdestruct`.
- **Implement circuit breakers:** Add mechanisms to halt operations in case of suspicious activity.
- **Test thoroughly:** Conduct extensive testing to ensure `selfdestruct` is used securely.

## Examples
- **Insecure Selfdestruct Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract InsecureSelfdestruct {
        function destroy() public {
            selfdestruct(payable(msg.sender)); // No access control
        }
    }
    ```

- **Secure Selfdestruct Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureSelfdestruct {
        address public admin;

        constructor(address _admin) {
            admin = _admin;
        }

        modifier onlyAdmin() {
            require(msg.sender == admin, "Unauthorized");
            _;
        }

        function destroy() public onlyAdmin {
            selfdestruct(payable(admin)); // Restricted to admin
        }
    }
    ```

---