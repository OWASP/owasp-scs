---
title: Unprotected Ether Withdrawal
id: SCWE-049
alias: unprotected-ether-withdrawal
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
Unprotected Ether withdrawal occurs when a smart contract allows withdrawal of Ether (ETH) without sufficient access control or proper authorization mechanisms. This vulnerability exposes the contract to unauthorized or malicious users, enabling them to drain funds without any checks on the withdrawal request.

## Remediation
To prevent this vulnerability, implement strong access control mechanisms like the `onlyOwner` modifier or a more flexible role-based access control (RBAC) system. Ensure that only authorized users (e.g., the contract owner or specific users) can initiate Ether withdrawals. Always verify user permissions before allowing access to critical contract functions.

## Impact
An attacker can exploit this vulnerability to withdraw Ether from the contract, leading to potential financial loss. This could result in a total loss of funds if no protective measures are in place, exposing the contract and its users to significant risks.

### Vulnerable Contract Example

```solidity
contract EtherWallet {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function withdraw(uint amount) public {
        payable(msg.sender).transfer(amount);  // No access control
    }
}
```

### Fixed Contract Example

```solidity
contract EtherWallet {
    address public owner;
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    function withdraw(uint amount) public onlyOwner {
        payable(msg.sender).transfer(amount);  // Access control added
    }
}
```