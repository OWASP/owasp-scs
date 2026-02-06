---
title: Missing Supply Cap Enforcement
id: SCWE-116
alias: missing-supply-cap
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-2]
  cwe: [693]
status: new
---

## Relationships
- CWE-693: Protection Mechanism Failure  
  [https://cwe.mitre.org/data/definitions/693.html](https://cwe.mitre.org/data/definitions/693.html)

## Description
Tokens or lending systems without hard supply caps allow privileged accounts or flawed logic to mint unlimited units, inflating supply and draining collateralized protocols. Lack of caps also breaks price assumptions in AMMs and oracles.

## Remediation
- Define immutable max supply and enforce it on every mint path.
- Separate minting roles with multi-sig and timelock; emit events for mint changes.
- Include cap checks in upgrades and cross-chain minting/bridging logic.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Token {
    address public owner;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) external {
        require(msg.sender == owner, "not owner");
        totalSupply += amount; // no cap
        // mint tokens...
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Token {
    address public owner;
    uint256 public totalSupply;
    uint256 public constant MAX_SUPPLY = 1_000_000 ether;

    function mint(address to, uint256 amount) external {
        require(msg.sender == owner, "not owner");
        require(totalSupply + amount <= MAX_SUPPLY, "cap exceeded");
        totalSupply += amount;
        // mint tokens...
    }
}
```

