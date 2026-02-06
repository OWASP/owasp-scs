---
title: Flash-Loan-Fueled Governance Manipulation
id: SCWE-101
alias: flashloan-governance-manipulation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-1]
  cwe: [367]
status: new
---

## Relationships
- CWE-367: Time-of-Check Time-of-Use (TOCTOU) Race Condition  
  [https://cwe.mitre.org/data/definitions/367.html](https://cwe.mitre.org/data/definitions/367.html)

## Description
If voting power is measured at execution time without historical snapshots or locking, an attacker can borrow a large balance via flash loan, pass a proposal, and return the loan in the same transaction. Governance decisions then depend on transient liquidity rather than long-term stake.

## Remediation
- Use token balance snapshots at a fixed block for voting power.
- Require vote escrow/locking or minimum voting period spanning multiple blocks.
- Set quorum and proposal thresholds based on historical supply, not instantaneous balances.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract SimpleGov {
    IERC20 public token;
    mapping(uint256 => bool) public proposals;

    function vote(uint256 id, bool support) external {
        require(token.balanceOf(msg.sender) > 1_000_000 ether, "low power");
        if (support) { proposals[id] = true; }
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Snapshot.sol";

contract SnapshotGov {
    ERC20Snapshot public token;
    mapping(uint256 => uint256) public snapshotId;

    function openProposal(uint256 id) external {
        snapshotId[id] = token.snapshot();
    }

    function vote(uint256 id, bool support) external {
        uint256 power = token.balanceOfAt(msg.sender, snapshotId[id]);
        require(power > 1_000_000 ether, "low power");
        // record vote...
    }
}
```

