---
title: Insecure Upgradeable Proxy Design
id: SCWE-005
alias: insecure-upgradeable-proxy-design
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-2]
  cwe: [668]
status: new
---

## Relationships
- CWE-668: Exposure of Resource to Wrong Sphere
  [https://cwe.mitre.org/data/definitions/668.html](https://cwe.mitre.org/data/definitions/668.html)

## Description
Insecure upgradeable proxy designs occur when a smart contract implements an upgradeable proxy pattern without properly securing or validating upgrades. This may allow unauthorized actors to change the contract’s logic, possibly introducing malicious behavior. It often happens when the upgrade functionality lacks proper access controls or when there is no timelock to delay the upgrade, giving malicious actors an opportunity to exploit the contract.

This vulnerability can lead to critical failures, including the redirection of contract calls to malicious logic or unauthorized updates that compromise the integrity of the contract.

## Remediation
- **Access Control:** Ensure only trusted parties (e.g., contract owners, multisig wallets) can perform upgrades.
- **Timelock Mechanism:** Implement a timelock to delay upgrades and provide transparency.
- **Transparent Proxy Pattern:** Use patterns that prevent unauthorized contract logic changes, such as the Transparent Proxy Pattern.
- **Audit Proxy Logic Regularly:** Conduct regular audits to ensure that the upgrade mechanism is secure and follows best practices.

## Examples

### Vulnerable Proxy Contract

```solidity
pragma solidity ^0.4.0;

contract VulnerableProxy {
    address public implementation;
    address public owner;

    function setImplementation(address _implementation) public {
        require(msg.sender == owner, "Only owner can set implementation");
        implementation = _implementation;
    }

    function () public payable {
        address _impl = implementation;
        require(_impl != address(0), "Implementation address is zero");
        assembly {
            let result := delegatecall(gas, _impl, add(msg.data, 0x20), mload(msg.data), 0, 0)
            let size := returndatasize
            let ptr := mload(0x40)
            return(ptr, size)
        }
    }
}
```
In this example, the `VulnerableProxy` contract allows the owner to update the implementation contract. If the owner is compromised, they can point the proxy to a malicious implementation, allowing the attacker to control the contract's logic.

### Fixed Proxy Contract with Secure Upgrade Mechanism

```solidity

pragma solidity ^0.4.0;

contract SecureProxy {
    address public implementation;
    address public owner;
    uint public lastUpgradeTime;
    uint public upgradeDelay = 1 days;  // 24 hours delay before upgrade

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }

    modifier upgradeable() {
        require(now >= lastUpgradeTime + upgradeDelay, "Upgrade not allowed yet");
        _;
    }

    function setImplementation(address _implementation) public onlyOwner upgradeable {
        implementation = _implementation;
        lastUpgradeTime = now; // Update the last upgrade time
    }

    function () public payable {
        address _impl = implementation;
        require(_impl != address(0), "Implementation address is zero");
        assembly {
            let result := delegatecall(gas, _impl, add(msg.data, 0x20), mload(msg.data), 0, 0)
            let size := returndatasize
            let ptr := mload(0x40)
            return(ptr, size)
        }
    }
}
```

In the fixed `SecureProxy` contract, the following changes have been made:

- Access Control: The `onlyOwner` modifier ensures that only the contract owner can update the proxy’s implementation.
- Timelock Mechanism: The `upgradeable` modifier adds a delay (set to 1 day in this example) to prevent rapid contract upgrades. The contract cannot be upgraded until the specified time has passed since the last upgrade.
- Secure Upgrade Logic: The proxy logic is updated only after passing the necessary access control and timelock checks.