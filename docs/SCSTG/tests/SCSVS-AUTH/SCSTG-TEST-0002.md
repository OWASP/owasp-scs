---
id: SCSTG-TEST-0002
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-1
platform: []
title: Identity Verification Test
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0002 
---

Validate that unexpected addresses do not result in unintended behaviors, particularly when these addresses refer to contracts within the same protocol.

- Ensure that when interacting with contracts, unexpected addresses are properly validated before performing sensitive operations.
```solidity
require(address(contract) != address(0), "Invalid address");
```

Verify that functions like ecrecover handle all potential null addresses properly to avoid vulnerabilities arising from unexpected ecrecover outputs.

- Ensure that ecrecover does not process empty or null addresses.
```solidity
address recovered = ecrecover(messageHash, v, r, s);
require(recovered != address(0), "Invalid signature");
```

