---
title: ECDSA Nonce Reuse
id: SCWE-114
alias: ecdsa-nonce-reuse
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-1]
  cwe: [323]
status: new
---

## Relationships
- CWE-323: Reusing a Nonce, Key Pair in Encryption  
  [https://cwe.mitre.org/data/definitions/323.html](https://cwe.mitre.org/data/definitions/323.html)

## Description
Reusing the same ECDSA nonce (`k`) across signatures (or using predictable nonces) leaks the private key. Contracts that accept off-chain signatures for permits, meta-txs, or governance can be compromised if signing infrastructure mismanages nonces.

## Remediation
- Use battle-tested libraries/wallets that generate unique, random or RFC6979 deterministic nonces per message.
- Monitor and rotate keys if nonce reuse is suspected; support key revocation on-chain.
- Avoid custom signing code or manual nonce management in scripts.

## Examples

### Vulnerable
```solidity
// Off-chain signer reuses k for two messages:
// sig1 = (r, s1) with k
// sig2 = (r, s2) with same k => private key can be recovered
```

### Fixed
```solidity
// Use libraries/wallets that follow RFC6979 and never reuse k.
// No on-chain code change prevents k reuse; the contract must allow key rotation.
```

