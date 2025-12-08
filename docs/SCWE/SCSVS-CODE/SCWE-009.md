---
title: Deprecated Variable and Function Usage
id: SCWE-009
alias: deprecated-usage
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [477]
status: new
---

## Relationships
- CWE-477: Use of Obsolete Function
  [https://cwe.mitre.org/data/definitions/477.html](https://cwe.mitre.org/data/definitions/477.html)

## Description
The use of deprecated variables and functions refers to employing code elements that are no longer recommended for use, either due to obsolescence, security concerns, or the introduction of better alternatives. Using such elements can cause issues, including reduced compatibility, poor maintainability, and security vulnerabilities. Specific concerns related to deprecated usage are:

- **Security risks**: Deprecated functions may have known vulnerabilities or might not be patched.
- **Compatibility issues**: Newer compiler versions and environments may not support deprecated code.
- **Maintenance difficulties**: Continuing to use deprecated code increases the complexity of codebase management and prevents clean upgrades.

## Remediation
- **Replace deprecated functions**: Always use the recommended and supported alternatives in the latest compiler versions.
- **Update dependencies**: If relying on libraries that use deprecated elements, upgrade to versions that support current standards.
- **Monitor for deprecation warnings**: Stay informed about deprecated functions in the Solidity language or external libraries and refactor the code when necessary.

## Examples

### Contract with Deprecated Function Usage

```solidity
pragma solidity ^0.4.0;

contract DeprecatedUsage {
    address public owner;
    uint public balance;

    // Deprecated function, example using older Solidity versions
    function sendTransaction(address recipient, uint amount) public {
        recipient.transfer(amount);
    }
}
```

In this example, the `transfer` function in Solidity's older versions is deprecated. Continuing to use such functions can cause issues with future compiler versions.

### Improved Contract without Deprecated Usage

```solidity
pragma solidity ^0.8.0;

contract UpdatedUsage {
    address public owner;
    uint public balance;

    // Replaced with safer, modern methods
    function sendTransaction(address recipient, uint amount) public {
        payable(recipient).transfer(amount);
    }
}
```
In this improved example, the contract uses the latest version of Solidity (0.8.0), which has better support and security features. The `transfer` method is also updated to be more compatible with the latest Solidity practices.