---
title: Insecure Use of Transfer and Send
id: SCWE-079
alias: insecure-use-of-transfer-send
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [400]
status: new
---

## Relationships  
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)  

## Description
The use of `.transfer()` and` .send() `for Ether transfers in Solidity is insecure because they impose a fixed gas limit of 2300 gas. This restriction can cause transactions to fail unexpectedly when the receiving contract has complex logic that requires more gas. Additionally, it can result in a Denial of Service (DoS) vulnerability if the receiving contract cannot execute due to insufficient gas.

This issue is especially problematic in upgradable smart contracts or protocol interactions, where the gas requirements of a receiving contract might change over time.


## Remediation
Instead of `.transfer()` and `.send()`, use `.call{value: msg.value}("")`, which allows more flexible gas allocation and prevents DoS risks. Always check for the return value of `.call()` to ensure the transfer was successful.


### Vulnerable Contract Example
```solidity
contract Example {
    function transferEther(address payable _to) public payable {
        // Fixed gas limit of 2300 gas can cause unintended failures
        _to.transfer(msg.value);  
    }
}
```
**Problem**:
- If `_to` is a contract that requires more than `2300 gas` (e.g., it has a fallback function with state changes), this transfer will fail.
- The contract has no error handling, meaning the sender won't be aware of the failure.


### Fixed Contract Example
```solidity
contract Example {
    function transferEther(address payable _to) public payable {
        // Use call() for better gas flexibility and proper error handling
        (bool success, ) = _to.call{value: msg.value}("");
        require(success, "Transfer failed");
    }
}
```
**Why is this better?**
- `.call{value: msg.value}("")` does not impose a gas limit, allowing the receiving contract to execute as needed.
- It includes a `require(success, "Transfer failed");` check, ensuring failures are properly handled.