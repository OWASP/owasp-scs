---
id: SCSTG-TEST-0006
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-2
platform: []
title: Test Access Control Using Merkle Trees
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0006
---

Ensure that `msg.sender` validation is properly implemented when using Merkle trees to maintain security and prevent unauthorized access.

- When using Merkle trees to authenticate users or grant permissions, ensure that the contract verifies that `msg.sender` matches the expected address and Merkle proof. This prevents unauthorized actors from bypassing security by submitting incorrect proofs.

```solidity
    require(verifyMerkleProof(msg.sender, merkleProof), "Invalid Merkle proof");
```

- Use whitelisting to restrict interactions to a specific set of addresses, providing additional security against malicious actors.

- Implement a whitelisting mechanism that allows only approved addresses to interact with specific functions. Ensure that only addresses explicitly added to the whitelist are able to execute sensitive operations.

```solidity
    address[] public whitelist;

    modifier onlyWhitelisted() {
        bool isWhitelisted = false;
        for (uint i = 0; i < whitelist.length; i++) {
            if (msg.sender == whitelist[i]) {
                isWhitelisted = true;
                break;
            }
        }
        require(isWhitelisted, "Address not whitelisted");
        _;
    }

    function addToWhitelist(address _address) external onlyOwner {
        whitelist.push(_address);
    }
```
- Ensure that functions modifying the contract state or accessing sensitive operations have proper access controls implemented.

- Critical functions, such as those that modify contract state or handle sensitive information, should only be callable by authorized addresses (e.g., the owner or an admin). Use modifiers to enforce access controls for these functions.

```solidity
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    function modifyContractState() external onlyOwner {
        // Logic to modify contract state
    }
```