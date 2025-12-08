---
title: Inconsistent Inheritance Hierarchy
id: SCWE-006
alias: inconsistent-inheritance-hierarchy
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-3]
  cwe: [710]
status: new
---

## Relationships
- CWE-710: Improper Adherence to Coding Standards
  [https://cwe.mitre.org/data/definitions/710.html](https://cwe.mitre.org/data/definitions/710.html)

## Description
Inconsistent inheritance hierarchies occur when a contract inherits from multiple contracts or libraries in an inconsistent or contradictory way. This leads to unexpected behavior or errors due to conflicting function implementations, state variables, or access controls. A proper and consistent inheritance structure is essential for clear logic and predictable contract execution.

Some common issues in inheritance hierarchies include:
- Ambiguous function overrides.
- Conflicting variable definitions.
- Misuse of multiple inheritance, which can lead to the diamond problem.

Inconsistent inheritance can significantly compromise a contract’s functionality and security, especially when multiple contracts or libraries with similar function names are used.

## Remediation
- **Clear Inheritance Structure:** Ensure that the inheritance hierarchy is logically structured and does not have overlapping functionalities or conflicting state variables.
- **Use Explicit Overrides:** Clearly override functions when necessary to avoid ambiguity, and ensure there is no unintentional function masking.
- **Favor Single Inheritance or Controlled Multiple Inheritance:** Avoid overly complex inheritance structures; if multiple inheritance is necessary, consider using design patterns like the Diamond Problem Resolver (i.e., using interfaces or abstract contracts).
- **Regular Audits:** Periodically audit the inheritance structure to identify any inconsistencies early on.

## Examples

### Vulnerable Contract with Inconsistent Inheritance

```solidity
pragma solidity ^0.4.0;

contract ParentA {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}

contract ParentB {
    uint public value;

    function setValue(uint _value) public {
        value = _value * 2;
    }
}

contract Child is ParentA, ParentB {
    function setValue(uint _value) public {
        // Ambiguity: which `setValue` should be called?
        ParentA.setValue(_value);
    }
}
```
In the above example, the `Child` contract inherits from both `ParentA` and `ParentB`. Both parent contracts define the `setValue` function. There is no clear indication of which function should be called, leading to ambiguity and potential bugs or undesired behavior.

### Fixed Contract with Consistent Inheritance
```solidity
pragma solidity ^0.4.0;

contract ParentA {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}

contract ParentB {
    uint public value;

    function setValue(uint _value) public {
        value = _value * 2;
    }
}

contract Child is ParentA {
    // Clear function override, only inherits from one parent
    function setValue(uint _value) public {
        ParentA.setValue(_value);
    }
}
```
In the fixed version of the contract, the `Child` contract only inherits from one parent (`ParentA`), which resolves the ambiguity. If both `ParentA` and `ParentB` were needed, explicit overriding or more careful contract design would be required to ensure the correct functionality.

