---
id: SCSTG-TEST-0007
scsvs_cg_id:
- SCSVS-ARCH
scsvs_scg_id:
- SCSVS-ARCH-2
platform: []
title: Modularity and Upgradability
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0007
---

### **Description**
Modularity and upgradability are essential principles for the long-term security and maintainability of smart contracts. Poor modularity often leads to monolithic designs that combine critical logic and storage, making it difficult to upgrade, audit, or scale the system. Without controlled upgrade mechanisms, an attacker could exploit weaknesses in the upgrade process, leading to unauthorized contract changes or the introduction of security flaws. Ensuring a well-structured contract with clear modular separation, as well as a secure upgrade process, is crucial to avoiding such vulnerabilities.

---

### **Test 1: Ensure Proper Separation of Logic and State**

#### Vulnerable Code
```solidity
contract Monolithic {
    uint256 public data;
    address public admin;

    function updateData(uint256 _data) public {
        require(msg.sender == admin, "Unauthorized");
        data = _data;
    }

    function upgrade(address newAdmin) public {
        require(msg.sender == admin, "Unauthorized");
        admin = newAdmin;
    }
}
```

### **Why It’s Vulnerable**
- The monolithic design combines logic and state in a single contract, making upgrades risky.
- Changes to storage or logic could inadvertently corrupt existing data.
- The lack of separation makes it more difficult to isolate bugs or vulnerabilities in logic.

#### Fixed Code:

```solidity
contract Logic {
    address public admin;
    Storage public storageContract;

    constructor(address _storageContract) {
        admin = msg.sender;
        storageContract = Storage(_storageContract);
    }

    function updateData(uint256 _data) public {
        require(msg.sender == admin, "Unauthorized");
        storageContract.setData(_data);
    }
}

contract Storage {
    uint256 public data;

    function setData(uint256 _data) public {
        data = _data;
    }
}
```
#### **How to Check**
- Code Review: Verify the separation of logic and storage into separate contracts.
- Storage Analysis: Ensure that the storage layout remains intact when upgrading the contract logic, and that no data corruption occurs.

### **Test 2: Verify Secure and Controlled Upgrade Mechanism**

#### Vulnerable Code:

```solidity
contract Proxy {
    address public implementation;

    function upgrade(address newImplementation) public {
        implementation = newImplementation;
    }
}
```

### **Why It’s Vulnerable**
- The upgrade function is not protected with any access control, allowing any user to replace the implementation contract. This opens the door for malicious actors to hijack the contract functionality.

#### Fixed Code:
```solidity
contract SecureProxy {
    address public implementation;
    address public admin;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Unauthorized");
        _;
    }

    function upgrade(address newImplementation) public onlyAdmin {
        implementation = newImplementation;
    }
}

```

#### **How to Check**
- Code Review: Ensure that upgrade functions are protected by access control mechanisms (e.g., only the admin can upgrade).
- Dynamic Testing: Attempt to perform an unauthorized upgrade to verify that the access control works as intended.