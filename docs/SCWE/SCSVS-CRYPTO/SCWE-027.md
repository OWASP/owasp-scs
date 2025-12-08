---
title: Vulnerable Cryptographic Algorithms
id: SCWE-027
alias: vulnerable-cryptographic-algorithms
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-2]
  cwe: [327]
status: new
---

## Relationships
- **CWE-327:** Use of a Broken or Risky Cryptographic Algorithm  
  [CWE-327 Link](https://cwe.mitre.org/data/definitions/327.html)

## Description
Vulnerable cryptographic algorithms refer to the use of outdated or insecure cryptographic algorithms, such as MD5 or SHA-1. This can lead to:
- Exploitation of the contract’s logic.
- Loss of funds or data.
- Reduced trust in the contract’s security.

## Remediation
- **Use secure algorithms:** Leverage modern cryptographic algorithms like SHA-256 or Keccak-256.
- **Avoid deprecated algorithms:** Do not use algorithms known to be insecure.
- **Test thoroughly:** Conduct extensive testing to ensure cryptographic security.

## Examples
- **Vulnerable Algorithm**
    ```solidity
    pragma solidity ^0.8.0;

    contract VulnerableAlgorithm {
        function hashData(bytes memory data) public pure returns (bytes32) {
            return sha256(data); // Insecure algorithm
        }
    }
    ```

- **Secure Algorithm**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureAlgorithm {
        function hashData(bytes memory data) public pure returns (bytes32) {
            return keccak256(data); // Secure algorithm
        }
    }
    ```

---
