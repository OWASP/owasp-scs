---
title: Missing Disable Initializer in Constructor for Proxy Contracts
id: SCWE-092
alias: Missing-Disable-Initializer-in-Constructor-for-Proxy-Contracts
platform: []
profiles: [L1, L2]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [665]
status: new
---

## Relationships
- **CWE-665**: [Improper Initialization](https://cwe.mitre.org/data/definitions/665.html)

## Description
This weakness occurs when upgradeable proxy contracts (e.g., UUPS or Transparent Proxy patterns) do not include a call to `_disableInitializers()` inside their constructor. Without this safeguard, malicious actors may invoke the `initialize()` function directly on the implementation contract. This can lead to takeover of admin roles, unauthorized ownership assignment, or malicious configuration of protocol-critical parameters.  

This mistake is frequently observed in contracts built with OpenZeppelin Upgradeable libraries where developers forget to disable initializers in the implementation contract’s constructor.  

## Impact
Failure to disable initializers in proxy contracts is a recurring and high-severity weakness. It enables attackers to:  
- Become the owner/admin of an uninitialized logic contract.  
- Hijack upgradeability or governance control.  
- Set malicious parameters (fees, treasury addresses, token supply logic, etc.).  

This weakness has caused multiple security incidents in production DeFi and NFT projects where attackers initialized orphaned implementation contracts and drained funds.  

Its importance stems from:  
- Widespread use of upgradeable contracts in DeFi and DAOs.  
- Frequent developer oversight when using proxy patterns.  
- High impact — loss of protocol ownership, funds, and governance control.  

## Remediation
- Always call `_disableInitializers()` in the constructor of implementation contracts.  
- Review all upgradeable contracts to ensure the implementation cannot be directly initialized.  
- Use OpenZeppelin’s recommended pattern and annotations (e.g., `@custom:oz-upgrades-unsafe-allow constructor`) when disabling initializers.  

## Examples

- **❌ Vulnerable Code**
```solidity
// Implementation contract for a UUPS Proxy
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract Vault is Initializable {
    address public owner;

    function initialize(address _owner) public initializer {
        owner = _owner;
    }
}
```

⚠️ Issue:  
- The constructor does not call `_disableInitializers()`.  
- Attackers can directly call `initialize()` on the implementation contract (not through the proxy) and take over ownership.  

- **✅ Safe Code**
```solidity
// Secure implementation contract for a UUPS Proxy
pragma solidity ^0.8.20;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract Vault is Initializable {
    address public owner;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers(); // Prevents initialize() from being called on implementation
    }

    function initialize(address _owner) public initializer {
        owner = _owner;
    }
}
```

✅ Fix:  
- Adding `_disableInitializers()` in the constructor ensures the logic (implementation) contract cannot be initialized directly.  
- Only the proxy can call `initialize()` safely during deployment.  
