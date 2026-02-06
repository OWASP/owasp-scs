---
title: Block Values as a Proxy for Time
id: SCWE-065
alias: block-values-as-proxy-for-time
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BLOCK]
  scsvs-scg: [SCSVS-BLOCK-2]
  cwe: [20]
status: new
---

## Relationships  
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)  

## Description
Using block values (such as `block.timestamp`, `block.number`, or `block.difficulty` / `block.prevrandao` post-merge) as a proxy for time in Ethereum smart contracts can be problematic. Block values are determined by validators (or miners on PoW chains) and can be manipulated within certain limits, making them unreliable for time-sensitive logic. Relying on these values for critical decisions like deadlines or expiration dates can result in unexpected behaviors, such as manipulations by validators (or miners on PoW chains) or unintended contract states.

## Remediation
To mitigate this vulnerability, account for the manipulation bounds of block values. `block.timestamp` can vary by ~15 seconds per block; design deadlines and time checks with this tolerance in mind. Time oracles are uncommon; the standard approach is to use `block.timestamp` with appropriate buffers. Where precision is critical, consider commit-reveal or multi-block confirmation.

### Vulnerable Contract Example
```solidity
contract TimeSensitive {
    uint public deadline;

    constructor(uint _deadline) {
        deadline = _deadline;
    }

    function hasExpired() public view returns (bool) {
        return block.timestamp > deadline;  // Relies on block.timestamp
    }
}
```

### Fixed Contract Example
```solidity
pragma solidity ^0.8.0;

contract TimeSensitive {
    uint public constant DEADLINE_BUFFER = 15; // seconds — accounts for block.timestamp manipulation
    uint public deadline;

    constructor(uint _deadline) {
        // Set deadline with buffer so expiry is robust to ~15s timestamp variance
        deadline = _deadline + DEADLINE_BUFFER;
    }

    function hasExpired() public view returns (bool) {
        return block.timestamp > deadline;
    }
}
```
**Mitigation:** Add a buffer when setting deadlines to account for the ~15 second manipulation window of `block.timestamp`. Avoid relying on sub-minute precision.