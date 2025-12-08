---
title: Incorrect Ether Balance Tracking
id: SCWE-075
alias: incorrect-ether-balance
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [852]  # CWE-852: Untrusted Control Sphere (External Ether Transfers)
status: new
---

## Relationships  
- CWE-852: Untrusted Control Sphere  
  [https://cwe.mitre.org/data/definitions/852.html](https://cwe.mitre.org/data/definitions/852.html)  

## Description
Incorrect Ether balance tracking occurs when a contract manually maintains an internal balance variable instead of relying on `address(this).balance`. This creates inconsistencies when Ether is received outside of expected functions (e.g., via `selfdestruct()`, `transfer()`, or direct deposits).  

Attackers can exploit this by artificially inflating the contract's perceived balance, leading to unauthorized withdrawals or failed transactions. This issue is common in poorly designed deposit/withdraw systems that do not properly verify the actual contract balance.

## Attack Scenario
An attacker sends Ether to the contract using `selfdestruct()`, increasing its actual balance without updating the internal tracking variable. Later, a user tries to withdraw funds, but the contract incorrectly assumes it has more Ether than it actually does, causing unexpected failures or exploits.

## Remediation
- **Use `address(this).balance`** instead of manually tracking Ether balance.
- **Prevent external Ether deposits** by disabling the fallback function unless explicitly needed.
- **Ensure proper accounting** by always reconciling balances before allowing withdrawals.

### Vulnerable Contract Example
```solidity
// ❌ Vulnerable to incorrect balance tracking due to external Ether deposits
contract IncorrectBalanceTracking {
    uint public balance;  // ❌ Manually tracking Ether balance

    function deposit() public payable {
        balance += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balance >= _amount, "Insufficient funds");
        payable(msg.sender).transfer(_amount);
        balance -= _amount;
    }
}
```
**Why is this vulnerable?**
- The contract does not account for direct Ether transfers outside deposit().
- An attacker can send Ether via `selfdestruct()`, inflating the contract balance without updating balance.
- This can lead to withdrawals being blocked or excessive withdrawals.

### Fixed Contract Example

```solidity
// ✅ Secure implementation that tracks actual balance correctly
contract CorrectBalanceTracking {
    function deposit() public payable {}

    function withdraw(uint _amount) public {
        require(address(this).balance >= _amount, "Insufficient funds");  // ✅ Correct balance check
        payable(msg.sender).transfer(_amount);
    }

    // Optional: Prevent direct Ether transfers
    receive() external payable {
        revert("Direct deposits not allowed");
    }
}
```
**Why is this secure?**
- Uses `address(this).balnce` for accurate balance tracking.
- Prevents external deposits unless explicitly intended.
- No manual `balance` variable, reducing risk of inconsistencies.

---