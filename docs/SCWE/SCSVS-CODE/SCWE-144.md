---
title: Bypassable Contract Existence Check via extcodesize
id: SCWE-144
alias: unsafe-extcodesize-contract-check
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [697]
status: new
---

## Relationships
- CWE-697: Incorrect Comparison  
  [https://cwe.mitre.org/data/definitions/697.html](https://cwe.mitre.org/data/definitions/697.html)

## Description
Using `extcodesize(addr) > 0` to detect whether an address is a contract fails during construction. When code runs inside a constructor, `extcodesize(address(this))` returns 0 because the contract's code is not yet deployed. An attacker can deploy a contract whose constructor calls the victim—the victim sees `extcodesize(caller) == 0` and treats the caller as an EOA, bypassing contract-specific restrictions.

## Remediation
- Do not rely on `extcodesize` to distinguish EOAs from contracts.
- If contract-only or EOA-only logic is required, use a different mechanism (e.g., trusted registry, explicit opt-in) or accept that constructor calls cannot be distinguished.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract TokenGating {
    mapping(address => bool) public allowed;

    function claim() external {
        require(extcodesize(msg.sender) == 0, "Contracts not allowed");
        allowed[msg.sender] = true;
    }

    function extcodesize(address account) internal view returns (uint256 size) {
        assembly { size := extcodesize(account) }
    }
}
```
**Why vulnerable:** An attacker deploys `Attacker` whose constructor calls `claim()`. During the constructor, `extcodesize(Attacker) == 0`, so the check passes and the contract receives the claim.

### Fixed
```solidity
pragma solidity ^0.8.0;

contract TokenGating {
    mapping(address => bool) public allowed;
    mapping(address => bool) public claimed;

    function claim() external {
        require(allowed[msg.sender], "Not allowed");
        require(!claimed[msg.sender], "Already claimed");
        claimed[msg.sender] = true;
    }
}
```
**Fix:** Use an allowlist instead of `extcodesize`. Access control is based on explicit registration, not EOA vs contract detection.
