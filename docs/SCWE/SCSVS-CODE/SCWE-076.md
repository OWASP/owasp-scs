---
title: Right-To-Left-Override Control Character (U+202E)
id: SCWE-076
alias: rtl-override-character
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [451]
status: new
---

## Relationships
- CWE-451: User Interface (UI) Misrepresentation of Critical Information  
  [CWE-451 Link](https://cwe.mitre.org/data/definitions/451.html)

## Description  
The Right-To-Left-Override (RTLO) control character (U+202E) can be used to manipulate the display order of text, creating misleading or deceptive visual representations in source code. Malicious actors can exploit this to:
- Mask malicious logic or misrepresent code intent.
- Introduce security-critical bugs that are difficult to detect visually.
- Deceive auditors, developers, or end-users by obscuring real functionality.

## Remediation
- **Disallow U+202E in source code:** Ensure RTLO and similar Unicode direction control characters are explicitly banned in smart contracts.
- **Static analysis tools:** Use static analysis to detect and prevent Unicode control characters in contract source code.
- **Education and awareness:** Educate developers about the risks associated with Unicode control characters in smart contract development.

## Examples
- **Code with RTLO Character**
    ```solidity
    pragma solidity ^0.8.0;

    contract MaliciousExample {
        function performAction() public {
            // The following line contains an RTLO character to misrepresent the logic visually
            executeLogic(/* attacker logic‮/*desrever ro*/victim logic */);
        }

        function executeLogic(bytes memory logic) internal {
            // Process logic here
        }
    }
    ```

- **Code Without RTLO Character**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureExample {
        function performAction(bytes memory logic) public {
            // Properly documented and clear function calls
            executeLogic(logic);
        }

        function executeLogic(bytes memory logic) internal {
            // Process logic here
        }
    }
    ```
