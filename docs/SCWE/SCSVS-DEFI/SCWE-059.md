---
title: Insufficient Gas Griefing
id: SCWE-059
alias: insufficient-gas-griefing
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-2]
  cwe: [400]
status: new
---

## Relationships  
- CWE-400: Uncontrolled Resource Consumption  
  [https://cwe.mitre.org/data/definitions/400.html](https://cwe.mitre.org/data/definitions/400.html)  


## Description
Insufficient gas griefing occurs when an attacker intentionally sends a transaction with insufficient gas to force the contract to fail. This can lead to resource consumption issues and potential denial of service for the contract or other users. If a contract relies on external calls or interacts with other contracts and does not properly handle gas estimation, it may be vulnerable to such attacks.

## Remediation
To mitigate this vulnerability, ensure that gas estimation and proper gas limits are handled when performing contract calls, especially when interacting with other contracts. Additionally, use mechanisms to handle failures gracefully, such as revert messages and checks for sufficient gas before initiating important operations.

### Vulnerable Contract Example
```solidity
contract GasGriefing {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferFunds(address payable recipient, uint256 amount) public {
        require(msg.sender == owner, "Not the owner");
        recipient.transfer(amount);  // Potential for griefing with insufficient gas
    }
}
```

### Fixed Contract Example
```solidity
contract GasGriefingSafe {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function transferFunds(address payable recipient, uint256 amount) public {
        require(msg.sender == owner, "Not the owner");
        bool success = recipient.send(amount);  // Safe transfer with gas estimation
        require(success, "Transfer failed due to insufficient gas");
    }
}
```