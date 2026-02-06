---
title: Missing Timelock on Privileged Operations
id: SCWE-100
alias: missing-timelock
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [284]
status: new
---

## Relationships
- CWE-284: Improper Access Control  
  [https://cwe.mitre.org/data/definitions/284.html](https://cwe.mitre.org/data/definitions/284.html)

## Description
Without a timelock on privileged actions (upgrades, parameter changes, pausing), a compromised or malicious admin can instantly deploy hostile logic or drain funds. Users and validators have no window to react, audit, or exit.

## Remediation
- Gate all privileged operations behind a timelock contract with queue, minimum delay, and cancellation.
- Emit events on queue/execute/cancel to provide monitoring transparency.
- Use multi-sig or role separation so a single key cannot bypass the delay.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Gov {
    address public owner;
    address public implementation;

    constructor() { owner = msg.sender; }

    function upgrade(address impl) external {
        require(msg.sender == owner, "not owner");
        implementation = impl; // executes immediately
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract TimelockGov {
    struct Action { address impl; uint256 eta; }
    Action public queued;
    address public owner;
    uint256 public constant DELAY = 2 days;

    constructor() { owner = msg.sender; }

    function queueUpgrade(address impl) external {
        require(msg.sender == owner, "not owner");
        queued = Action({impl: impl, eta: block.timestamp + DELAY});
    }

    function executeUpgrade() external {
        require(block.timestamp >= queued.eta, "too early");
        implementation = queued.impl;
    }
}
```

