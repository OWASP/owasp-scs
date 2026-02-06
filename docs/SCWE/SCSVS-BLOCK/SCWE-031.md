---
title: Insecure use of Block Variables
id: SCWE-031
alias: insecure-block-timestamp-usage
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BLOCK]
  scsvs-scg: [SCSVS-BLOCK-2]
  cwe: [682]
status: new
---

## Relationships
- **CWE-682: Incorrect Calculation**  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
In blockchain networks like Ethereum, block variables `(block.timestamp, block.number, block.difficulty` / `block.prevrandao` post-merge, etc.) provide information about the current state of the blockchain. However, these values are not fully deterministic and can be manipulated by validators (or miners on PoW chains), leading to vulnerabilities in smart contracts.

Block timestamps are not guaranteed to be accurate or consistent, and validators (or miners on PoW chains) can influence them within a certain range. This can cause issues when contracts depend on precise timing for critical functionality, such as token distribution, access control, or other time-sensitive events.

Potential issues that arise from insecure timestamp usage include:

- Timestamp Manipulation: Validators (or miners on PoW) can slightly alter `block.timestamp` to influence time-sensitive logic (e.g., auctions, token distributions, staking rewards).
- Predictable Randomness: Using `block.number` or `block.difficulty` as a source of randomness allows attackers to predict and manipulate outcomes.
- Exploitable Access Control: Contracts that rely on block timestamps for permissions or actions may be bypassed if timestamps are adjusted.

## Remediation
- **Avoid timestamp-based conditions**: Where possible, use block numbers instead of timestamps. Block numbers are more reliable and less subject to manipulation.
- **Use Oracles**: For time-sensitive contracts, consider using trusted oracles to provide external time data.

## Examples

### Insecure Block Timestamp Usage- Timestamp-Based Deadlines

```solidity
pragma solidity ^0.4.0;

contract TimestampExample {
    uint public deadline;

    function setDeadline(uint _deadline) public {
        deadline = _deadline;
    }

    function checkDeadline() public view returns (string) {
        if (block.timestamp > deadline) {
            return "Deadline passed";
        } else {
            return "Deadline not passed";
        }
    }
}
```

In the above example, `block.timestamp` is used to compare with the deadline. This creates a potential vulnerability as validators (or miners on PoW) can manipulate the block timestamp within a predefined window (~15 seconds).

### Fixed Block Timestamp Usage
```solidity
pragma solidity ^0.4.0;

contract SafeTimestampExample {
    uint public deadline;
    uint public blockNumber;

    function setDeadline(uint _deadline) public {
        deadline = _deadline;
        blockNumber = block.number;
    }

    function checkDeadline() public view returns (string) {
        if (block.number > blockNumber + 1000) { // Assuming a reasonable number of blocks for a deadline
            return "Deadline passed";
        } else {
            return "Deadline not passed";
        }
    }
}
```
In this fixed version, the contract uses `block.number` instead of `block.timestamp`. This makes the contract less susceptible to timestamp manipulation, as block numbers are more reliable and consistent.

### Insecure Lottery Using block.timestamp

```solidity
pragma solidity ^0.8.0;

contract InsecureLottery {
    address[] public players;

    function enter() public payable {
        require(msg.value > 0.01 ether, "Minimum ETH required");

        players.push(msg.sender);
    }

    function pickWinner() public {
        uint index = uint(block.timestamp) % players.length; // Insecure: Predictable outcome
        (bool ok, ) = payable(players[index]).call{value: address(this).balance}("");
        require(ok, "Transfer failed");
    }
}
```
Issue:
- Predictability: Since `block.timestamp` is manipulable within a small range, validators (or miners on PoW chains) can influence the winner selection.
- Attack Vector: A validator (or miner on PoW) could reorder transactions to ensure a specific outcome

### Secure Alternative (Commit-Reveal)

```solidity
pragma solidity ^0.8.0;

contract SecureLottery {
    mapping(address => bytes32) public commits;
    mapping(address => bytes32) public revealed;
    address[] public players;

    function commit(bytes32 hash) external payable {
        require(msg.value > 0.01 ether, "Minimum ETH required");
        require(commits[msg.sender] == bytes32(0), "Already committed");
        commits[msg.sender] = hash;
        players.push(msg.sender);
    }

    function reveal(bytes32 secret) external {
        require(keccak256(abi.encodePacked(secret)) == commits[msg.sender], "Invalid reveal");
        revealed[msg.sender] = secret;
    }

    function pickWinner() external {
        bytes32 combined = bytes32(0);
        for (uint i = 0; i < players.length; i++) {
            require(revealed[players[i]] != bytes32(0), "All must reveal");
            combined = keccak256(abi.encodePacked(combined, revealed[players[i]]));
        }
        uint index = uint(combined) % players.length;
        (bool ok, ) = payable(players[index]).call{value: address(this).balance}("");
        require(ok, "Transfer failed");
    }
}
```
Fixes:
- Uses commit-reveal: each player commits a hash, then reveals; combined secrets determine the winner.
- `block.prevrandao` and `block.timestamp` are **not safe** for value-at-stake randomness — use VRF (e.g., Chainlink) or commit-reveal.

--- 