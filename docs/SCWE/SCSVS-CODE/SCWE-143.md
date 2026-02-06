---
title: Critical Address Parameters Not Validated for Zero Address
id: SCWE-143
alias: missing-zero-address-validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)

## Description
Critical address parameters (owner, oracle, fee recipient, token address) that are not validated for `address(0)` can brick the contract or cause funds to be sent to the burn address. Assigning `address(0)` as owner prevents any owner-only actions; using it as a recipient loses funds permanently. SCWE-091 covers zero *value* in token transfers; this weakness addresses zero *address*.

## Remediation
- Validate `require(addr != address(0), "Zero address")` for all critical address parameters in constructors and setters.
- Use custom errors for gas efficiency where appropriate.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Vault {
    address public owner;
    address public feeRecipient;

    constructor(address _owner, address _feeRecipient) {
        owner = _owner;           // No check: address(0) bricks contract
        feeRecipient = _feeRecipient;  // No check: fees sent to burn address
    }

    function collectFees() external {
        uint256 fees = address(this).balance;
        (bool ok, ) = feeRecipient.call{value: fees}("");
        require(ok, "Transfer failed");
    }
}
```

### Fixed
```solidity
constructor(address _owner, address _feeRecipient) {
    require(_owner != address(0), "Invalid owner");
    require(_feeRecipient != address(0), "Invalid fee recipient");
    owner = _owner;
    feeRecipient = _feeRecipient;
}
```
