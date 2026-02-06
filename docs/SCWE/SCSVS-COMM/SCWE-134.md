---
title: Event Emission Before State Update
id: SCWE-134
alias: premature-event-emission
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-2]
  cwe: [209]
status: new
---

## Relationships
- CWE-209: Generation of Error Message Containing Sensitive Information  
  [https://cwe.mitre.org/data/definitions/209.html](https://cwe.mitre.org/data/definitions/209.html)

## Description
Emitting events before state changes can mislead off-chain indexers, bots, and accounting systems. Attackers may race on optimistic off-chain reactions (e.g., bots responding to Transfer events) before the actual state is finalized or even reverted.

## Remediation
- Emit events only after successful state updates.
- When using optimistic event flows, include commit/reveal or finalized flags.
- In critical paths, make off-chain consumers validate state after seeing events.

## Examples

### Vulnerable
```solidity
emit Transfer(msg.sender, to, amount);
balances[msg.sender] -= amount; // may revert later
balances[to] += amount;
```

### Fixed
```solidity
balances[msg.sender] -= amount;
balances[to] += amount;
emit Transfer(msg.sender, to, amount); // after state change
```

