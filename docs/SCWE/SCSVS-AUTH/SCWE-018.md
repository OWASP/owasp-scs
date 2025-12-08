---
title: Use of tx.origin for Authorization
id: SCWE-018
alias: use-of-tx-origin-for-authorization
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [346]
status: new
---

## Relationships
- **CWE-346**: Origin Validation Error  
  [https://cwe.mitre.org/data/definitions/346.html](https://cwe.mitre.org/data/definitions/346.html)

## Description
The use of `tx.origin` for authorization is a security vulnerability in which a smart contract checks the origin of the transaction to determine if a user is authorized to perform an action. This approach is flawed because `tx.origin` can be exploited by an attacker through a chain of transactions, allowing unauthorized users to interact with the contract. An attacker could trick the contract into performing an action on behalf of the victim by utilizing another contract in the transaction chain.

**Key Issues**:
- Allows unauthorized transactions by using the `tx.origin` variable instead of `msg.sender`.
- Vulnerable to phishing and reentrancy attacks, where attackers can use contracts to impersonate the victim.
- Mismanagement of roles and improper transaction flow handling.

## Remediation
- **Use `msg.sender` instead of `tx.origin`**: Always rely on `msg.sender` for authentication and authorization, as it correctly represents the immediate sender of the current call.
- **Strict validation checks**: Ensure that authorization checks are done on the direct sender of the transaction, i.e., `msg.sender`, and not the originator.

## Examples

### Vulnerable Contract (Using `tx.origin` for Authorization)
```solidity
pragma solidity ^0.8.0;

contract Vulnerable {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function restrictedAction() public {
        require(tx.origin == owner, "Only the owner can perform this action");
        // Action code here
    }
}
```
In the vulnerable contract, the authorization check uses `tx.origin` to validate the caller. This is a problem because if the contract is called via another contract, `tx.origin` will return the original transaction sender (not the immediate caller), which opens up the contract to attacks such as phishing. The attacker can create a contract that interacts with the vulnerable contract on behalf of the victim.



### Fixed Contract (Using msg.sender for Authorization)
```solidity
pragma solidity ^0.8.0;

contract Secure {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    function restrictedAction() public {
        require(msg.sender == owner, "Only the owner can perform this action");
        // Action code here
    }
}

```
In the fixed contract, `msg.sender` is used instead of `tx.origin`. This ensures that the contract checks the immediate sender of the call, which prevents attacks where malicious contracts impersonate the victim.
