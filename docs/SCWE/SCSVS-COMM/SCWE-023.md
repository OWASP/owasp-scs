---
title: Lack of Communication Authenticity
id: SCWE-023
alias: lack-of-communication-authenticity
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
Lack of communication authenticity refers to the failure to verify the authenticity of messages or transactions. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data.
- Exploitation of the contract's logic.

## Remediation
- **Use signatures:** Require signed messages for critical actions.
- **Validate inputs:** Ensure all messages are properly validated before processing.
- **Implement secure communication:** Use secure protocols and libraries for communication.

## Examples
- **Lack of Authenticity**
    ```solidity
    pragma solidity ^0.8.0;

    contract NoAuthenticity {
        function processMessage(bytes memory message) public {
            // Process message without authenticity check
        }
    }
    ```

- **Authentic Communication**
    ```solidity
    pragma solidity ^0.8.0;

    import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

    contract AuthenticCommunication {
        using ECDSA for bytes32;

        function processMessage(bytes memory message, bytes memory signature) public {
            bytes32 messageHash = keccak256(message);
            address signer = messageHash.recover(signature);
            require(signer == msg.sender, "Invalid signature");
            // Process message
        }
    }
    ```

---