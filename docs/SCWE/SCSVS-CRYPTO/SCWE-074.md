---
title: Hash Collisions with Multiple Variable Length Arguments
id: SCWE-074
alias: hash-collisions-multiple-variable-length-arguments
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-2]
  cwe: [347]
status: new
---

## Relationships  
- CWE-347: Improper Verification of Cryptographic Signature  
  [https://cwe.mitre.org/data/definitions/347.html](https://cwe.mitre.org/data/definitions/347.html)  

## Description
When hashing multiple variable-length arguments, there is a potential risk of hash collisions, which can occur if two different sets of inputs produce the same hash output. This vulnerability is particularly relevant in situations where hashes are used as identifiers, signatures, or keys, and collisions may lead to incorrect behavior or security breaches, such as false validation of signatures or unexpected contract logic execution.

## Remediation
To prevent hash collisions, use a strong cryptographic hashing function like `keccak256` or `sha256`, and ensure that the inputs to the hash function are well-structured. Consider combining different sources of entropy (e.g., timestamps, nonces) and always verify the integrity of the data before trusting a hash.

### Vulnerable Contract Example
```solidity
contract Example {
    function verifyData(bytes memory data1, bytes memory data2) public pure returns (bytes32) {
        // Vulnerable to hash collisions with multiple variable-length arguments
        return keccak256(abi.encodePacked(data1, data2));  // Possible collision risk
    }
}
```


### Fixed Contract Example
```solidity
contract Example {
    function verifyData(bytes memory data1, bytes memory data2) public pure returns (bytes32) {
        // Safe way to hash multiple variable-length arguments
        return keccak256(abi.encode(data1, data2));  // More secure handling of variable-length inputs
    }
}
```