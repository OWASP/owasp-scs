---
title: Reentrancy Attacks
id: SCWE-046
alias: reentrancy-attacks
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [367]
status: new
---

## Relationships
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition  
  [https://cwe.mitre.org/data/definitions/367.html](https://cwe.mitre.org/data/definitions/367.html)

## Description
Reentrancy attacks occur when a contract allows untrusted external calls during execution without properly updating state variables or implementing protections. This enables attackers to repeatedly call functions and manipulate the contract’s state before execution completes. Common issues include:

- Making external calls before updating state variables.  
- Lack of mechanisms to prevent repeated or recursive calls.  
- Improper handling of external interactions. 

## Remediation
- **Update state first:** Modify critical state variables before any external calls.  
- **Implement reentrancy guards:** Use tools like `nonReentrant` modifiers to block recursive calls. 

## Examples

### Vulnerable Contract Example (Reentrancy)

```solidity
pragma solidity ^0.4.0;

contract Vulnerable {
    mapping(address => uint) public balances;

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount);
        msg.sender.call.value(_amount)(); // Vulnerable external call
        balances[msg.sender] -= _amount;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}
```

### Fixed Contract Example

```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract Secure is ReentrancyGuard {
    mapping(address => uint) public balances;

    function withdraw(uint _amount) public nonReentrant {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        balances[msg.sender] -= _amount;
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
}
```