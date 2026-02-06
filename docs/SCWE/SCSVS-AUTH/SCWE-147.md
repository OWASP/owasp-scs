---
title: Permit or Meta-Transaction Signatures Without Expiration
id: SCWE-147
alias: missing-signature-expiration
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
Permit (EIP-2612) and meta-transaction signatures that omit a `deadline` or `expiry` parameter can be replayed indefinitely once obtained. An attacker who captures a valid signature (e.g., via phishing or a compromised frontend) can submit it at any future time. SCWE-105 covers domain separator and nonce; this weakness specifically addresses the absence of expiration.

## Remediation
- Include a `deadline` (or `expiry`) in the signed message and enforce `require(block.timestamp <= deadline, "Expired")` when processing the signature.
- Use EIP-712 structured data with a deadline field.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract MetaTx {
    function execute(address signer, bytes32 hash, uint8 v, bytes32 r, bytes32 s) external {
        require(ecrecover(hash, v, r, s) == signer, "Bad sig");
        // No deadline: signature valid forever
        _execute(signer);
    }
}
```

### Fixed
```solidity
function execute(address signer, uint256 deadline, bytes32 hash, uint8 v, bytes32 r, bytes32 s) external {
    require(block.timestamp <= deadline, "Expired");
    require(ecrecover(hash, v, r, s) == signer, "Bad sig");
    _execute(signer);
}
```
**Note:** The `hash` must be computed from EIP-712 structured data that includes the `deadline` field so the signature cannot be replayed after expiry.
