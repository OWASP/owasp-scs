---
title: Insecure Use of Fallback Functions
id: SCWE-043
alias: insecure-use-of-fallback-functions
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [250]
status: new
---

## Relationships
- **CWE-250: Execution with Unnecessary Privileges**  
  [CWE-250 Link](https://cwe.mitre.org/data/definitions/250.html)

## Description  
Insecure use of fallback functions refers to vulnerabilities that arise when fallback functions are used improperly. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data due to unintended execution.
- Exploitation of contract logic if the fallback function allows arbitrary interactions.

Fallback functions are triggered when a contract receives a call with no matching function signature. They can be used to handle Ether transfers or proxy unknown function calls. If misconfigured, they may enable unintended behaviors, such as unauthorized access or fund loss.

## Remediation
- **Restrict logic execution in fallback functions**: Avoid placing critical execution logic inside fallback functions unless necessary.  
- **Separate Ether reception**: Use `receive()` explicitly to handle Ether transfers instead of overloading `fallback()`.  
- **Validate calls**: Ensure fallback functions do not execute unintended behavior. If required, use access control for specific use cases (e.g., controlled proxy calls).  
- **Use explicit function definitions**: Instead of relying on fallback functions for critical operations, define explicit functions with proper access control.  

## Examples
### 🚨 **Insecure Fallback Function**
#### *Problem: No access control or validation, allowing unintended execution.*
```solidity
pragma solidity ^0.8.0;

contract InsecureFallback {
    fallback() external {
        // No access control or validation
    }
}
```
- This contract allows any call with an unknown function signature to trigger the fallback function, which could result in unintended behavior.

###  Secure Fallback Function (Safe Handling of Ether)
- Solution: Explicitly handle Ether transfers using receive()

```solidity
pragma solidity ^0.8.0;

contract SecureFallback {
    address public admin;

    constructor(address _admin) {
        admin = _admin;
    }

    // Explicitly define a receive function to safely accept Ether
    receive() external payable {}

    // Safe fallback function (does nothing if unintentionally called)
    fallback() external payable {
        // Optional: Log unexpected calls for security monitoring
    }
}
```
This version properly separates Ether reception from fallback execution, preventing unintended behavior.

---