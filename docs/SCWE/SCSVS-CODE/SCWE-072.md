---
title: Use of Deprecated Solidity Functions
id: SCWE-072
alias: use-of-deprecated-solidity-functions
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [676]
status: new
---

## Relationships  
- CWE-676: Use of a Dangerous Function  
  [https://cwe.mitre.org/data/definitions/676.html](https://cwe.mitre.org/data/definitions/676.html)  

## Description
Some Solidity functions and features have been deprecated over time due to security risks, inefficiencies, or better alternatives being introduced in newer versions of Solidity. Using deprecated functions can expose contracts to known vulnerabilities and potential attacks. Examples include `suicide()`, which was replaced by `selfdestruct()`, and `sha3()`, which was replaced by `keccak256()`.

## Remediation
Always check the Solidity documentation to ensure that the functions you're using are not deprecated. If a function is deprecated, replace it with its recommended alternative to maintain the contract’s security and ensure compatibility with future Solidity versions.

### Vulnerable Contract Example
```solidity
contract Example {
    function oldFunction() public {
        // Using deprecated function `suicide`
        suicide(msg.sender);  // Deprecated, should be replaced with `selfdestruct`
    }
}
```

### Fixed Contract Example
```solidity
contract Example {
    function oldFunction() public {
        // Correctly using the recommended alternative `selfdestruct`
        selfdestruct(payable(msg.sender));  // Replacing deprecated `suicide` with `selfdestruct`
    }
}
```