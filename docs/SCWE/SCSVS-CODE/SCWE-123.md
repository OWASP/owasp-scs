---
title: Corrupt Free Memory Pointer in Assembly
id: SCWE-123
alias: corrupt-free-memory-pointer
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [693]
status: new
---

## Relationships
- CWE-693: Protection Mechanism Failure  
  [https://cwe.mitre.org/data/definitions/693.html](https://cwe.mitre.org/data/definitions/693.html)

## Description
Inline assembly that writes to memory without preserving the Solidity free-memory pointer (at `0x40`) can corrupt ABI encoding for later calls or returns. Downstream decodes may misread buffers, leading to unexpected reverts or data leaks.

## Remediation
- Save and restore the free-memory pointer when using custom memory writes.
- Prefer Solidity primitives unless assembly is necessary; encapsulate unsafe sections.
- Use formalized patterns for encoding/decoding (e.g., `abi.encode`) to avoid manual pointer math.

## Examples

### Vulnerable
```solidity
assembly {
    mstore(0x40, add(0x40, 0x20)) // advances but later writes may clobber
    mstore(0x00, value)
}
// subsequent abi.encode may read corrupted area
```

### Fixed
```solidity
assembly {
    let memPtr := mload(0x40)
    mstore(memPtr, value)
    mstore(0x40, add(memPtr, 0x20))
}
```

