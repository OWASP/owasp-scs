---
title: Ether Locked Due to Missing Withdrawal Path
id: SCWE-140
alias: locked-ether-non-withdrawable
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [404]
status: new
---

## Relationships
- CWE-404: Improper Resource Shutdown or Release  
  [https://cwe.mitre.org/data/definitions/404.html](https://cwe.mitre.org/data/definitions/404.html)

## Description
Contracts can receive ETH via `receive()`, `fallback()`, `selfdestruct` from another contract, or accidental sends. If the contract has no function to withdraw or forward this ETH, the funds become permanently locked. This can occur when a contract was not designed to hold ETH, when the withdrawal function is restricted to a role that no longer exists, or when the contract lacks a rescue/withdraw mechanism for unexpected inflows.

## Remediation
- Implement a withdrawal or rescue function for authorized roles to recover stuck ETH.
- If the contract should not accept ETH, use `receive() external payable { revert("ETH not accepted"); }`.
- Document how unexpected ETH (e.g., from `selfdestruct`) is handled.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract TokenSale {
    mapping(address => uint256) public balances;

    function buyTokens() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdrawTokens() external {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Why vulnerable:** If ETH is sent via `selfdestruct` or a plain transfer, it increases `address(this).balance` but not any user's `balances`. That ETH cannot be withdrawn by anyone and is locked.

### Fixed
```solidity
pragma solidity ^0.8.0;

contract TokenSale {
    address public owner;
    uint256 public totalDeposits;
    mapping(address => uint256) public balances;

    constructor() { owner = msg.sender; }

    function buyTokens() external payable {
        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function withdrawTokens() external {
        uint256 amount = balances[msg.sender];
        balances[msg.sender] = 0;
        totalDeposits -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }

    function rescueStuckETH() external {
        require(msg.sender == owner, "Not owner");
        uint256 excess = address(this).balance - totalDeposits;
        require(excess > 0, "No excess");
        (bool ok, ) = owner.call{value: excess}("");
        require(ok, "Transfer failed");
    }
}
```
**Fix:** Track `totalDeposits` and only rescue ETH in excess of user deposits (e.g., from `selfdestruct`). `withdrawTokens` lets users claim their deposits; `rescueStuckETH` recovers only excess ETH.
