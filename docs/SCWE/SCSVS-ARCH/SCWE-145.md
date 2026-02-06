---
title: Unvalidated Constructor Parameters
id: SCWE-145
alias: missing-constructor-input-validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Constructors that accept critical parameters (owner, oracle, fee recipient, token addresses) without validation can deploy a contract in a broken or insecure state. Zero addresses, invalid values, or inconsistent configuration (e.g., fee > 100%) may be impossible to fix after deployment if there is no setter or upgrade path.

## Remediation
- Validate all constructor parameters: zero address checks, range checks (e.g., fee <= 100%), and consistency checks.
- Use `require` or custom errors to revert deployment with a clear message when validation fails.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Staking {
    address public owner;
    address public rewardToken;
    uint256 public feeBps;

    constructor(address _owner, address _rewardToken, uint256 _feeBps) {
        owner = _owner;           // No validation
        rewardToken = _rewardToken;
        feeBps = _feeBps;         // Could be > 10000
    }
}
```

### Fixed
```solidity
constructor(address _owner, address _rewardToken, uint256 _feeBps) {
    require(_owner != address(0), "Invalid owner");
    require(_rewardToken != address(0), "Invalid token");
    require(_feeBps <= 10000, "Fee too high");
    owner = _owner;
    rewardToken = _rewardToken;
    feeBps = _feeBps;
}
```
