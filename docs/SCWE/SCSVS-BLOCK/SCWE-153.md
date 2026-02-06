---
title: Reliance on block.prevrandao for High-Value Randomness
id: SCWE-153
alias: unsafe-block-prevrandao-value-at-stake
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BLOCK]
  scsvs-scg: [SCSVS-BLOCK-1]
  cwe: [330]
status: new
---

## Relationships
- CWE-330: Use of Insufficiently Random Values  
  [https://cwe.mitre.org/data/definitions/330.html](https://cwe.mitre.org/data/definitions/330.html)

## Description
Post-merge (Ethereum PoS), `block.difficulty` was replaced by `block.prevrandao`. Both are manipulable by validators: they can influence the value within protocol rules. Using `block.prevrandao` (or `block.difficulty`) for high-value randomness—lotteries, airdrops, winner selection—allows validators or sophisticated actors to predict or bias outcomes. SCWE-024 and SCWE-084 cover blockhash/timestamp; this weakness specifically addresses `block.prevrandao`.

## Remediation
- Do not use `block.prevrandao` or `block.difficulty` for value-at-stake randomness.
- Use Chainlink VRF, commit-reveal schemes, or other verifiable randomness sources.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Lottery {
    address[] public participants;

    function pickWinner() external view returns (uint256) {
        return uint256(keccak256(abi.encodePacked(block.prevrandao, block.timestamp))) % participants.length;
    }
}
```
**Why vulnerable:** `block.prevrandao` is manipulable by validators; they can influence the value to bias the outcome.

### Fixed
Use Chainlink VRF V2 or a commit-reveal scheme where participants commit hashes before the random value is known. See SCWE-024 for a Chainlink VRF example.
