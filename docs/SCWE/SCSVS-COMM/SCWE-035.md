---
title: Insecure Delegatecall Usage
id: SCWE-035
alias: insecure-delegatecall-usage
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [250]
status: new
---

## Relationships
- CWE-250: Execution with Unnecessary Privileges  
  [CWE-250 Link](https://cwe.mitre.org/data/definitions/250.html)

## Description  
Insecure delegatecall usage refers to vulnerabilities that arise when using `delegatecall` to execute code from another contract. This can lead to:
- Unauthorized access to sensitive functions.
- Exploitation of vulnerabilities in the called contract.
- Loss of funds or data.

## Remediation
- **Validate targets:** Ensure the target contract is trusted and secure.
- **Restrict permissions:** Restrict `delegatecall` usage to trusted addresses.
- **Test thoroughly:** Conduct extensive testing to ensure `delegatecall` is used securely.

## Examples
- **Insecure Delegatecall Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract InsecureDelegatecall {
        function executeDelegatecall(address target, bytes memory data) public {
            (bool success, ) = target.delegatecall(data); // ❌ No validation, attacker-controlled contract can be used
            require(success, "Delegatecall failed");
        }
    }
    ```
- Anyone can call `executeDelegatecall()` with a malicious contract, which will execute arbitrary code within the caller’s context.
- Can lead to theft of funds, privilege escalation, or state corruption.

- **Secure Delegatecall Usage**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureDelegatecall {
        address public owner;
        address public trustedTarget;

        modifier onlyOwner() {
            require(msg.sender == owner, "Not authorized");
            _;
        }

        constructor(address _trustedTarget) {
            owner = msg.sender;
            trustedTarget = _trustedTarget;
        }

        function updateTrustedTarget(address _newTarget) public onlyOwner {
            require(isTrusted(_newTarget), "Untrusted target");
            trustedTarget = _newTarget;
        }

        function executeDelegatecall(bytes memory data) public onlyOwner {
            require(trustedTarget != address(0), "Invalid target");
            (bool success, ) = trustedTarget.delegatecall(data);
            require(success, "Delegatecall failed");
        }

        function isTrusted(address _target) internal pure returns (bool) {
            // Implement further checks if needed
            return _target != address(0);
        }
    }
    ```

Fixes:
- Only the contract owner can update trustedTarget.
- Validation of trusted target before executing delegatecall.
- Prevents arbitrary execution by restricting calls to trustedTarget.
