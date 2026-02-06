---
title: Low-Level Call to Non-Contract Address
id: SCWE-134
alias: call-to-non-contract-address
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMM]
  scsvs-scg: [SCSVS-COMM-1]
  cwe: [252]
status: new
---

## Relationships
- CWE-252: Unchecked Return Value  
  [https://cwe.mitre.org/data/definitions/252.html](https://cwe.mitre.org/data/definitions/252.html)

## Description
When using low-level `call`, `staticcall`, or `delegatecall` to a user-supplied or dynamic address, the target may be an EOA (externally owned account) with no contract code. In that case, the call returns `success = true` and empty return data, but no code executes. Contracts that assume the target performed logic (e.g., a callback, validation, or state change) can proceed under false assumptions, leading to bypassed checks, unexecuted logic, or incorrect accounting.

## Remediation
- Verify that the target address contains code using `extcodesize` (or `address.code.length` in Solidity 0.8.12+) before low-level calls.
- Use allowlists for callable targets instead of accepting arbitrary addresses.
- Prefer high-level interface calls when the target is known to be a contract.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract PluginRegistry {
    function executeViaPlugin(address plugin, bytes calldata data) external {
        (bool ok, ) = plugin.call(data);
        require(ok, "plugin failed");
        // If plugin is an EOA, call "succeeds" but no code ran — logic may be bypassed
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract PluginRegistry {
    function executeViaPlugin(address plugin, bytes calldata data) external {
        require(plugin.code.length > 0, "target has no code");
        (bool ok, ) = plugin.call(data);
        require(ok, "plugin failed");
    }
}
```
