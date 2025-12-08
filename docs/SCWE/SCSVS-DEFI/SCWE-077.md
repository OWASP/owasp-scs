---
title: Lack of Rate Limiting  
id: SCWE-077  
alias: lack-of-rate-limiting  
platform: []  
profiles: [L1]  
mappings:  
  scsvs-cg: [SCSVS-DEFI]  
  scsvs-scg: [SCSVS-DEFI-2]  
  cwe: [770]  
status: new  
---

## Relationships  
- **CWE-770: Allocation of Resources Without Limits or Throttling**  
  [https://cwe.mitre.org/data/definitions/770.html](https://cwe.mitre.org/data/definitions/770.html)  

## Description  
Lack of rate limiting in a smart contract can lead to **Denial of Service (DoS)** attacks, excessive gas consumption, or contract state bloating. Without a mechanism to restrict the frequency of function calls, an attacker can flood the contract with transactions, causing delays, increased gas fees, or complete unavailability of critical functions.  

This vulnerability is particularly dangerous in **DeFi protocols**, where unlimited function calls could drain funds, abuse governance mechanisms, or overload on-chain processing.  

## Remediation  
- Implement **rate-limiting mechanisms** such as **time-based constraints** (e.g., requiring a cooldown period between calls).  
- Use **counters with expiration timestamps** to track and restrict repetitive actions.  
- Introduce **gas fees or staking requirements** to deter spam transactions.  

### Vulnerable Contract Example  
```solidity
contract Example {
    mapping(address => uint) public userRequests;

    // ❌ No rate limiting: users can spam this function indefinitely
    function request() public {
        userRequests[msg.sender]++;
        // No restrictions or cooldowns, allowing abuse
    }
}
```

**Why is this vulnerable?**
- No restrictions on how frequently a user can call `request()`.
- An attacker can spam transactions, leading to high gas costs and DoS.
- Storage bloat from excessive `userRequests` mappings.

### Fixed Contract Example

```solidity
contract SecureExample {
    struct RequestData {
        uint count;
        uint lastReset;
    }

    mapping(address => RequestData) public userRequests;
    uint public constant REQUEST_LIMIT = 5;
    uint public constant TIME_WINDOW = 1 hours;

    // ✅ Implement rate limiting with a cooldown period
    function request() public {
        RequestData storage requestData = userRequests[msg.sender];

        if (block.timestamp > requestData.lastReset + TIME_WINDOW) {
            requestData.count = 0;  // Reset count after time window
            requestData.lastReset = block.timestamp;
        }

        require(requestData.count < REQUEST_LIMIT, "Rate limit exceeded");
        requestData.count++;
    }
}
```
**Why is this safe?**
- Tracks request timestamps, resetting counts after a fixed period.
- Restricts excessive calls, preventing abuse and DoS attacks.
- Efficient state management, reducing unnecessary storage costs.

**By enforcing rate limits, contracts can prevent spam attacks and ensure fair access to on-chain resources.**