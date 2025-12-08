---
id: SCSTG-TEST-0005
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-1
platform: []
title: Test Timed Permissions
scsvs_cg_levels: 
- L2
tests: SCSTG-TEST-0005 
---

Ensure that access controls are implemented correctly to determine who can use certain functions, and avoid unauthorized changes or withdrawals.

- Ensure that functions requiring specific roles or permissions are restricted properly using onlyOwner or role-based checks.

```solidity
    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    function withdraw() external onlyOwner {
        // Only the owner can withdraw
    }
```