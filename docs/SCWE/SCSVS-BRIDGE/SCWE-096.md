---
title: Missing Token Burn on During Cross-Chain NFT Withdrawal
id: SCWE-096
alias: Missing-Token-Burn-on-During-Cross-Chain-NFT-Withdrawal
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-1]
  cwe: [345]
status: new
---

## Relationships
- CWE-345:  Insufficient Verification of Data Authenticity  
  [CWE-345 Link](https://cwe.mitre.org/data/definitions/345.html)
- CWE-664: Improper Control of a Resource Through Its Lifetime      
  [CWE-664 Link](https://cwe.mitre.org/data/definitions/664.html)

## Description  
This weakness occurs when a cross-chain bridge allows withdrawals from Chain B to Chain A without properly burning or locking the corresponding token on the source chain (Chain B) before initiating the cross-chain transaction.

As a result, the same token can exist simultaneously on both chains, enabling a double-spend scenario where malicious actors can sell, transfer, or use the same token on multiple chains.

## Remediation  
1. Burn the NFT
- Call the burn(tokenId) function on the L2 NFT contract before sending the cross-chain withdrawal request.
- This ensures that the NFT no longer exists on L2 and cannot be reused, transferred, or sold.

2. Alternatively, Lock the NFT (if burning isn’t possible)
- If NFTs are not meant to be permanently destroyed, implement a lock mechanism to freeze the token on L2 until the cross-chain withdrawal is completed successfully.

3. Update Cross-Chain Workflow

- Enforce the burn/lock operation as part of the withdrawal process.
- Revert the entire transaction if the burn/lock fails.

## Examples  
- **Vulnerable Code (Not Burning Token Before Sending Cross Chain Message)**  
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SourceChainNFTGateway {
    mapping(address => mapping(uint256 => address)) public ownerOf;

    function withdrawNFT(address l2Token, uint256 tokenId) external {
        require(ownerOf[l2Token][tokenId] == msg.sender, "Not the owner");

        // ❌ Send cross-chain message to Destination Chain (omitted for simplicity)
        // NFT is still available on Source Chain → double-spend possible
    }
}
```

- **Safe Code (Burning Token Before Sending Cross Chain Message)**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IL2NFT {
    function burn(uint256 tokenId) external;
}

contract SourceChainNFTGateway {
    mapping(address => mapping(uint256 => address)) public ownerOf;

    function withdrawNFT(address l2Token, uint256 tokenId) external {
        require(ownerOf[l2Token][tokenId] == msg.sender, "Not the owner");

        // ✅ Burn the NFT on Source Chain to prevent double-spend
        IL2NFT(l2Token).burn(tokenId);

        // Send cross-chain message to Destination Chain (omitted for simplicity)
    }
}
```
