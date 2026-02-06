---
title: Single-Step Ownership Transfer Without Confirmation
id: SCWE-139
alias: missing-two-step-ownership-transfer
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [670]
status: new
---

## Relationships
- CWE-670: Always-Incorrect Control Flow Implementation  
  [https://cwe.mitre.org/data/definitions/670.html](https://cwe.mitre.org/data/definitions/670.html)

## Description
A single-step `transferOwnership(newOwner)` immediately assigns ownership to the new address. If the wrong address is used (typo, burn address `address(0)`, or a contract that cannot receive ownership), the contract can be permanently locked—no one can perform owner-only actions or correct the mistake. A two-step process (propose → accept) allows the intended recipient to confirm and prevents accidental loss of control.

## Remediation
- Implement a two-step ownership transfer: `transferOwnershipPending(newOwner)` sets a pending owner, and `acceptOwnership()` (callable only by the pending owner) completes the transfer.
- Validate that `newOwner != address(0)` and consider rejecting contract addresses if the owner must be an EOA for operational reasons.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Ownable {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) external {
        require(msg.sender == owner, "Not owner");
        owner = newOwner;  // Single step: typo or address(0) permanently locks contract
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Ownable {
    address public owner;
    address public pendingOwner;

    constructor() {
        owner = msg.sender;
    }

    function transferOwnership(address newOwner) external {
        require(msg.sender == owner, "Not owner");
        require(newOwner != address(0), "Zero address");
        pendingOwner = newOwner;
    }

    function acceptOwnership() external {
        require(msg.sender == pendingOwner, "Not pending owner");
        owner = pendingOwner;
        delete pendingOwner;
    }
}
```
