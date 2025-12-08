---
title: Insecure Signature Verification
id: SCWE-019
alias: insecure-signature-verification
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-AUTH]
  scsvs-scg: [SCSVS-AUTH-2]
  cwe: [347]
status: new
---

## Relationships
- CWE-347: Improper Verification of Cryptographic Signature
  [https://cwe.mitre.org/data/definitions/347.html](https://cwe.mitre.org/data/definitions/347.html)

## Description
Insecure signature verification occurs when a contract improperly verifies a cryptographic signature or fails to securely validate signatures, allowing attackers to forge or manipulate them. This vulnerability can allow unauthorized transactions or the bypassing of important security mechanisms, potentially leading to fraud, unauthorized access, or other attacks.

Common causes of insecure signature verification include:
- Not validating the signer's address.
- Using weak or outdated cryptographic libraries.
- Failing to check signature validity before processing actions.
- Incorrectly handling the signature format.

## Remediation
- **Verify signatures properly:** Always verify that the signature matches the intended signer by using the `ecrecover` function for Ethereum addresses and comparing the result to the expected signer address.
- **Use strong cryptographic methods:** Ensure the use of robust cryptographic techniques and libraries. Avoid using outdated or weak algorithms.
- **Use secure signature formats:** Make sure that signature formats are validated properly (e.g., ensure proper handling of `v`, `r`, `s` values in Ethereum signatures).
- **Implement checks before acting on the signature:** Always perform checks for valid signature and relevant parameters before executing any logic that could be influenced by the signature.

## Examples

### Insecure Signature Verification

```solidity
pragma solidity ^0.8.0;

contract InsecureSignatureExample {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    // Insecure signature verification: does not properly validate the signature
    function executeTransaction(bytes32 hash, uint8 v, bytes32 r, bytes32 s) public {
        address signer = ecrecover(hash, v, r, s);  // Signature verification
        if (signer == owner) {
            // Execute some sensitive action
        }
    }
}
```
In the insecure version, the contract checks if the signature corresponds to the owner but does not properly validate or handle potential issues with the signature, such as its format or correctness.

### Fixed Signature Verification
```solidity
pragma solidity ^0.8.0;

contract SecureSignatureExample {
    address public owner;

    constructor() public {
        owner = msg.sender;
    }

    // Secure signature verification: properly checks signature and signer
    function executeTransaction(bytes32 hash, uint8 v, bytes32 r, bytes32 s) public {
        address signer = ecrecover(hash, v, r, s);
        require(signer == owner, "Invalid signature");  // Ensure valid signature before proceeding
        // Execute some sensitive action
    }
}
```
In the fixed version, we use the `require()` function to ensure the signature matches the owner's address, thereby improving security by preventing unauthorized access or actions.
