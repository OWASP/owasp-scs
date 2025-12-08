---
title: Excessive Contract Complexity
id: SCWE-002
alias: excessive-complexity
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [710]
status: new
---

## Relationships
- CWE-710: Improper Adherence to Coding Standards  
  [https://cwe.mitre.org/data/definitions/710.html](https://cwe.mitre.org/data/definitions/710.html)

## Description
Excessive contract complexity refers to situations where the design or implementation of a smart contract becomes overly complicated, making it difficult to understand, audit, and maintain. Such complexity increases the likelihood of introducing bugs and vulnerabilities that may not be apparent during development or testing. It often arises from:

- Overuse of complex inheritance structures or external libraries.
- Too many functions, interdependencies, and conditions within the contract.
- Unnecessarily convoluted logic that could be simplified.

The more complex the code, the higher the chance that mistakes are made, especially if future developers or auditors need to interact with the contract. Complexity can lead to hidden vulnerabilities that may be exploited over time.

## Remediation
- **Refactor and simplify the code**: Break down complex functions into smaller, easier-to-understand components.
- **Limit inheritance depth**: Use inheritance judiciously and prefer composition over deep inheritance chains.
- **Use clear and descriptive names**: Functions, variables, and events should have self-explanatory names that indicate their purpose.
- **Avoid redundant logic**: Consolidate repeated logic into reusable functions or libraries.
- **Ensure modularity**: Split the contract into manageable modules that focus on specific tasks, improving readability and maintainability.

## Examples

### Excessive Complexity

```solidity
pragma solidity ^0.4.0;

contract ComplexContract {
    uint public balance;
    address public owner;

    function ComplexFunction1(uint value) public {
        // Complex logic with many conditions
        if (value > 10) {
            // do something
        }
        // Multiple nested functions and too many conditions
        for (uint i = 0; i < value; i++) {
            if (i % 2 == 0) {
                // nested loop
            }
        }
    }

    function ComplexFunction2(address addr) public {
        // Complex logic with external dependencies
        SomeLibrary.someFunction(addr);
    }
}
```

### Simplified Version

```solidity
pragma solidity ^0.4.0;

contract SimpleContract {
    uint public balance;
    address public owner;

    function deposit(uint value) public {
        balance += value;
    }

    function withdraw(uint value) public {
        require(balance >= value, "Insufficient funds");
        balance -= value;
    }
}
```