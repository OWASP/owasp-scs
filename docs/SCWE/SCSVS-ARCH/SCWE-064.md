---
title: Incorrect Inheritance Order
id: SCWE-064
alias: incorrect-inheritance-order
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-2]
  cwe: [1001]
status: new
---

## Relationships  
- CWE-1001: Variable Shadowing  
  [https://cwe.mitre.org/data/definitions/1001.html](https://cwe.mitre.org/data/definitions/1001.html)  

## Description
Incorrect inheritance order in Solidity can lead to unintended behavior, especially when multiple base contracts define similar variables or functions. Solidity’s linearization of the inheritance order can result in one contract unintentionally overriding or shadowing variables or functions defined in a parent contract, leading to confusion, errors, and potential vulnerabilities.

In Solidity, the order of inheritance matters. If the inheritance hierarchy is not properly structured, the wrong version of a variable or function may be called, causing bugs or security issues.

## Remediation
To mitigate this vulnerability, carefully review and order the inheritance structure. Ensure that parent contracts are inherited in a logical sequence and that any variables or functions are not unintentionally shadowed or overridden. Consider following a clear and consistent inheritance pattern.

### Vulnerable Contract Example
```solidity
contract BaseA {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}

contract BaseB {
    uint public value;

    function setValue(uint _value) public {
        value = _value + 1;  // Different implementation
    }
}

contract Child is BaseB, BaseA {
    function setValue(uint _value) public {
        value = _value + 2;  // Shadows value from BaseA or BaseB
    }
}
```

### Fixed Contract Example
```solidity
contract BaseA {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}

contract BaseB {
    uint public value;

    function setValue(uint _value) public {
        value = _value + 1;  // Different implementation
    }
}

contract Child is BaseA, BaseB {
    function setValue(uint _value) public {
        value = _value + 2;  // Calls setValue from BaseA or BaseB intentionally
    }
}
```