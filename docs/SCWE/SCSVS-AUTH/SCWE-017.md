---
title: Privileged Role Mismanagement
id: SCWE-017
alias: privileged-role-mismanagement
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-1]
  cwe: [269]
status: new
---

## Relationships
- CWE-269: Improper Privilege Management  
  [https://cwe.mitre.org/data/definitions/269.html](https://cwe.mitre.org/data/definitions/269.html)

## Description
Privileged role mismanagement occurs when a smart contract incorrectly assigns roles or permissions, granting excessive privileges to certain users. This can lead to users obtaining permissions beyond what is necessary for their intended function, creating a potential for privilege escalation or unauthorized actions. In the context of smart contracts, improper privilege management can lead to critical vulnerabilities such as unauthorized contract changes, malicious interactions, or loss of funds.

Common causes include:
- Insufficient checks for users attempting to access privileged functions.
- Roles being dynamically assigned without validation.
- Inadequate access control mechanisms for sensitive contract functions.

## Remediation
- **Role-based access control (RBAC):** Implement strict role checks using modifiers to ensure that users can only perform actions that correspond to their assigned roles.
- **Principle of least privilege:** Limit the privileges of each role to the bare minimum needed to perform their task.
- **Use of trusted or immutable sources:** Ensure that privileged roles cannot be arbitrarily changed by unauthorized users or during attacks.
- **Periodic reviews and audits:** Regularly review roles and permissions to ensure they are correctly assigned and maintained.

## Examples

### Privileged Role Mismanagement Example

```solidity
pragma solidity ^0.8.0;

contract PrivilegedRoleMismanagement {
    address public admin;
    uint public balance;

    function setAdmin(address _admin) public {
        admin = _admin;
    }

    function withdraw(uint amount) public {
        require(msg.sender == admin, "Only admin can withdraw");
        balance -= amount;
    }
}
```

In the above example, there is no check for the address assigning the `admin` role, and it can be changed by anyone, including malicious actors.

### Fixed Privileged Role Management
```solidity
pragma solidity ^0.8.0;

contract FixedRoleManagement {
    address public owner;
    uint public balance;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    constructor() public {
        owner = msg.sender;
    }

    function setOwner(address _owner) public onlyOwner {
        owner = _owner;
    }

    function withdraw(uint amount) public onlyOwner {
        balance -= amount;
    }
}
```
In the fixed version, the `onlyOwner` modifier is used to ensure that only the owner can perform sensitive actions such as transferring ownership or withdrawing funds. This helps mitigate the risk of privilege mismanagement by enforcing access control at the contract level.
