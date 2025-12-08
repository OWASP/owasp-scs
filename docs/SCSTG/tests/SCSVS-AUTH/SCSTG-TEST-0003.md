---
id: SCSTG-TEST-0003
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-1
platform: []
title: Least Privilege Principle Test
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0003 
---

Use msg.sender instead of tx.origin for authorization to avoid potential abuse from malicious contracts; include checks like require(tx.origin == msg.sender) to ensure the sender is an EOA.

- tx.origin can be abused by malicious contracts to trick the system into performing actions on behalf of an unsuspecting user. msg.sender is preferred since it refers to the direct sender of the message.
```solidity
require(msg.sender == owner, "Not the owner");
require(tx.origin == msg.sender, "Only EOA can execute");
```

Certain addresses might be blocked or restricted from receiving tokens (e.g., LUSD). Ensure that address restrictions are properly managed and verified.

- If certain addresses (like LUSD) should be blocked from receiving tokens, ensure that there’s a check in place to restrict these addresses.
```solidity
address restrictedAddress = 0x123...;  // Example of a restricted address
require(msg.sender != restrictedAddress, "Restricted address cannot perform this operation");
```


Ensure that Guard’s hooks (e.g., checkTransaction(), checkAfterExecution()) are executed to enforce critical security checks.

- If using a Guard contract, ensure that hooks like checkTransaction() or checkAfterExecution() are properly implemented to enforce security conditions.
```solidity
function checkTransaction() internal {
    // Add conditions to verify transaction before execution
}

function checkAfterExecution() internal {
    // Add conditions to verify transaction after execution
}
```