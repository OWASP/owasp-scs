---
id: SCSTG-TEST-0004
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-1
platform: []
title: Test Access Control on Critical Functions
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0004 
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