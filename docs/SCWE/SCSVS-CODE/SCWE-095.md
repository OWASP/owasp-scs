---
title: Missing Destination Address Size Check
id: SCWE-095
alias: Missing-Destination-Address-Size-Check
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [20]
status: new
---

## Relationships
- **CWE-20**: [Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

## Description  
This weakness occurs when a smart contract function accepts a `bytes32` parameter intended to represent an Ethereum address without validating its size. Ethereum addresses are 20 bytes, and using a `bytes32` type without proper checks can lead to incorrect address interpretation, potentially causing funds to be sent to unintended addresses.  

This is especially risky in cross-chain, bridging, or interoperability contexts where address formats and padding conventions may vary. If the upper 12 bytes of the `bytes32` value are non-zero (or the value is otherwise malformed), naive casting to `address` can silently truncate or misinterpret the actual destination, leading to irreversible fund loss or misdirection.

## Impact  
Failure to validate `bytes32` inputs that represent addresses may enable:
- Accidental misdirection of funds to unintended addresses due to truncation.  
- Loss of funds in production deployments, as ETH/token transfers are irreversible.  
- Exploitation by attackers who craft inputs with malicious upper bits to redirect value.  
- Integration fragility in cross-chain workflows where address encoding/padding differs.  

## Remediation  
- Avoid using `bytes32` to represent addresses when possible; prefer the native `address` type.  
- If `bytes32` is required for protocol compatibility, validate that the upper 12 bytes are zero before casting: ensure `uint256(destination) >> 160 == 0`.  
- Centralize the validation and conversion logic in a dedicated helper to prevent inconsistent handling.  
- Add unit tests and fuzzing to verify that malformed `bytes32` values are rejected.  

## Examples  
- **❌ Vulnerable Code (Lack of address size validation)**  
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Example {
    mapping(address => uint256) public balances;

    // Deposit ETH
    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // ❌ Vulnerable: destinationAddress is bytes32, not validated
    function withdraw(bytes32 destinationAddress, uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        _debitFrom(msg.sender, amount);
        _send(destinationAddress, amount);
    }

    // Internal debit
    function _debitFrom(address from, uint256 amount) internal {
        balances[from] -= amount;
    }

    // Internal send
    function _send(bytes32 destinationAddress, uint256 amount) internal {
        address payable dest = payable(address(uint160(uint256(destinationAddress))));
        (bool ok, ) = dest.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```

- **✅ Safe Code (Validation of address size)**  
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Example {
    mapping(address => uint256) public balances;

    // Deposit ETH
    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // ✅ Safe: Validates destinationAddress size
    function withdraw(bytes32 destinationAddress, uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        require(uint256(destinationAddress) >> 160 == 0, "Invalid address: upper 12 bytes must be zero");
        _debitFrom(msg.sender, amount);
        _send(destinationAddress, amount);
    }

    // Internal debit
    function _debitFrom(address from, uint256 amount) internal {
        balances[from] -= amount;
    }

    // Internal send
    function _send(bytes32 destinationAddress, uint256 amount) internal {
        address payable dest = payable(address(uint160(uint256(destinationAddress))));
        (bool ok, ) = dest.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```


