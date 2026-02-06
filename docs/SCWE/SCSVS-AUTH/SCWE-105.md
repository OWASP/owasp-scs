---
title: Permit Signature Replay via Missing Domain Separator or Nonce
id: SCWE-105
alias: permit-signature-replay
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
Improper EIP-2612 permit implementations that omit chain-specific domain separators, do not increment nonces, or ignore expiration allow signatures to be replayed across chains or multiple times. Attackers can repeatedly approve spending or re-use permits on forked networks.

## Remediation
- Build EIP-712 domain separators including `name`, `version`, `chainId`, and `verifyingContract`.
- Maintain per-owner nonces and increment on every successful permit.
- Enforce deadlines and reject expired signatures.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;
contract Token {
    mapping(address => uint256) public nonces;

    function permit(address owner, address spender, uint256 value, bytes calldata sig) external {
        // missing chainId/domain checks, nonce not incremented
        address signer = ecrecover(/* simplified */);
        require(signer == owner, "bad sig");
        // allowance set here...
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;
contract Token {
    bytes32 public DOMAIN_SEPARATOR;
    mapping(address => uint256) public nonces;

    constructor() {
        DOMAIN_SEPARATOR = keccak256(abi.encode(
            keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
            keccak256(bytes("Token")),
            keccak256(bytes("1")),
            block.chainid,
            address(this)
        ));
    }

    function permit(/* params */) external {
        // verify typed data with nonce and deadline, then increment nonce
        nonces[owner] += 1;
    }
}
```

