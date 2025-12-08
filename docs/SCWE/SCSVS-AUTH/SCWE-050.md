---
title: Unprotected SELFDESTRUCT Instruction
id: SCWE-050
alias: unprotected-selfdestruct
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-2]
  cwe: [732]
status: new
---

## Relationships  
- CWE-732: Incorrect Permission Assignment for Critical Resource  
  [https://cwe.mitre.org/data/definitions/732.html](https://cwe.mitre.org/data/definitions/732.html)  

## Description
The `SELFDESTRUCT` instruction in Ethereum allows a contract to destroy itself and send its remaining Ether balance to a specified address. If this instruction is not properly protected with access controls, an attacker could trigger it, causing the contract to self-destruct and possibly transferring all the funds to an unauthorized address. This can result in the total loss of funds or disruption of contract functionality.

## Remediation
To mitigate this vulnerability, it is crucial to protect the `SELFDESTRUCT` instruction with proper access control mechanisms. Only authorized users, such as the contract owner or admin, should be allowed to call the `SELFDESTRUCT` function. Consider using modifiers like `onlyOwner` or a role-based access control system to enforce permission checks before allowing this critical operation.

### Vulnerable Contract Example
```solidity
contract Destructible {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    // Unprotected SELFDESTRUCT allowing anyone to call it
    function destruct() public {
        selfdestruct(payable(msg.sender));  // No access control
    }
}
```

### Fixed Contract Example
```solidity
contract Destructible {
    address public owner;
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    // Only the owner can call SELFDESTRUCT
    function destruct() public onlyOwner {
        selfdestruct(payable(msg.sender));  // Access control added
    }
}
```
