---
title: Unbounded Withdrawal Queue Growth
id: SCWE-126
alias: unbounded-withdrawal-queue
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-2]
  cwe: [400]
status: new
---

## Relationships
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)

## Description
Protocols that queue withdrawals without bounding length or processing batches can face gas exhaustion when executing large queues. Attackers can spam small requests to DoS withdrawal execution or force users to accept delays.

## Remediation
- Cap queue size or use batched/paged processing with upper gas limits.
- Charge fees or require minimum amounts to discourage spam.
- Allow users to cancel/claim in smaller chunks rather than processing the entire queue at once.

## Examples

### Vulnerable
```solidity
function processAll() external {
    for (uint256 i = 0; i < queue.length; i++) {
        _pay(queue[i]);
    }
}
```

### Fixed
```solidity
function processBatch(uint256 start, uint256 max) external {
    uint256 end = start + max;
    if (end > queue.length) end = queue.length;
    for (uint256 i = start; i < end; i++) {
        _pay(queue[i]);
    }
}
```

