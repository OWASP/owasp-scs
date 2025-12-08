---
id: SCSTG-TEST-0011
scsvs_cg_id:
- SCSVS-COMM
scsvs_scg_id:
- SCSVS-COMM-1
platform: []
title: Test Contract Interactions 
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0011
---

### **Description**
Ensuring secure interactions and communications in smart contracts is crucial for protecting against unauthorized access, manipulation, and attacks. This includes ensuring that contracts interact securely with external contracts, manage oracle integrations safely, and use secure methods for cross-chain and bridge operations. A failure to adhere to best practices for these interactions can expose the contract to vulnerabilities such as reentrancy, front-running, or incorrect data feeds. This test focuses on validating that smart contracts perform secure interactions and communications, safeguarding the system from common attack vectors.

---

### **Test 1: Ensure Secure Contract Interactions**

#### **Vulnerable Code:**

```solidity
pragma solidity ^0.5.0;

contract VulnerableContract {
    address public trustedAddress;

    constructor(address _trustedAddress) public {
        trustedAddress = _trustedAddress;
    }

    function callExternalContract(address _to, uint256 _value) public {
        _to.call{value: _value}(""); // Vulnerable to reentrancy or other attacks
    }
}
```

### **Why It’s Vulnerable**
- The contract uses `.call` to make external calls, which is generally unsafe and susceptible to reentrancy attacks.
- The function allows anyone to trigger the call and transfer funds, exposing the contract to potential attacks.


#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract SecureContract {
    address public trustedAddress;

    constructor(address _trustedAddress) {
        trustedAddress = _trustedAddress;
    }

    function callExternalContract(address _to, uint256 _value) public {
        require(_to != address(0), "Invalid address");
        (bool success, ) = _to.call{value: _value}("");
        require(success, "External call failed");
    }
}
```
### **How to Check**
- **Code Review:** Look for external calls in the contract and ensure that they are using safe methods such as `transfer` or `send` where appropriate, or implementing reentrancy protection.
- **Static Analysis:** Use static analysis tools like SolidityScan, MythX or Slither to detect unsafe calls in the code.
- **Dynamic Testing:** Simulate a reentrancy attack by deploying a contract that calls the vulnerable contract and tries to drain funds.
