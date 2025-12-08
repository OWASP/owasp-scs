---
title: Missing Protection against Signature Replay Attacks
id: SCWE-055
alias: missing-signature-replay-protection
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-1]
  cwe: [294]
status: new
---

## Relationships  
- CWE-294: Authentication Bypass by Capture-replay  
  [https://cwe.mitre.org/data/definitions/294.html](https://cwe.mitre.org/data/definitions/294.html)  

## Description
Signature replay attacks occur when a valid signature from a previous transaction is reused in a different context, such as a different transaction or contract call. Without proper protection, an attacker can capture and replay a signature, potentially bypassing authentication checks and causing unauthorized actions or transactions.

## Remediation
To prevent signature replay attacks, include additional checks that ensure the signature is valid for a specific transaction or context. This can be done by incorporating unique identifiers like a nonce, timestamp, or a unique transaction hash into the signature to bind it to a specific use. Always verify that the signature is only valid for the intended action.

### Vulnerable Contract Example
```solidity
contract ReplayAttackExample {
    mapping(address => uint256) public nonces;

    function authenticate(bytes32 message, uint8 v, bytes32 r, bytes32 s) public {
        address signer = ecrecover(message, v, r, s);
        require(signer == msg.sender, "Invalid signature");
        // No protection against replay attacks; attacker can reuse the same signature
    }
}
```

### Fixed Contract Example
```solidity
  pragma solidity ^0.8.0;

  import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

  contract SecureReplayProtectionExample {
      using ECDSA for bytes32;

      mapping(address => uint256) public nonces;

      function authenticate(bytes32 message, bytes memory signature) public {
          uint256 nonce = nonces[msg.sender]++;
          bytes32 messageWithContext = keccak256(abi.encodePacked(message, nonce, block.chainid));  
          address signer = messageWithContext.toEthSignedMessageHash().recover(signature);
          require(signer == msg.sender, "Invalid signature");
      }
  }
```
**Fixes Implemented:**
-  Binds signature to a nonce (ensuring it's only usable once).
-  Includes `chainId` (prevents cross-chain replay attacks).
- Uses OpenZeppelin’s ECDSA library (avoids signature malleability risks).

---