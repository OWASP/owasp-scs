---
title: Floating Pragma
id: SCWE-060
alias: floating-pragma
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [703]
status: new
---

## Relationships  
- CWE-703: Improper Check for Unusual or Exceptional Conditions  
  [https://cwe.mitre.org/data/definitions/703.html](https://cwe.mitre.org/data/definitions/703.html)  

## Description
The use of floating pramas (e.g., `^0.8.0`) in smart contract development can lead to unexpected issues when new versions of the Solidity compiler are released. Floating versions allow the contract to automatically use newer versions of the compiler within the specified range, which may introduce breaking changes, unexpected bugs, or security vulnerabilities. To avoid this, it is important to specify fixed versions to ensure the contract works reliably and consistently across different environments.

## Remediation
To mitigate this vulnerability, always specify a fixed compiler version in the contract to avoid using floating pramas. This ensures that the contract is compiled using a known and tested version of the compiler, preventing unexpected behavior from new, untested releases.

### Vulnerable Contract Example
```solidity
pragma solidity ^0.8.0;  // Floating version allows for any 0.8.x version

contract Vulnerable {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}
```

### Fixed Contract Example
```solidity
pragma solidity 0.8.4;  // Fixed version ensures no unexpected updates

contract Fixed {
    uint public value;

    function setValue(uint _value) public {
        value = _value;
    }
}
```