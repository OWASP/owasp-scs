---
title: Unauthenticated Meta-Transactions
id: SCWE-106
alias: unauthenticated-meta-transactions
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
Meta-transaction forwarders that relay calls without verifying the signer, nonce, chain, or expiry let relayers execute arbitrary actions on behalf of victims. Missing replay protection allows the same signed request to be executed multiple times.

## Remediation
- Verify EIP-712 typed data signatures against the declared signer.
- Track and increment per-signer nonces; enforce deadlines and chainId.
- Restrict trusted forwarders and sanitize `msg.sender`/`msg.data` assumptions in downstream calls.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Forwarder {
    function relay(address target, bytes calldata data) external {
        (bool ok, ) = target.call(data); // no signature or nonce check
        require(ok, "call failed");
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Forwarder {
    mapping(address => uint256) public nonces;

    function relay(address target, bytes calldata data, uint256 nonce, uint256 deadline, bytes calldata sig) external {
        require(block.timestamp <= deadline, "expired");
        bytes32 digest = keccak256(abi.encode(target, data, nonce, block.chainid, deadline));
        address signer = ECDSA.recover(digest, sig);
        require(nonce == nonces[signer]++, "bad nonce");
        (bool ok, ) = target.call(data);
        require(ok, "call failed");
    }
}
```

