---
title: Signature Malleability
id: SCWE-054
alias: signature-malleability
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-2]
  cwe: [345]
status: new
---

## Relationships  
- CWE-345: Insufficient Verification of Data Authenticity  
  [https://cwe.mitre.org/data/definitions/345.html](https://cwe.mitre.org/data/definitions/345.html)  

## Description
Signature malleability refers to the ability to modify a valid signature without changing its validity. This can occur when signatures are not properly verified or when certain components of a signature (like the `v`, `r`, and `s` values) can be altered while still producing a valid signature.

Attackers can modify a signature’s `s` value or flip `v` between 27 and 28, generating different valid signatures for the same message. This can lead to:

- Replay attacks, where transactions can be re-executed with modified signatures.
- Transaction hijacking, where a valid signature is altered to redirect funds or manipulate contract state.

## Remediation
To mitigate signature malleability, ensure that the signature verification process is robust. Use secure cryptographic libraries that properly handle signature validation, such as ECDSA or EdDSA with additional checks to prevent malleability. When verifying signatures, consider using a canonical format for signature components to avoid malleability.

### Vulnerable Contract Example- (Allows Signature Malleability)
```solidity
contract MalleableSignatureExample {
    function verifySignature(bytes32 message, uint8 v, bytes32 r, bytes32 s) public pure returns (bool) {
        address signer = ecrecover(message, v, r, s);  // Signature malleability risk
        return signer != address(0);
    }
}
```
- This contract does not restrict `s` values, allowing malleable signatures.
- Issue: The contract does not check if `s` is in the lower half of the `curve (s < secp256k1n/2)`, allowing multiple valid signatures for the same message.



### Fixed Contract Example- Prevents Signature Malleability)
```solidity
  pragma solidity ^0.8.0;

  import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

  contract SecureSignatureExample {
      using ECDSA for bytes32;

      function verifySignature(bytes32 message, bytes memory signature) public pure returns (address) {
          return message.toEthSignedMessageHash().recover(signature);
      }
  }
```

- Fix: Uses `OpenZeppelin’s ECDSA library`, which ensures `s` is in the lower half and restricts `v` to 27 or 28.
- Outcome: Prevents attackers from modifying valid signatures to create alternate, equally valid ones.
