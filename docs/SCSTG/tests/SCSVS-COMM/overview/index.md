---
title: Unchecked External Calls in Smart Contracts
---
### **Description**

Unchecked external calls occur when a smart contract makes an external call to another contract or address without verifying the call's outcome. In Ethereum, external calls may fail silently, and the calling contract may mistakenly proceed as if the call succeeded. This leads to state inconsistencies and potential exploitation. The issue is particularly risky in functions like delegatecall, send, or call, where the outcome must be explicitly checked.

**Example: Code Without Proper Access Control**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.4.24;

contract Proxy {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function forward(address callee, bytes _data) public {
        require(callee.delegatecall(_data)); // Unchecked external call vulnerability
    }
}
```
### Impact     

- When external calls fail and their results are unchecked, the contract can proceed under incorrect assumptions, leading to potential loss of funds or other unexpected behaviors.
- Unverified external calls can lead to incorrect updates to the contract state, making it vulnerable to exploits and logical inconsistencies.
- Attackers can manipulate such vulnerabilities to execute malicious code or withdraw funds multiple times.


### Remediation


- Use safer methods such as transfer() over send() when transferring Ether. The transfer() function reverts automatically if the call fails.
- For low-level functions like call and delegatecall, always check the return value and handle failures appropriately.
- Limit interactions with untrusted contracts and ensure robust validation before performing critical operations.