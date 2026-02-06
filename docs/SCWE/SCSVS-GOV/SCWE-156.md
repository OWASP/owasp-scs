---
title: Missing Emergency Circuit Breaker for Critical Operations
id: SCWE-156
alias: lack-of-circuit-breaker
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [693]
status: new
---

## Relationships
- CWE-693: Protection Mechanism Failure  
  [https://cwe.mitre.org/data/definitions/693.html](https://cwe.mitre.org/data/definitions/693.html)

## Description
A circuit breaker is a threshold-based or condition-based halt mechanism that stops critical operations when anomalies are detected (e.g., TVL drop >X%, unusual withdrawal volume, oracle deviation). Unlike simple pausability (SCWE-014), a circuit breaker automatically or semi-automatically triggers based on predefined conditions, providing an additional safety layer during attacks or market stress.

## Remediation
- Implement circuit breakers that halt deposits, withdrawals, or swaps when thresholds are exceeded.
- Use oracle-based triggers (e.g., price deviation) or rate-limit triggers.
- Ensure the circuit breaker can be reset by governance or after cooldown.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract LendingPool {
    mapping(address => uint256) public balances;
    uint256 public totalDeposits;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Gap:** No circuit breaker. A flash loan or oracle attack could drain funds before anyone can pause.

### Mitigation
```solidity
uint256 public maxWithdrawalPerTx = 100 ether;
uint256 public lastWithdrawalTime;
uint256 public constant WITHDRAWAL_COOLDOWN = 1 hours;

function withdraw(uint256 amount) external {
    require(amount <= maxWithdrawalPerTx, "Circuit breaker: amount too high");
    require(block.timestamp >= lastWithdrawalTime + WITHDRAWAL_COOLDOWN, "Cooldown");
    lastWithdrawalTime = block.timestamp;
    // ... rest of logic
}
```
