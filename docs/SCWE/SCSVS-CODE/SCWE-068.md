---
title: State Variable Default Visibility
id: SCWE-068
alias: state-variable-default-visibility
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [704]
status: new
---

## Relationships  
- CWE-704: Incorrect Type Conversion or Cast  
  [https://cwe.mitre.org/data/definitions/704.html](https://cwe.mitre.org/data/definitions/704.html)  


## Description
In Solidity, state variables have a default visibility of `internal`, which means they can only be accessed within the contract or derived contracts (not by external callers). Omitting explicit visibility can lead to unintended behavior: for example, if a developer intends `private` but forgets to specify it, derived contracts can still access the variable; if they intend `public` but omit it, no getter is generated and external callers cannot read the value. Explicit visibility ensures the variable behaves as intended.

## Remediation
Always explicitly specify the visibility of state variables. The possible visibility options are:
- `public`: Accessible by anyone, both externally and internally.
- `internal`: Accessible only within the contract or derived contracts (default).
- `private`: Accessible only within the contract.

### Vulnerable Contract Example
```solidity
contract Vulnerable {
    uint balance;  // Default internal; no getter — external callers cannot read it

    constructor() {
        balance = 100;
    }

    function updateBalance(uint amount) public {
        balance = amount;  // Intended public? Forgot visibility — no automatic getter
    }
}
```

### Fixed Contract Example
```solidity
contract Secure {
    uint private balance;  // Explicitly set visibility to private

    constructor() {
        balance = 100;
    }

    function updateBalance(uint amount) public {
        balance = amount;  // No external access to the variable
    }
}
```