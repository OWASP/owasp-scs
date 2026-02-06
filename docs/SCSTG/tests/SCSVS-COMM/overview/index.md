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

    function forward(address callee, bytes memory _data) public {
        require(callee.delegatecall(_data)); // Unchecked: no validation of callee; delegatecall executes in caller context
    }
}
```
### Impact     

- When external calls fail and their results are unchecked, the contract can proceed under incorrect assumptions, leading to potential loss of funds or other unexpected behaviors.
- Unverified external calls can lead to incorrect updates to the contract state, making it vulnerable to exploits and logical inconsistencies.
- Attackers can manipulate such vulnerabilities to execute malicious code or withdraw funds multiple times.


### Remediation

- For low-level functions like `call`, `delegatecall`, and `staticcall`, always check the return value and handle failures with `require(success, "message")`.
- For ETH transfers, prefer `call{value}("")` with explicit success checks over `transfer()` or `send()` (see SCWE-079); `transfer()` has a 2300 gas stipend and can cause DoS when the recipient is a contract.
- Limit interactions with untrusted contracts and ensure robust validation before performing critical operations.