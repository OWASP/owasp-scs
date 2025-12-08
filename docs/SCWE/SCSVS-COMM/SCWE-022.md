---
title: Message Replay Vulnerabilities
id: SCWE-022
alias: message-replay-vulnerabilities
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [294]
status: new
---

## Relationships
- CWE-294: Authentication Bypass by Capture-replay  
  [CWE-294 Link](https://cwe.mitre.org/data/definitions/294.html)

## Description  
Message replay vulnerabilities occur when an attacker can reuse a valid message or transaction to perform unauthorized actions. This can lead to:
- Unauthorized access to sensitive functions.
- Loss of funds or data.
- Exploitation of the contract's logic.

## Remediation
- **Use nonces:** Include a unique nonce in each message to prevent reuse.
- **Validate timestamps:** Ensure messages are only valid for a limited time.
- **Implement replay protection:** Use established libraries or mechanisms to prevent replay attacks.

## Examples
- **Vulnerable to Replay Attacks**
    ```solidity
    pragma solidity ^0.8.0;

    contract ReplayVulnerable {
        function processMessage(bytes memory message) public {
            // Process message without replay protection
        }
    }
    ```

- **Protected Against Replay Attacks**
    ```solidity
    pragma solidity ^0.8.0;

    contract ReplayProtected {
        mapping(bytes32 => bool) public usedMessages;

        function processMessage(bytes memory message, uint nonce, uint chainId) public {
            bytes32 messageHash = keccak256(abi.encodePacked(message, nonce, chainId));
            require(!usedMessages[messageHash], "Message already used");
            usedMessages[messageHash] = true;
            // Process message
        }
    }
    ```

---