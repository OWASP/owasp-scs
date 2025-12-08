---
title: Lack of Emergency Stop Mechanism
id: SCWE-014
alias: lack-of-emergency-stop
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [693]
status: new
---

## Relationships
- **CWE-693**: Protection Mechanism Failure  
  [CWE-693](https://cwe.mitre.org/data/definitions/693.html)

## Description
A Lack of Emergency Stop Mechanism refers to the absence of a built-in feature in a smart contract that allows for halting or pausing critical operations during emergencies. This mechanism is essential for mitigating risks like a discovered vulnerability, unexpected behavior, or a malicious attack. Without this safeguard, the contract may continue executing malicious actions or suffer irreversible damage. The ability to stop critical functions provides an important recovery measure in scenarios where an exploit is detected or control needs to be regained.

Key risks:
- Continuous execution of harmful or malicious actions without control.
- Difficulty in recovering from unexpected failures.
- Increased vulnerability to hacks or exploitation.

## Remediation
- **Implement a pausable contract pattern**: Use the `Pausable` contract from the OpenZeppelin library to implement a mechanism that allows authorized users (e.g., the owner or a governance entity) to pause and unpause certain critical contract functions.
- **Limit emergency stop to critical functions**: Ensure that only critical functions can be paused to minimize the impact on the rest of the system's operation.
- **Implement role-based access control**: Use a role-based mechanism to control who has the ability to pause or unpause functions, reducing the risk of unauthorized access.

## Examples

### Lack of Emergency Stop Mechanism Example
```solidity
pragma solidity ^0.8.0;

contract NoEmergencyStop {
    address public owner;
    uint public criticalValue;

    constructor() {
        owner = msg.sender;
    }

    // This function is critical and lacks an emergency stop mechanism
    function updateCriticalValue(uint newValue) public {
        require(msg.sender == owner, "Only the owner can update this value");
        criticalValue = newValue;
    }
}
```
In the `NoEmergencyStop` contract, there is no way to stop or pause critical operations, which makes it vulnerable to continued exploitation if an issue arises.

### Fixed: Emergency Stop Mechanism Example

```solidity
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/Pausable.sol";

contract EmergencyStopExample is Pausable {
    address public owner;
    uint public criticalValue;

    constructor() {
        owner = msg.sender;
    }

    // Critical function that can be paused in case of emergency
    function updateCriticalValue(uint newValue) public whenNotPaused {
        require(msg.sender == owner, "Only the owner can update this value");
        criticalValue = newValue;
    }

    // Emergency stop function to pause the contract
    function emergencyStop() public {
        require(msg.sender == owner, "Only the owner can stop the contract");
        _pause();  // Pauses the contract
    }

    // Emergency restart function to unpause the contract
    function resumeOperations() public {
        require(msg.sender == owner, "Only the owner can resume the contract");
        _unpause();  // Resumes the contract
    }
}

```
The `EmergencyStopExample` contract implements the `Pausable` pattern, which allows the contract owner to pause and unpause critical functions using the `emergencyStop` and `resumeOperations` functions. This ensures that if a vulnerability is discovered or a critical issue occurs, the contract can be halted temporarily to prevent further damage.