---
title: Missing Post-Operation Health Check
id: SCWE-125
alias: missing-health-check
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-1]
  cwe: [754]
status: new
---

## Relationships
- CWE-754: Improper Check for Unusual or Exceptional Conditions  
  [https://cwe.mitre.org/data/definitions/754.html](https://cwe.mitre.org/data/definitions/754.html)

## Description
Lending/borrowing protocols that do not re-evaluate health factors after actions (borrow, withdraw, leverage) allow users to exit with unhealthy positions. Attackers can drain collateral or avoid liquidation by skipping post-operation solvency checks.

## Remediation
- Recompute health factor after every state-changing action and revert if below threshold.
- Lock price/oracle reads during the operation to avoid mid-tx manipulation.
- Add invariant/fuzz tests to ensure every path enforces solvency.

## Examples

### Vulnerable
```solidity
function borrow(uint256 amount) external {
    _issueDebt(msg.sender, amount);
    // no health check after debt increase
}
```

### Fixed
```solidity
function borrow(uint256 amount) external {
    _issueDebt(msg.sender, amount);
    require(_health(msg.sender) >= MIN_HF, "insolvent");
}
```

