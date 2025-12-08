---
title: Unauthorized Parameter Changes
id: SCWE-013
alias: unauthorized-parameter-changes
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-2]
  cwe: [494]
status: new
---

## Relationships
- CWE-233: Improper Handling of Parameters 
  [https://cwe.mitre.org/data/definitions/233.html](https://cwe.mitre.org/data/definitions/233.html)

## Description
Unauthorized parameter changes occur when privileged smart contract parameters—such as fees, governance rules, withdrawal limits, or security configurations—can be modified by a single entity or an unauthorized user. This can lead to **unexpected behavior, security risks, or financial loss** if an attacker gains access to the privileged account.

Key risks associated with unauthorized parameter changes:
- **Single Point of Control**: A centralized owner can unilaterally alter critical parameters, leading to governance concerns.
- **Malicious Modifications**: Attackers who exploit an access control flaw may change key parameters, resulting in stolen funds or manipulated contract logic.
- **Lack of Transparency**: Hidden or undocumented parameter changes can mislead users and investors, reducing trust.
- **Impact on DeFi Protocols**: Unauthorized changes to liquidity pool fees, interest rates, or reward mechanisms can disrupt incentives and harm protocol users.

## Remediation
- **Use Role-Based Access Control (RBAC)**: Assign granular roles and restrict who can modify key parameters.
- **Multisig Approval for Parameter Changes**: Require governance approval (e.g., Gnosis Safe) before making critical updates.
- **Timelocks for Parameter Changes**: Introduce time delays on modifications to allow community review and prevent instant malicious changes.
- **On-Chain Governance for DAOs**: Utilize decentralized governance mechanisms where stakeholders vote on parameter updates.
- **Emit Events for Transparency**: Log all parameter changes on-chain to ensure visibility and auditability.

## Examples

### Example of a Contract With Unauthorized Parameter Changes (Centralized Control)

```solidity
pragma solidity ^0.8.0;

contract RiskyContract {
    address public owner;
    uint256 public feeRate;

    constructor() {
        owner = msg.sender;
        feeRate = 5; // Default fee rate
    }

    function updateFeeRate(uint256 newRate) public {
        require(msg.sender == owner, "Only owner can update fee rate");
        feeRate = newRate; // ❌ Single entity can modify a critical parameter at any time
    }
}
```

- In this example, the owner can unilaterally change the fee rate, which poses a security risk.

### Refactored to Require Multisig and Timelocks

```solidity
pragma solidity ^0.8.0;

interface ITimelock {
    function queueTransaction(address target, uint256 value, bytes calldata data, uint256 eta) external;
    function executeTransaction(address target, uint256 value, bytes calldata data, uint256 eta) external;
}

contract SecureGovernance {
    ITimelock public timelock;
    uint256 public feeRate;

    constructor(address _timelock) {
        timelock = ITimelock(_timelock);
        feeRate = 5; // Default fee rate
    }

    function updateFeeRate(uint256 newRate) public {
        bytes memory data = abi.encodeWithSignature("setFeeRate(uint256)", newRate);
        timelock.queueTransaction(address(this), 0, data, block.timestamp + 2 days); // ✅ Adds delay before execution
    }

    function setFeeRate(uint256 newRate) public {
        require(msg.sender == address(timelock), "Only timelock can execute");
        feeRate = newRate;
    }
}
```

This improved version:
- Uses a Timelock contract to delay parameter changes, preventing instant unauthorized updates.
- Restricts execution to an approved governance mechanism, preventing a single actor from making direct changes.
