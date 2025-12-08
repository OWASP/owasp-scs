---
id: SCSTG-TEST-0016
scsvs_cg_id:
- SCSVS-ORACLE
scsvs_scg_id:
- SCSVS-ORACLE-1
platform: []
title: Testing Arithmetic and Logic Security
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0016
---

### **Description**
Preventing arithmetic overflow and underflow is critical for maintaining the integrity and security of smart contracts. If a contract performs arithmetic operations without proper safeguards, it is vulnerable to overflow and underflow issues, which can be exploited by attackers to manipulate contract behavior, causing unexpected results or loss of funds.

---

### **Test 1: Ensure Safe Math Operations are Used**

#### Vulnerable Code:

```solidity
pragma solidity ^0.8.0;

contract UnsafeMath {
    uint256 public balance;

    function addFunds(uint256 _amount) public {
        balance += _amount;  // Possible overflow if balance + _amount exceeds max uint256 value
    }
}
```
#### **Why It’s Vulnerable**
The contract does not use a safe math library to perform arithmetic operations. If the balance exceeds uint256's maximum value (2^256 - 1), an overflow occurs.  
This can result in unexpected contract behavior or a reset of the balance value, allowing attackers to manipulate the contract.

#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract SafeMath {
    using SafeMath for uint256;
    uint256 public balance;

    function addFunds(uint256 _amount) public {
        balance = balance.add(_amount);  // Safe addition using SafeMath to prevent overflow
    }
}
```

#### **How to Check**
- **Code Review:** Check that all arithmetic operations use libraries such as SafeMath (for older versions) or rely on Solidity 0.8’s built-in overflow checks.  
- **Testing:** Use edge cases such as adding large values to check if the contract prevents overflow.

---

### **Test 2: Verify Correct Use of Fixed-Point Arithmetic**


#### Vulnerable Code:

```solidity
pragma solidity ^0.8.0;

contract FixedPointExample {
    uint256 public totalSupply;

    function calculateReward(uint256 _rewardPercentage) public view returns (uint256) {
        return totalSupply * _rewardPercentage / 100;  // Simple calculation without considering fixed-point precision
    }
}
```


#### **Why It’s Vulnerable**
The function performs division without accounting for fixed-point precision. This could result in rounding errors, especially for small percentage values.  
Using integer division directly leads to truncation, causing inaccuracies in reward calculations.

#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract FixedPointExample {
    uint256 public totalSupply;
    uint256 constant FIXED_POINT = 1e18;  // Set a scaling factor for fixed-point precision

    function calculateReward(uint256 _rewardPercentage) public view returns (uint256) {
        return (totalSupply * _rewardPercentage * FIXED_POINT) / 100 / FIXED_POINT;  // Proper fixed-point arithmetic
    }
}

```

#### **How to Check**
- **Code Review:** Verify that fixed-point arithmetic is implemented using appropriate scaling factors (e.g., 1e18) to avoid precision loss.  
- **Dynamic Testing:** Test the function with small values for `_rewardPercentage` and check that the result is accurate, verifying that there is no unexpected rounding behavior.