---
title: Improper Deletion of Mappings
id: SCWE-053
alias: improper-mapping-deletion
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [459]
status: new
---

## Relationships  
- **CWE-459: Incomplete Cleanup**  
  [https://cwe.mitre.org/data/definitions/459.html](https://cwe.mitre.org/data/definitions/459.html)  

## Description  
In Solidity, mappings (`mapping(address => uint256)`) do not store key-value pairs in a way that allows them to be iterated over or deleted in a straightforward manner. Deleting a mapping variable does not remove its entries; it only resets the reference to the mapping, leaving stale data accessible if another variable references the same mapping. Improper deletion of mappings can lead to storage inconsistencies, potential access control issues, and unintended behavior.

## Remediation  
- Instead of using `delete mappingVariable;`, explicitly set each key’s value to zero where necessary.  
- Consider additional data structures (e.g., arrays or linked lists) to track mapping keys if deletion is required.  
- Ensure mapping deletions do not leave residual data that can be accessed unexpectedly.  

### Vulnerable Contract Example  
```solidity
contract Example {
    mapping(address => uint256) public balances;

    function addBalance(address user, uint256 amount) public {
        balances[user] = amount;
    }

    function resetBalances() public {
        delete balances;  // ❌ This does not clear individual key-value pairs!
    }
}
```
**Why is this vulnerable?**

- `delete balances;` only resets the storage reference but does not remove key-value pairs.
- If another contract or function still references `balances`, the data remains accessible.
- Unexpected behavior may arise where users assume balances have been erased but can still access the old data.


### Fixed Contract Example

```solidity
contract SecureExample {
    mapping(address => uint256) public balances;
    address[] private users;

    function addBalance(address user, uint256 amount) public {
        if (balances[user] == 0) {
            users.push(user);
        }
        balances[user] = amount;
    }

    function resetBalances() public {
        for (uint256 i = 0; i < users.length; i++) {
            balances[users[i]] = 0;  // ✅ Explicitly clears each entry
        }
        delete users;  // ✅ Resets the tracking array
    }
}
```

**Why is this safe?**
- Tracks users in an array to allow explicit deletion of each mapping entry.
- Ensures all key-value pairs are properly reset instead of just deleting the mapping reference.
- Prevents residual data from being accessed unintentionally.

**By properly handling mapping deletions, developers can avoid unintended data persistence and ensure accurate contract state management.**