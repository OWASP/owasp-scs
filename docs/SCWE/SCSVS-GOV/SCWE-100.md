---
title: Missing Quorum Validation in Governance Execution
id: SCWE-100
alias: missing-governance-quorum-validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [754]
status: new
---

## Relationships
- CWE-754: Improper Check for Unusual or Exceptional Conditions  
  [https://cwe.mitre.org/data/definitions/754.html](https://cwe.mitre.org/data/definitions/754.html)

## Description
Governance systems that allow proposal execution based solely on vote counts (e.g., "for" > "against") without enforcing a minimum participation threshold (quorum) can execute proposals with negligible community participation. A proposal may "pass" with only a handful of votes if quorum is not checked, allowing a small group or attacker with accumulated tokens to push through changes that lack legitimate community mandate.

## Remediation
- Enforce a minimum quorum (e.g., percentage of total supply or voting power) before allowing execution.
- Require both vote majority and quorum to be satisfied; revert execution if quorum is not met.
- Consider time-weighted or participation-based quorum to prevent last-block manipulation.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract VulnerableGov {
    mapping(uint256 => uint256) public forVotes;
    mapping(uint256 => uint256) public againstVotes;
    uint256 public totalSupply;

    function execute(uint256 proposalId) external {
        require(forVotes[proposalId] > againstVotes[proposalId], "proposal failed");
        // No quorum check — can execute with 2 for, 1 against even if totalSupply is 1M
        _executeProposal(proposalId);
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract SecureGov {
    mapping(uint256 => uint256) public forVotes;
    mapping(uint256 => uint256) public againstVotes;
    uint256 public totalSupply;
    uint256 public constant QUORUM_BPS = 400; // 4%

    function execute(uint256 proposalId) external {
        uint256 totalVotes = forVotes[proposalId] + againstVotes[proposalId];
        require(forVotes[proposalId] > againstVotes[proposalId], "proposal failed");
        require(totalVotes * 10000 >= totalSupply * QUORUM_BPS, "quorum not met");
        _executeProposal(proposalId);
    }
}
```
