---
title: Single Point of Failure in Administrative Key Management
id: SCWE-155
alias: centralization-risk-single-admin-key
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [284]
status: new
---

## Relationships
- CWE-284: Improper Access Control  
  [https://cwe.mitre.org/data/definitions/284.html](https://cwe.mitre.org/data/definitions/284.html)

## Description
Contracts that rely on a single administrative key (EOA or contract) without multisig, timelock, or key rotation create a single point of failure. Compromise of that key (phishing, malware, physical theft) gives full control; loss of the key (e.g., no backup) can permanently lock critical functions. SCWE-129 covers single EOA admin; this weakness focuses on the *risk* of single-key design and the absence of mitigations.

## Remediation
- Use multisig wallets (e.g., Gnosis Safe) for administrative actions.
- Implement timelocks for sensitive operations (SCWE-020).
- Plan for key rotation or recovery mechanisms.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Treasury {
    address public owner;

    function withdraw(uint256 amount) external {
        require(msg.sender == owner, "Not owner");
        (bool ok, ) = owner.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Risk:** Single `owner` key; no multisig, no timelock. Compromise or loss permanently affects the treasury.

### Fixed
```solidity
contract Treasury {
    address public owner;  // In production: use multisig (e.g., Gnosis Safe)
    uint256 public constant TIMELOCK = 2 days;
    uint256 public pendingAmount;
    uint256 public unlockTime;

    function proposeWithdraw(uint256 amount) external {
        require(msg.sender == owner, "Not owner");
        pendingAmount = amount;
        unlockTime = block.timestamp + TIMELOCK;
    }

    function executeWithdraw() external {
        require(msg.sender == owner, "Not owner");
        require(block.timestamp >= unlockTime, "Timelock");
        uint256 amount = pendingAmount;
        pendingAmount = 0;
        (bool ok, ) = owner.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Fix:** Timelock adds a delay so large withdrawals can be contested. Use a multisig for `owner` in production.
