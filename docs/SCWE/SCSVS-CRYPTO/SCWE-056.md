---
title: Lack of Proper Signature Verification
id: SCWE-056
alias: lack-proper-signature-verification
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-1]
  cwe: [345]
status: new
---

## Relationships  
- CWE-345: Insufficient Verification of Data Authenticity  
  [https://cwe.mitre.org/data/definitions/345.html](https://cwe.mitre.org/data/definitions/345.html)  

## Description
This vulnerability occurs when a smart contract fails to properly verify whether a signature was produced by an authorized entity.
In Ethereum, contracts often use `ecrecover` to check signatures, but failing to validate who signed the message allows:

- Unauthorized transactions, where attackers submit signatures from any key.
- Replay attacks, where valid signatures are reused to repeat actions.
- Malicious contract state manipulation, where attackers gain unauthorized access.

## Remediation
To mitigate this vulnerability, always implement proper signature verification using secure cryptographic methods. Use the `ecrecover` function to recover the signer’s address and ensure that the recovered address matches the expected address. Additionally, verify that the signature is valid for the intended message or transaction and that the signer is authorized to perform the action.

### Vulnerable Contract Example- (Lack of Signer Verification)
```solidity
contract SignatureVerificationExample {
    function authenticate(bytes32 message, uint8 v, bytes32 r, bytes32 s) public view returns (address) {
        address signer = ecrecover(message, v, r, s);
        return signer;  // No further validation of the signer or message
    }
}
```
- Issue: The contract does not check if the recovered address matches an authorized signer.
- Exploit: Any valid ECDSA signature can be used, even from an attacker’s key.


### Fixed Contract Example- (Proper Signature Verification)
```solidity
    pragma solidity ^0.8.0;

    import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

    contract SecureSignatureVerificationExample {
        using ECDSA for bytes32;

        address public authorizedSigner;

        constructor(address _authorizedSigner) {
            require(_authorizedSigner != address(0), "Invalid signer");
            authorizedSigner = _authorizedSigner;
        }

        function authenticate(bytes32 message, bytes memory signature) public view returns (bool) {
            address signer = message.toEthSignedMessageHash().recover(signature);
            require(signer == authorizedSigner, "Unauthorized signer"); // Proper validation
            return true;
        }
    }
```
- Fix: The contract now explicitly checks that the recovered address matches `authorizedSigner`.
- Outcome: Prevents attackers from submitting arbitrary signatures and ensures only authorized signatures are accepted.
