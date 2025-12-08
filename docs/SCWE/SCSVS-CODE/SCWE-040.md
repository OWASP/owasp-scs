---
title: Incorrect Storage Packing
id: SCWE-040
alias: incorrect-storage-packing
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [805]
status: new
---


## Relationships  
- **CWE-805: Buffer Access with Incorrect Length Value**  
  [https://cwe.mitre.org/data/definitions/805.html](https://cwe.mitre.org/data/definitions/805.html)  

## Description  
Incorrect storage packing in Solidity occurs when storage variables are not efficiently packed within a single storage slot, leading to unnecessary gas consumption. Solidity automatically stores variables in 32-byte (256-bit) slots, and inefficient ordering of data types can lead to wasted space. Contracts that fail to optimize storage packing may incur higher gas costs during deployments and transactions.

## Remediation  
To optimize storage packing:  
- Group smaller data types together (e.g., `uint8`, `bool`) to fit within a single 32-byte slot.  
- Avoid leaving gaps between variables of different sizes.  
- Order state variables efficiently to minimize wasted storage slots.  

### Vulnerable Contract Example  
```solidity
contract InefficientStorage {
    uint256 a;  // Occupies full 32-byte slot
    bool b;     // Occupies another 32-byte slot (wasteful)
    uint8 c;    // Uses a new 32-byte slot instead of sharing
    uint256 d;  // Uses its own slot, leading to extra gas costs
}
```

**Why is this vulnerable?**
- Each variable unnecessarily occupies a separate storage slot, increasing gas costs.
- The `bool` and `uint8` could be packed into the same 32-byte slot, reducing wasted storage space.

### Fixed Contract Example

```solidity
contract OptimizedStorage {
    uint256 a;   // Occupies one full 32-byte slot
    uint256 d;   // Placed next to 'a' to use another full slot
    bool b;      // Packed within the same slot as 'c'
    uint8 c;     // Fits within the same slot as 'b'
}
```
**Why is this safe?**
- `bool` and `uint8` share the same storage slot, reducing unnecessary storage use.
- `uint256` variables are placed together to minimize fragmentation.
- Optimized storage layout leads to lower gas costs for contract execution.

**By correctly ordering state variables and utilizing Solidity’s storage packing rules, developers can significantly reduce gas fees and improve contract efficiency.**