---
title: Shadowing State Variables
id: SCWE-069
alias: shadowing-state-variables
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [1001]
status: new
---

## Relationships  
- CWE-1001: Variable Shadowing  
  [https://cwe.mitre.org/data/definitions/1001.html](https://cwe.mitre.org/data/definitions/1001.html)  

## Description
Shadowing occurs when a state variable in a derived contract uses the same name as one in the base contract. This can lead to confusion and unexpected behavior, as the derived contract will hide the state variable from the base contract, potentially causing errors in contract logic or making it harder to maintain and audit the code.

It is essential to avoid naming state variables in derived contracts the same as those in base contracts to ensure that the intended state is correctly accessed and modified.

## Remediation
To avoid state variable shadowing, use unique names for state variables in derived contracts or explicitly refer to the base contract variable using `super`. This will ensure that the correct state variable is accessed and manipulated as intended.

### Vulnerable Contract Example
```solidity
contract Base {
    uint public balance;

    constructor() {
        balance = 100;
    }
}

contract Derived is Base {
    uint public balance;  // Shadows state variable from Base contract

    function updateBalance(uint amount) public {
        balance = amount;  // Refers to Derived's balance, not Base's balance
    }
}
```

### Fixed Contract Example
```solidity
contract Base {
    uint public balance;

    constructor() {
        balance = 100;
    }
}

contract Derived is Base {
    uint public newBalance;  // Unique name for Derived contract

    function updateBalance(uint amount) public {
        newBalance = amount;  // Updates Derived's balance without shadowing
    }
}
```