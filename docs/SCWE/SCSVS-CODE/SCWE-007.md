---
title: Presence of Unused Variables
id: SCWE-007
alias: unused-variables
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [563]
status: new
---

## Relationships
- CWE-563: Assignment to Variable with No Effect
  [https://cwe.mitre.org/data/definitions/563.html](https://cwe.mitre.org/data/definitions/563.html)

## Description
The presence of unused variables in smart contracts refers to variables that are declared but never utilized in the contract logic. These variables consume storage or memory space unnecessarily, potentially wasting gas when deployed or executed. This situation often arises due to incomplete code, forgotten variables, or code that was intended for future use but never implemented. The presence of such variables increases the attack surface by making it harder to understand the contract and opens up potential vulnerabilities.

Some common risks include:
- Wasted gas due to storage and memory consumption.
- Increased complexity and difficulty in understanding contract behavior.
- Potential confusion for auditors or future developers working on the contract.

Unused variables can also hide logic errors or indicate that parts of the contract are not functioning as intended.

## Remediation
- **Remove Unused Variables:** Ensure that any variables that are not required for the contract’s functionality are removed.
- **Code Review and Refactoring:** Regularly review and refactor the code to eliminate dead or unnecessary variables.
- **Automated Static Analysis Tools:** Use static analysis tools to detect unused variables and other unnecessary code patterns.

## Examples

### Contract with Unused Variables

```solidity
pragma solidity ^0.4.0;

contract UnusedVariables {
    uint public balance;
    uint public unusedVariable; // This variable is not used anywhere

    function deposit(uint amount) public {
        balance += amount;
    }
    
    function withdraw(uint amount) public {
        balance -= amount;
    }
}
```

In the example above, the `unusedVariable` is declared but never used within the contract. This is a waste of storage space and can confuse anyone reading or auditing the code.


### Fixed Code with Unused Variables Removed
```solidity
pragma solidity ^0.4.0;

contract FixedUnusedVariables {
    uint public balance;

    function deposit(uint amount) public {
        balance += amount;
    }
    
    function withdraw(uint amount) public {
        balance -= amount;
    }
}

```
The improved contract removes the unnecessary `unusedVariable`, reducing the complexity and improving gas efficiency.

