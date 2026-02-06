---
title: Missing Replay Nonce per Bridge Lane
id: SCWE-133
alias: missing-bridge-nonce
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-1]
  cwe: [294]
status: new
---

## Relationships
- CWE-294: Authentication Bypass by Capture-replay  
  [https://cwe.mitre.org/data/definitions/294.html](https://cwe.mitre.org/data/definitions/294.html)

## Description
Bridge receivers that do not track nonces per source chain/sender allow the same message to be replayed, causing duplicate mints or withdrawals. Forked chains can also replay historical messages if lanes are not isolated.

## Remediation
- Maintain monotonically increasing nonces per (sourceChain, sourceSender).
- Reject messages with reused or out-of-order nonces.
- Bind nonces into signed payloads or proofs to prevent tampering.

## Examples

### Vulnerable
```solidity
function receive(bytes calldata payload) external {
    _execute(payload); // no nonce tracking
}
```

### Fixed
```solidity
mapping(uint256 => mapping(address => uint256)) public nonce;

function receive(uint256 srcChain, address src, uint256 n, bytes calldata payload) external {
    require(n == nonce[srcChain][src]++, "replay");
    _execute(payload);
}
```

