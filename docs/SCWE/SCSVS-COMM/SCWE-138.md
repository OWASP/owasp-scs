---
title: Reentrancy via ERC721/ERC1155 Safe Transfer Callbacks
id: SCWE-138
alias: erc721-erc1155-callback-reentrancy
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [841]
status: new
---

## Relationships
- CWE-841: Improper Enforcement of Behavioral Workflow  
  [https://cwe.mitre.org/data/definitions/841.html](https://cwe.mitre.org/data/definitions/841.html)

## Description
ERC721 `safeTransferFrom` and ERC1155 `safeTransferFrom` invoke `onERC721Received` or `onERC1155Received` on the recipient contract. If the recipient is a contract that accepts NFTs and performs sensitive logic (e.g., withdrawals, state updates) inside these callbacks without reentrancy protection, an attacker can reenter the sender contract during the transfer and exploit stale state—similar to ERC777 hooks (SCWE-104) but for NFTs.

## Remediation
- Add `nonReentrant` guards around functions that perform NFT transfers and any logic that could be reentered via the receiver callback.
- Update state (e.g., balances, accounting) before calling `safeTransferFrom`.
- Consider using `transferFrom` instead of `safeTransferFrom` when the recipient is trusted, to avoid callbacks.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

interface IERC721 {
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
}

contract NFTVault {
    mapping(address => uint256) public deposits;
    IERC721 public nft;

    function deposit(uint256 tokenId) external {
        nft.safeTransferFrom(msg.sender, address(this), tokenId);
        deposits[msg.sender]++;
    }

    function withdraw(uint256 tokenId) external {
        require(deposits[msg.sender] > 0, "No deposit");
        nft.safeTransferFrom(address(this), msg.sender, tokenId);  // Callback here—attacker reenters
        deposits[msg.sender]--;  // Too late: attacker already reentered and passed the check
    }
}
```
**Why vulnerable:** During `withdraw`, `safeTransferFrom` calls `onERC721Received` on the recipient before the state update. A malicious contract can reenter `withdraw` in that callback, pass the `deposits[msg.sender] > 0` check again, and withdraw a second NFT (double withdrawal).

### Fixed
```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NFTVault is ReentrancyGuard {
    mapping(address => uint256) public deposits;
    IERC721 public nft;

    function withdraw(uint256 tokenId) external nonReentrant {
        require(deposits[msg.sender] > 0, "No deposit");
        deposits[msg.sender]--;
        nft.safeTransferFrom(address(this), msg.sender, tokenId);
    }
}
```
**Fix:** `nonReentrant` blocks reentry through the ERC721 receiver callback.
