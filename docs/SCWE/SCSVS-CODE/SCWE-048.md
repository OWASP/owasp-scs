---
title: Unchecked Call Return Value
id: SCWE-048
alias: unchecked-call
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [390]
status: new
---

## Relationships
- CWE-252: Unchecked Return Value
  [https://cwe.mitre.org/data/definitions/252.html](https://cwe.mitre.org/data/definitions/252.html)
- CWE-390: Detection of Error Condition Without Action
  [https://cwe.mitre.org/data/definitions/390.html](https://cwe.mitre.org/data/definitions/390.html)

## Description
Unchecked call return value vulnerabilities occur when a contract fails to validate the success or failure of low-level calls, such as `call`, `delegatecall`, and `staticcall`. Ignoring the return values of these calls can result in undetected errors, allowing malicious or unintended actions to succeed silently.

## Remediation
- **Check return values:** Always verify the success of low-level calls.  
- **Use higher-level abstractions:** Prefer method calls or, if you are confident that 2300 gas are sufficient for the recipient to handle the transfer, `transfer` over `call`, as they revert on failure. 

## Examples

### Vulnerable Contract Example

```solidity
pragma solidity ^0.8.0;

contract UncheckedCall {
    function sendEther(address _recipient) public payable {
        _recipient.call{value: msg.value}(""); // Unchecked call, no error handling
    }
}
```
### Fixed Contract Example

```solidity
pragma solidity ^0.8.0;

contract CheckedCall {
    function sendEther(address payable _recipient) public payable {
        (bool success, ) = _recipient.call{value: msg.value}("");
        require(success, "Transfer failed");
    }
}
```
