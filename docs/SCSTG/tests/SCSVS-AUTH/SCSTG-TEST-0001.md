---
id: SCSTG-TEST-0001
scsvs_cg_id:
- SCSVS-AUTH
scsvs_scg_id:
- SCSVS-AUTH-1
platform: []
title: Testing Multi-Signature Schemes
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0001 
---

Ensure that multi-signature schemes are implemented for critical operations, requiring approvals from multiple authorized parties to enhance security and reduce the risk of unauthorized actions.

- Verify that the multi-signature logic ensures a configurable threshold of approvals before executing sensitive operations.  
- Confirm that all signers are authenticated and that duplicate signatures are rejected.  
- Test edge cases, such as insufficient approvals or tampered data.

```solidity
// Example of multi-signature scheme
pragma solidity ^0.8.0;

contract MultiSigWallet {
    address[] public owners;
    uint public requiredApprovals;
    mapping(address => bool) public isOwner;
    mapping(uint => mapping(address => bool)) public approvals;

    struct Transaction {
        address to;
        uint value;
        bool executed;
    }

    Transaction[] public transactions;

    constructor(address[] memory _owners, uint _requiredApprovals) {
        require(_owners.length > 0, "Owners required");
        require(_requiredApprovals > 0 && _requiredApprovals <= _owners.length, "Invalid approval count");

        for (uint i = 0; i < _owners.length; i++) {
            isOwner[_owners[i]] = true;
        }
        owners = _owners;
        requiredApprovals = _requiredApprovals;
    }

    function submitTransaction(address _to, uint _value) public {
        require(isOwner[msg.sender], "Not an owner");
        transactions.push(Transaction({to: _to, value: _value, executed: false}));
    }

    function approveTransaction(uint _txIndex) public {
        require(isOwner[msg.sender], "Not an owner");
        require(!approvals[_txIndex][msg.sender], "Already approved");

        approvals[_txIndex][msg.sender] = true;
    }

    function executeTransaction(uint _txIndex) public {
        require(transactions[_txIndex].executed == false, "Already executed");

        uint approvalCount = 0;
        for (uint i = 0; i < owners.length; i++) {
            if (approvals[_txIndex][owners[i]]) {
                approvalCount++;
            }
        }

        require(approvalCount >= requiredApprovals, "Not enough approvals");

        transactions[_txIndex].executed = true;
        payable(transactions[_txIndex].to).transfer(transactions[_txIndex].value);
    }

    receive() external payable {}
}
```
Review the logic to ensure all approvals are validated before execution, duplicate approvals are prevented, and transaction data integrity is maintained. Test with various approval scenarios to verify proper handling of edge cases.