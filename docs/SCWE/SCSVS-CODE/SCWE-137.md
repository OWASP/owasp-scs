---
title: Read-Only Reentrancy via View Function State Staleness
id: SCWE-137
alias: read-only-reentrancy
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [367]
status: new
---

## Relationships
- CWE-367: Time-of-check Time-of-use (TOCTOU) Race Condition  
  [https://cwe.mitre.org/data/definitions/367.html](https://cwe.mitre.org/data/definitions/367.html)

## Description
Read-only reentrancy occurs when a `view` or `pure` function is called during an external callback (e.g., from a lending protocol reading collateral, or an integrator querying state). The view function returns stale state because the contract's effects have not yet been applied—the callback happens mid-transaction, before state updates complete. External protocols that rely on this state for critical decisions (e.g., liquidations, pricing, health checks) can be exploited to drain funds or bypass invariants.

This is distinct from classic reentrancy (SCWE-046): no state-modifying function is reentered, but the *read* of inconsistent state by external callers during a callback causes the vulnerability.

## Remediation
- Apply `nonReentrant` guards to functions that make external calls, even if the caller only reads state—external protocols may call back into view functions.
- Use a "read-your-writes" pattern: ensure view functions reflect in-flight state or document that they are unsafe during callbacks.
- Integrators should not rely on view functions of contracts that perform external calls without reentrancy guards.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract LendingPool {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public borrowed;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }

    function getHealthFactor(address user) external view returns (uint256) {
        return (balances[user] * 1e18) / (borrowed[user] + 1);
    }
}
```
**Why vulnerable:** During `withdraw`, the recipient's callback can invoke `getHealthFactor(user)` (e.g., from an integrator or liquidation bot). The victim's state may be mid-update or the integrator may rely on cached/stale values from the victim or dependent contracts. External protocols making decisions based on such reads can allow unhealthy borrows or incorrect liquidations.

### Fixed
```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract LendingPool is ReentrancyGuard {
    mapping(address => uint256) public balances;
    mapping(address => uint256) public borrowed;

    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Fix:** `nonReentrant` prevents external callbacks from reentering or being used while state is mid-update, so view functions cannot be called in an inconsistent state during the callback.
