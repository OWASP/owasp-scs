---
title: Shadowing Variables and Functions
id: SCWE-010
alias: shadowing-variables-functions
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [1109]
status: new
---

## Relationships
- **CWE-1109: Use of Same Variable for Multiple Purposes**  
  [CWE-1109](https://cwe.mitre.org/data/definitions/1109.html)  
  Description: This weakness occurs when a variable is used for multiple purposes in a way that causes confusion, bugs, or unintentional side effects. In the context of smart contracts, shadowing variables leads to such misuse, as it causes ambiguity between different scopes.

## Description
Shadowing variables or functions is a scenario where a local variable or function shares the same name as one in a larger or outer scope. This can cause ambiguity and lead to unexpected behavior or bugs, as the inner variable or function hides the outer one. This problem is especially tricky in Solidity due to its inheritance model, where a child contract might unintentionally override parent contract variables or functions.

### Key issues:
- **Ambiguity**: The developer might not be aware that a variable or function is being hidden.
- **Unintentional logic errors**: It may lead to the wrong variable being accessed, or the wrong function being called.
- **Difficulty in debugging**: Shadowing makes the code harder to understand and trace, especially in complex contracts or when inheritance is involved.

## Remediation
- **Use unique and descriptive names**: Always use unique names for variables and functions to avoid shadowing. Use clear, descriptive names for contract variables and functions.
- **Avoid redeclaring variables in nested scopes**: Ensure that variables or functions in inner scopes don’t conflict with those in outer scopes.
- **Static analysis tools**: Use static analysis tools to detect and warn about shadowing issues.

## Examples

### Example of Shadowing Variables and Functions

```solidity
pragma solidity ^0.4.0;

contract ShadowingExample {
    uint public balance;

    // This function shadows the 'balance' variable
    function deposit(uint balance) public {
        // Local variable 'balance' now shadows the contract's balance variable
        balance += balance;  // This operation affects the local 'balance', not the contract's state variable
    }
}

contract Test {
    ShadowingExample example;

    constructor() public {
        example = new ShadowingExample();
    }

    function testDeposit() public {
        example.deposit(100);  // Calling the deposit function on the example contract
    }
}
```
In the above example, the parameter `balance` in the `deposit` function shadows the contract’s state variable `balance`. This causes confusion, and the operation `balance += balance`; modifies the local variable instead of the contract state variable, leading to unexpected behavior.

### Fixed Code

```solidity
pragma solidity ^0.4.0;

contract ShadowingExample {
    uint public balance;

    // The parameter is renamed to avoid shadowing the state variable 'balance'
    function deposit(uint amount) public {
        balance += amount;  // Correctly updates the contract's state variable
    }
}

contract Test {
    ShadowingExample example;

    constructor() public {
        example = new ShadowingExample();
    }

    function testDeposit() public {
        example.deposit(100);  // Calling the deposit function on the example contract
    }
}
```
In the optimized version, the function parameter is renamed from `balance` to `amount` to avoid shadowing the state variable. This clears up the ambiguity and ensures the function operates on the contract's state variable, not the local variable.

