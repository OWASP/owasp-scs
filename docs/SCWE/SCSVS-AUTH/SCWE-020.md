---
title: Absence of Time-Locked Functions
id: SCWE-020
alias: absence-time-locked-functions
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-2]
  cwe: [840]
status: new
---

## Relationships
- CWE-840: Business Logic Errors
  [https://cwe.mitre.org/data/definitions/840.html](https://cwe.mitre.org/data/definitions/840.html)

## Description
Absence of time-locked functions occurs when smart contracts do not implement mechanisms to delay certain critical functions or actions based on time conditions. This can result in the contract allowing actions that should be restricted or postponed for a certain period, such as emergency fund withdrawals or sensitive administrative actions. Without time-locking mechanisms, malicious actors or faulty logic could trigger these actions at the wrong time, leading to undesired outcomes.

Time-locking is commonly used in scenarios like:
- Delaying admin or owner functions to prevent immediate misuse.
- Ensuring withdrawal or fund transfer happens only after a predefined delay.
- Enabling emergency actions only after a certain time or under specific conditions.

## Remediation
- **Implement time-locked functions:** Ensure that critical functions, especially those related to fund transfers or administrative actions, are protected by a time lock, delaying their execution until an appropriate time has passed.
- **Use block timestamps:** Leverage block timestamps or block numbers to control the execution of functions.
- **Limit emergency access:** If implementing emergency mechanisms, ensure that there are time delays before they can be invoked, to reduce the chance of misuse.
- **Review time-based logic regularly:** Verify the correctness of time-based logic to ensure that the system behaves as intended.

## Examples

### Absence of Time-Locked Function

```solidity
pragma solidity ^0.8.0;

contract NoTimeLock {
    address public owner;
    uint public funds;

    constructor() public {
        owner = msg.sender;
        funds = 1000;
    }

    // Critical function without time-lock
    function withdrawFunds(uint amount) public {
        require(msg.sender == owner, "Not the owner");
        funds -= amount;
    }
}
```
In this example, the contract lacks any time-lock mechanism, allowing the owner to withdraw funds at any time, which could be dangerous if mishandled. 

### Time-Locked Function Implementation
```solidity
pragma solidity ^0.8.0;

contract TimeLockExample {
    address public owner;
    uint public funds;
    uint public lastWithdrawalTime;
    uint public withdrawalDelay = 1 weeks;

    constructor() public {
        owner = msg.sender;
        funds = 1000;
        lastWithdrawalTime = now;
    }

    // Critical function with time-lock
    function withdrawFunds(uint amount) public {
        require(msg.sender == owner, "Not the owner");
        require(now >= lastWithdrawalTime + withdrawalDelay, "Time lock not expired");
        
        lastWithdrawalTime = now;
        funds -= amount;
    }
}
```
In the fixed version, a time-lock mechanism is implemented, ensuring that the owner can only withdraw funds after a certain delay (e.g., one week). This provides an added layer of security, particularly in cases where emergency withdrawals or administrative actions are necessary but should not be immediate.