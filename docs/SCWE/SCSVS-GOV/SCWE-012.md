---
title: Lack of Multisig Governance
id: SCWE-012
alias: lack-of-multisig-governance
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-1]
  cwe: [285]
status: new
---

## Relationships
- CWE-285: Improper Authorization  
  [https://cwe.mitre.org/data/definitions/285.html](https://cwe.mitre.org/data/definitions/285.html)

## Description
Lack of multisig governance occurs when critical smart contract functions, such as upgrades, fund withdrawals, or parameter changes, are controlled by a single entity. This creates a **single point of failure**, increasing the risk of **compromise, insider abuse, or unauthorized access**. Without multisig governance, attackers or malicious actors can easily exploit privileged functions if the private key of a single administrator is compromised.

Key risks associated with missing multisig governance:
- **Centralization Risk**: A single entity can control and modify key contract parameters.
- **Single Point of Failure**: Loss or compromise of the owner's private key can result in catastrophic consequences.
- **Unauthorized Access**: An attacker gaining control of the private key can execute privileged functions without approval.
- **Lack of Accountability**: Decisions are made unilaterally, reducing transparency and security.

## Remediation
- **Implement a Multisig Wallet**: Use multisignature schemes (e.g., Gnosis Safe) to require multiple signers for critical transactions.
- **Role-Based Access Control (RBAC)**: Assign multiple roles with different privileges to prevent centralized control.
- **Timelocks for Critical Functions**: Introduce a delay for privileged actions, allowing time for community intervention if needed.
- **On-Chain Governance Mechanisms**: Decentralize decision-making using **DAO-based governance** where applicable.

## Examples

### Example of a Contract Without Multisig Governance (Centralized Owner)

```solidity
pragma solidity ^0.8.0;

contract CentralizedGovernance {
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    function upgradeContract(address newContract) public {
        require(msg.sender == owner, "Only owner can upgrade");
        // ❌ Only a single owner can perform critical actions
    }

    function withdrawFunds(address payable recipient, uint256 amount) public {
        require(msg.sender == owner, "Only owner can withdraw funds");
        recipient.transfer(amount); // ❌ No multisig verification
    }
}
```

- In this example, all governance actions depend on a single owner, making it a high-risk design.

### Refactored to Use Multisig Governance

```solidity
pragma solidity ^0.8.0;

interface IMultiSig {
    function submitTransaction(address destination, uint256 value, bytes calldata data) external;
}

contract SecureGovernance {
    IMultiSig public multisigWallet;

    constructor(address _multisigWallet) {
        multisigWallet = IMultiSig(_multisigWallet);
    }

    function upgradeContract(address newContract) public {
        bytes memory data = abi.encodeWithSignature("upgradeTo(address)", newContract);
        multisigWallet.submitTransaction(address(this), 0, data); // ✅ Requires multisig approval
    }

    function withdrawFunds(address payable recipient, uint256 amount) public {
        bytes memory data = abi.encodeWithSignature("transfer(address,uint256)", recipient, amount);
        multisigWallet.submitTransaction(address(this), 0, data); // ✅ Multisig verification for withdrawals
    }
}
```

- This improved version delegates authority to a multisig wallet, requiring multiple approvals before executing critical actions.
