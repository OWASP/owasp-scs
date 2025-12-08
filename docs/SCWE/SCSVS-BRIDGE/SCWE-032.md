---
title: Dependency on Block Gas Limit
id: SCWE-032
alias: dependency-on-block-gas-limit
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-2]
  cwe: [400]
status: new
---

## Relationships
- CWE-400: Uncontrolled Resource Consumption  
  [CWE-400 Link](https://cwe.mitre.org/data/definitions/400.html)

## Description  
Dependency on block gas limit refers to the reliance on the Ethereum block gas limit for contract operations, which can lead to:
- Failed transactions if gas limits are exceeded.
- Exploitation of vulnerabilities in gas-intensive operations.
- Loss of funds or data.

## Remediation
- **Optimize gas usage:** Minimize gas consumption in contract operations.
- **Avoid unbounded loops:** Ensure loops have a fixed upper limit.
- **Test thoroughly:** Conduct extensive testing to ensure operations stay within gas limits.

## Examples
- **Gas-Intensive Operation- Storing Large Dynamic Data**
    ```solidity
    pragma solidity ^0.8.0;

    contract GasIntensive {
        uint[] public largeArray;

        function appendData(uint[] memory data) public {
            for (uint i = 0; i < data.length; i++) {
                largeArray.push(data[i]); // Storing a large dataset in a single transaction
            }
        }
    }
    ```
- This contract appends large arrays in a single transaction, which fails when the block gas limit is exceeded.
- Attackers could exploit this by forcing high gas consumption and causing DoS attacks (e.g., filling storage inefficiently).

- **Optimized Gas Usage- Chunk Processing & Gas Efficiency**
    ```solidity
    pragma solidity ^0.8.0;

    contract GasOptimized {
        uint[] public largeArray;

        function appendData(uint[] memory data, uint start, uint end) public {
            require(end <= data.length, "Invalid range");
            for (uint i = start; i < end; i++) {
                largeArray.push(data[i]); // Process in controlled batches
            }
        }
    }
    ```

Why is this better?
- The start and end parameters allow batch processing instead of handling everything in a single call.
- Prevents hitting the block gas limit by splitting work across multiple transactions.
---