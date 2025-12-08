---
title: Unnamed Function Parameters
id: SCWE-093
alias: Unnamed-Function-Parameters
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [710]
status: new
---

## Relationships
- **CWE-710**: [Improper Adherence to Coding Standards](https://cwe.mitre.org/data/definitions/710.html)

## Description  
This weakness occurs when functions declare parameters without names (only types). Unnamed parameters reduce code clarity and hinder maintainability, making it difficult for reviewers and future maintainers to understand the purpose and expected usage of each argument. In smart contracts, where correctness is critical, this ambiguity can result in misinterpretation, incorrect argument ordering in calls or refactors, and subtle logic errors.

## Impact  
Lack of clear parameter names can lead to:
- Misuse of function arguments due to misunderstanding of their meaning.  
- Increased likelihood of logic bugs during refactoring and maintenance.  
- Higher audit and review overhead; reduced readability and self-documentation.  
- Potential security issues if parameters are confused (e.g., recipient vs. sender, amount vs. fee).  

## Remediation  
- Always provide descriptive names for all function parameters.  
- Choose meaningful, self-explanatory names consistent with a coding standard.  
- Supplement with NatSpec where helpful to document parameter intent and units.  
- Enforce naming conventions with linters and code review checklists.  

## Examples  
- **❌ Vulnerable Code (Unnamed parameters reduce clarity)**  
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract Example {
    function transfer(address, uint256, bytes memory) public {
        // Function logic
    }
}
```

- **✅ Safe Code (Named parameters improve readability)**  
```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract Example {
    function transfer(address recipient, uint256 amount, bytes memory data) public {
        // Function logic
    }
}
```


