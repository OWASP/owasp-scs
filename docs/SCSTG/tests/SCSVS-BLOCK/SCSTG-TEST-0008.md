---
id: SCSTG-TEST-0008
scsvs_cg_id:
- SCSVS-BLOCK
scsvs_scg_id:
- SCSVS-BLOCK-1
platform: []
title: Efficient Loop and Function Design
scsvs_cg_levels:
- L1
tests: SCSTG-TEST-0008
---

### **Description**  
Inefficient loop and function designs in smart contracts can result in excessive gas consumption, leading to out-of-gas errors and potential denial-of-service (DoS) vulnerabilities. Smart contract security auditors must ensure that all loops and functions are optimized to operate within Ethereum's block gas limit.

### **Test 1: Detecting Unbounded Loops**

#### **Objective**  
Identify and mitigate the use of unbounded loops in contract code, as they are vulnerable to excessive gas usage.  

#### **Vulnerable Code Example**  
```solidity
pragma solidity ^0.8.0;

contract UnboundedLoopExample {
    uint[] public data;

    function processAll() public {
        for (uint i = 0; i < data.length; i++) {
            // This operation scales with the size of the array
            data[i] = data[i] + 1;
        }
    }
}
```

### **Why It’s Vulnerable**

The loop iterates over the entire `data` array, which could grow indefinitely.  
- For large arrays, gas consumption may exceed the block gas limit, causing the transaction to fail.  
- Attackers could exploit this by filling the array, making the function unusable for legitimate users.  

### **How to Check**  
- **Code Review:** Look for `for` or `while` loops operating on dynamic arrays or mappings without size constraints.  
- **Dynamic Input Testing:** Test the function with a large dataset to simulate its behavior near the gas limit.  
- **Review Documentation:** Ensure the contract specifies constraints on data growth and function usage.  


### **Fixed Code Example** 

```solidity
pragma solidity ^0.8.0;

contract BoundedLoopExample {
    uint[] public data;

    function processBatch(uint start, uint end) public {
        require(end <= data.length, "End index out of bounds");
        for (uint i = start; i < end; i++) {
            data[i] = data[i] + 1;
        }
    }
}
```

---

### **Test 2: Identifying Inefficient Nested Loops**

#### **Objective**  
- Detect and address inefficient nested loops that exponentially increase gas consumption.


### Vulnerable Code:

```solidity
pragma solidity ^0.8.0;

contract NestedLoopExample {
    uint[][] public matrix;

    function processMatrix() public {
        for (uint i = 0; i < matrix.length; i++) {
            for (uint j = 0; j < matrix[i].length; j++) {
                matrix[i][j] = matrix[i][j] * 2;
            }
        }
    }
}
```

### **Why It’s Vulnerable**

Nested loops increase the complexity of the operation, leading to higher gas costs as input size increases.  
- Large datasets could render the function unusable within the gas limits, causing DoS conditions.  

### **How to Check**  
- **Code Review:** Examine nested loops in the code and assess their gas consumption relative to the input size.  
- **Gas Profiling:** Use tools like `eth-gas-reporter` to analyze gas usage during testing.  
- **Dynamic Testing:** Simulate scenarios with large `matrix` sizes to observe the contract’s behavior under stress.  

```solidity
pragma solidity ^0.8.0;

contract OptimizedNestedLoopExample {
    uint[][] public matrix;

    function processMatrixBatch(uint startRow, uint endRow) public {
        require(endRow <= matrix.length, "End row exceeds matrix size");
        for (uint i = startRow; i < endRow; i++) {
            for (uint j = 0; j < matrix[i].length; j++) {
                matrix[i][j] = matrix[i][j] * 2;
            }
        }
    }
}
```