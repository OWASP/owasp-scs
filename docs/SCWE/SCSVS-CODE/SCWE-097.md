---
title: Missing Explicit Function Visibility
id: SCWE-097
alias: function-default-visibility
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [284]
status: new
---

## Relationships
- CWE-284: Improper Access Control  
  [https://cwe.mitre.org/data/definitions/284.html](https://cwe.mitre.org/data/definitions/284.html)

## Description
When a function’s visibility is omitted in Solidity, it defaults to `public`, allowing any caller to invoke logic that may have been intended to be internal or private. This expands the attack surface, enabling unauthorized state changes, fund movements, or reentrancy entry points.

## Remediation
- Explicitly declare visibility (`private`, `internal`, `public`, `external`) on every function.
- Use linters/static analysis to enforce visibility declarations.
- Restrict privileged logic with proper access modifiers and role checks.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Vault {
    uint256 public balance;

    function withdraw(uint256 amount) { // defaults to public
        balance -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Vault {
    uint256 public balance;

    function withdraw(uint256 amount) external {
        // add proper access control or business checks here
        balance -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

