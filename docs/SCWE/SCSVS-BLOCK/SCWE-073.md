---
title: Message Call with Hardcoded Gas Amount
id: SCWE-073
alias: message-call-with-harcoded-gas
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BLOCK]
  scsvs-scg: [SCSVS-BLOCK-1]
  cwe: [400]
status: new
---

## Relationships  
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)  

## Description
In Solidity, calling external contracts with a hardcoded gas value can lead to various issues, such as running out of gas or allowing a malicious contract to manipulate gas consumption. Hardcoding the gas amount is inflexible and may lead to resource exhaustion or cause the transaction to fail when the gas limit is insufficient for the operation.

## Remediation
Instead of hardcoding gas values, it is better to allow the gas to be automatically determined or adjust the gas dynamically depending on the needs of the transaction. This ensures that the transaction can complete successfully while avoiding unnecessary resource consumption.

### Vulnerable Contract Example
```solidity
contract Example {
    address public target;

    function callTarget() public {
        // Hardcoding the gas value for the message call
        target.call{gas: 100000}("");  // Vulnerable to resource consumption issues
    }
}
```

### Fixed Contract Example
```solidity
contract Example {
    address public target;

    function callTarget() public {
        // Let Solidity handle gas consumption dynamically
        target.call("");  // Gas amount handled by the EVM dynamically
    }
}
```