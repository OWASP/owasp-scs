---
title: Insecure Event Emission
id: SCWE-063
alias: insecure-event-emission
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-2]
  cwe: [778]
status: new
---

## Relationships  
- CWE-778: Insufficient Logging  
  [https://cwe.mitre.org/data/definitions/778.html](https://cwe.mitre.org/data/definitions/778.html)  

## Description  
Events in Solidity play a critical role in logging contract activity and ensuring transparency. Improper event handling can lead to security risks such as:  

1. **Missing critical event emissions** – Making external monitoring difficult.  
2. **Emitting misleading or incorrect data** – Resulting in users or external systems making incorrect assumptions.  
3. **Logging sensitive information** – Leaking private or security-sensitive data.  

Failure to handle events properly can affect contract auditing, debugging, and external monitoring tools, making it difficult to detect anomalies or track contract states correctly.  

## Remediation  
- Emit events for all critical state changes, such as token transfers, ownership changes, or contract upgrades.  
- Ensure that the data logged in events accurately represents the actual contract state.  
- Avoid logging sensitive information such as private keys, hashes used for authentication, or confidential business logic.  

### Vulnerable Contract Example  
```solidity
contract Example {
    mapping(address => uint) public balances;
    event Withdraw(address indexed user, uint amount);

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient funds");
        payable(msg.sender).transfer(_amount);
        balances[msg.sender] -= _amount;
        
        // Incorrect event emission: Logs the requested amount instead of the actual withdrawn amount
        emit Withdraw(msg.sender, _amount);
    }
}
```

### Issues in the Vulnerable Code
- The Withdraw event logs `_amount`, which is the requested `withdrawal` amount, but if the transfer fails (due to gas limits, reentrancy, or an external issue), the event still logs it as if the withdrawal happened.
- If an attacker exploits a discrepancy between event logs and actual state changes, they could mislead users, external indexers, or off-chain services.

### Fixed Contract Example

```solidity
contract Example {
    mapping(address => uint) public balances;
    event Withdraw(address indexed user, uint actualAmount);

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient funds");

        uint beforeBalance = address(this).balance;
        (bool success, ) = payable(msg.sender).call{value: _amount}("");
        uint afterBalance = address(this).balance;

        require(success, "Transfer failed");

        uint actualWithdrawn = beforeBalance - afterBalance;
        balances[msg.sender] -= actualWithdrawn;

        // Logs the correct amount actually withdrawn
        emit Withdraw(msg.sender, actualWithdrawn);
    }
}
```
### Fixes in the Secure Code
- Uses `call{value: _amount}("")` to send funds safely and ensures success before updating the balance.
- Calculates the actual withdrawn amount `(beforeBalance - afterBalance)` to ensure accurate logging.
- Prevents false event emissions by only logging an event if the transaction succeeds.