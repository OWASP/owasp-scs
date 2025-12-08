---
title: Incorrect Constructor Name
id: SCWE-070
alias: incorrect-constructor-name
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [1001]
status: new
---

## Relationships  
- CWE-1001: Variable Shadowing  
  [https://cwe.mitre.org/data/definitions/1001.html](https://cwe.mitre.org/data/definitions/1001.html)  

## Description
In Solidity, the constructor is a special function used to initialize a contract's state variables when it is deployed. If a constructor is incorrectly named, it will not function as expected, leading to issues such as failing to initialize state variables or triggering unexpected behavior. The constructor must have the exact name of the contract and no return type.

If the constructor name is not correct, it will not be executed as intended, and the contract may not behave as expected, potentially leaving it in an uninitialized or inconsistent state.

## Remediation
Ensure that the constructor has the correct name, which must match the contract name and contain no return type. In newer versions of Solidity (0.4.22 and later), the constructor keyword is used instead of the contract name for constructor functions.

### Vulnerable Contract Example
```solidity
contract Example {
    uint public value;

    // Incorrect constructor name (for Solidity <0.4.22)
    function Example() public {  // Constructor name must match the contract name in older Solidity versions
        value = 10;
    }
}
```

### Fixed Contract Example
```solidity
contract Example {
    uint public value;

    // Correct constructor definition (Solidity >=0.4.22)
    constructor() public {  // Use "constructor" instead of the contract name
        value = 10;
    }
}
```