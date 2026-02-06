---
title: Unverified Cross-Chain Message Proofs
id: SCWE-108
alias: unverified-cross-chain-proofs
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-3]
  cwe: [345]
status: new
---

## Relationships
- CWE-345: Insufficient Verification of Data Authenticity  
  [https://cwe.mitre.org/data/definitions/345.html](https://cwe.mitre.org/data/definitions/345.html)

## Description
Relayers may deliver fabricated payloads if the destination contract does not validate Merkle proofs, light-client headers, or signatures that attest to the message on the source chain. Forged messages can mint wrapped assets or execute arbitrary calls.

## Remediation
- Verify message inclusion against a trusted root (Merkle/Patricia proof) or light-client header.
- Validate signatures from authorized validators and enforce quorum thresholds.
- Reject messages that fail proof verification or originate from unrecognized relayers.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Inbox {
    function deliver(bytes calldata payload) external {
        _process(payload); // assumes relayer is honest
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Inbox {
    address[] public validators;
    uint256 public constant QUORUM = 2;

    function deliver(bytes calldata payload, bytes[] calldata sigs) external {
        require(_verifyQuorum(payload, sigs) >= QUORUM, "invalid proof");
        _process(payload);
    }
}
```

