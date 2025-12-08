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
Using block values (such as `block.timestamp`, `block.number`, or `block.difficulty`) as a proxy for time in Ethereum smart contracts can be problematic. Block values are determined by miners and can be manipulated within certain limits, making them unreliable for time-sensitive logic. Relying on these values for critical decisions like deadlines or expiration dates can result in unexpected behaviors, such as manipulations by miners or unintended contract states.

## Remediation
To mitigate this vulnerability, avoid using block values as a direct proxy for time-based logic. Instead, consider using external oracles that provide reliable and tamper-proof time data or incorporate additional checks to prevent miner manipulation. Where necessary, combine block values with other data points to reduce the risk of exploitation.

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
contract TimeSensitive {
    uint public deadline;
    address public oracle;

    constructor(uint _deadline, address _oracle) {
        deadline = _deadline;
        oracle = _oracle;
    }

    function hasExpired() public view returns (bool) {
        // Use a trusted oracle for time verification
        uint currentTime = Oracle(oracle).getCurrentTime();
        return currentTime > deadline;
    }
}
```