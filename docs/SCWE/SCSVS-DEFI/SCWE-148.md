---
title: Gas Exhaustion via Unbounded Loops with External Calls
id: SCWE-148
alias: unbounded-external-call-loops
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-1]
  cwe: [400]
status: new
---

## Relationships
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)

## Description
Loops that iterate over user-controlled arrays and perform external calls (transfers, approvals, or other contract calls) in each iteration can exhaust gas when the array is large. Each external call consumes gas; unbounded loops cause the transaction to hit the block gas limit and revert, resulting in denial of service. SCWE-109 covers unbounded loops generally; this weakness focuses on loops that perform external calls.

## Remediation
- Impose an upper bound on loop iterations or batch size.
- Use pull-based patterns: let users claim individually instead of pushing to many addresses in one tx.
- Process in chunks with pagination or checkpoints.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Airdrop {
    function distribute(address[] calldata recipients, uint256 amount) external {
        for (uint256 i = 0; i < recipients.length; i++) {
            (bool ok, ) = recipients[i].call{value: amount}("");
            require(ok, "Transfer failed");
        }
    }
}
```
**Why vulnerable:** Large `recipients.length` causes out-of-gas; one failed transfer reverts the entire batch.

### Fixed
```solidity
uint256 public constant MAX_BATCH = 100;

function distribute(address[] calldata recipients, uint256 amount) external {
    require(recipients.length <= MAX_BATCH, "Batch too large");
    for (uint256 i = 0; i < recipients.length; i++) {
        (bool ok, ) = recipients[i].call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
