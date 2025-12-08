---
id: SCSTG-TEST-0014
scsvs_cg_id:
- SCSVS-DEFI
scsvs_scg_id:
- SCSVS-DEFI-1
platform: []
title: Test Gas Usage in Loops
scsvs_cg_levels:
- L2
tests:
- SCSTG-TEST-0014
---

### **Description**
Efficient gas usage is critical in smart contract development to ensure transactions are cost-effective and do not exceed block gas limits. Poorly optimized contracts can result in high transaction costs, failed transactions, and potential denial of service (DoS) attacks. Optimizing gas usage helps ensure that smart contracts are scalable, cost-effective, and maintain the overall security of decentralized applications (dApps). This test focuses on ensuring that gas usage is properly optimized, and contracts are designed to operate efficiently within the constraints of Ethereum's gas limits.

---

### **Test 1: Validate Gas Usage in Loops**

#### **Vulnerable Code**

```solidity
pragma solidity ^0.8.0;

contract GasInefficient {
    uint256[] public data;

    function addData(uint256[] memory newData) public {
        for (uint i = 0; i < newData.length; i++) {
            data.push(newData[i]);  // Inefficient loop causing high gas costs
        }
    }
}
```

#### **Why It’s Vulnerable**
- This contract uses a loop to iterate over an input array and push data into a dynamic array.  
- The gas cost increases linearly with the size of the input array. For large datasets, this can lead to excessive gas usage, potentially causing the transaction to exceed the block gas limit.  
- Smart contracts with inefficient loops that grow dynamically can become unmanageable when interacting with large datasets.


#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract OptimizedGas {
    uint256[] public data;

    function addData(uint256[] memory newData) public {
        uint256 length = newData.length;
        for (uint i = 0; i < length; i++) {
            data.push(newData[i]);  // Optimized by storing array length outside the loop
        }
    }
}
```

#### **How to Check**
- **Code Review:** Ensure that loops and functions which deal with dynamic data structures are optimized for gas usage. Look for unnecessary state changes or excessive iterations within a single transaction.  
- **Gas Estimation:** Use tools like eth-gas-reporter or Remix IDE to estimate gas usage before and after optimizations.  
- **Dynamic Testing:** Test the contract with various input sizes and check that it performs within reasonable gas limits, ensuring it doesn't exceed the block gas limit.