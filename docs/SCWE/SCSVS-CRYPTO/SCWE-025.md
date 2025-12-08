---
title: Improper Cryptographic Key Management
id: SCWE-025
alias: improper-cryptographic-key-management
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-1]
  cwe: [310]
status: new
---

## Relationships
- CWE-310: Cryptographic Issues  
  [CWE-310 Link](https://cwe.mitre.org/data/definitions/310.html)

## Description  
Improper cryptographic key management refers to the failure to securely generate, store, or use cryptographic keys. This can lead to:
- Unauthorized access to sensitive data.
- Exploitation of the contract's logic.
- Loss of funds or data.

## Remediation
- **Use secure key management:** Leverage secure key management systems or libraries.
- **Avoid hardcoding keys:** Never hardcode cryptographic keys in the contract.
- **Regularly rotate keys:** Periodically update cryptographic keys to reduce risks.

## Examples
- **Improper Key Management**
    ```solidity
    pragma solidity ^0.8.0;

    contract ImproperKeyManagement {
        bytes32 private key = keccak256("insecure-key"); // Hardcoded key
    }
    ```

- **Proper Key Management**
    ```solidity
    pragma solidity ^0.8.0;

    contract ProperKeyManagement {
        bytes32 private key;

        constructor(bytes32 _key) {
            key = _key; // Configurable key
        }
    }
    ```