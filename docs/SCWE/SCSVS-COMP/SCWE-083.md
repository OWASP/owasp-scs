---
title: Failure to Handle Edge Cases
id: SCWE-083
alias: failure-to-handle-edge-cases
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMP]
  scsvs-scg: [SCSVS-COMP-2]
  cwe: [754]
status: new
---

## Relationships  
- CWE-754: Improper Check for Unusual or Exceptional Conditions  
  [https://cwe.mitre.org/data/definitions/754.html](https://cwe.mitre.org/data/definitions/754.html)  

## Description
Failure to account for edge cases can result in unexpected behaviors, security vulnerabilities, and unintended contract failures. Edge cases are unusual but possible inputs or states that developers often overlook, leading to incorrect logic, reverts, or even exploits.

### Common scenarios include:

- Arithmetic Issues (e.g., division by zero, integer overflow/underflow, precision loss).
- Boundary Conditions (e.g., handling empty arrays, minimum/maximum values).
- State-Dependent Bugs (e.g., failing to check for uninitialized variables, invalid state transitions).
- Gas-Related Failures (e.g., unbounded loops consuming excessive gas).

## Remediation
Ensure that all edge cases are properly considered and handled during the development of the contract. Utilize `require` and `assert` to ensure proper validation of inputs, outputs, and states.
- Implement explicit validation for all possible edge cases.
- Use Solidity's built-in safety features (e.g., SafeMath, Solidity 0.8 overflow checks).
- Use require/assert statements to enforce input constraints and expected states.
- Test contracts thoroughly, including stress tests, fuzzing, and invariant testing.



### Vulnerable Contract Example-  (Arithmetic Issue)
```solidity
contract Example {
    function divide(uint256 _numerator, uint256 _denominator) public pure returns (uint256) {
        return _numerator / _denominator; // Division by zero is not checked
    }
}
```
### Fixed Contract Example
- Solution: Use `require` to check for division by zero.
```solidity
contract Example {
    function divide(uint256 _numerator, uint256 _denominator) public pure returns (uint256) {
        require(_denominator != 0, "Cannot divide by zero");
        return _numerator / _denominator;
    }
}
```

### Handling Empty Arrays
- Issue: A function assumes that the array is never empty, leading to an out-of-bounds error.

```solidity
contract Example {
    uint256[] public data;

    function getLast() public view returns (uint256) {
        return data[data.length - 1]; // ❌ Reverts if array is empty
    }
}
```

### Fixed Code:
-  Solution: Validate that the array is not empty before accessing elements.
```solidity
contract Example {
    uint256[] public data;

    function getLast() public view returns (uint256) {
        require(data.length > 0, "Array is empty");
        return data[data.length - 1];
    }
}
```