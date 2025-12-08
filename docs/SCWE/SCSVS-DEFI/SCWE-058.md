---
title: DoS with Block Gas Limit
id: SCWE-058
alias: dos-block-gas-limit
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-1]
  cwe: [400]
status: new
---

## Relationships  
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)  

## Description
Denial of Service (DoS) with block gas limit occurs when a contract is designed in such a way that its execution depends on a large amount of gas, potentially exceeding the block gas limit. This can result in the transaction failing, causing the contract to become unavailable or unusable. Attackers can exploit this vulnerability by creating transactions that consume excessive gas, effectively locking the contract or preventing normal operation.

## Remediation
To mitigate this vulnerability, ensure that operations that depend on gas consumption are efficient and that gas limits are taken into account when designing contract logic. Avoid functions that require large amounts of gas to complete, and consider implementing features like batching or chunking operations to spread the gas usage across multiple transactions.

### Vulnerable Contract Example
```solidity
contract GasLimitDoS {
    uint256[] public data;

    function addData(uint256[] memory newData) public {
        for (uint256 i = 0; i < newData.length; i++) {
            data.push(newData[i]);  // Can consume a large amount of gas if the array is large
        }
    }
}
```
### Fixed Contract Example
```solidity
contract GasLimitSafe {
    uint256[] public data;

    function addData(uint256[] memory newData) public {
        uint256 batchSize = 100;  // Limit the batch size to avoid excessive gas usage
        for (uint256 i = 0; i < newData.length && i < batchSize; i++) {
            data.push(newData[i]);
        }
    }
}
```