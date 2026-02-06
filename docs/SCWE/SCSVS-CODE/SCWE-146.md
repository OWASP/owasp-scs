---
title: Improper Use of try/catch Leading to Silent Failures
id: SCWE-146
alias: incorrect-try-catch-error-handling
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [390]
status: new
---

## Relationships
- CWE-390: Detection of Error Condition Without Action  
  [https://cwe.mitre.org/data/definitions/390.html](https://cwe.mitre.org/data/definitions/390.html)

## Description
Solidity 0.6+ `try/catch` allows catching reverts from external calls. If the catch block does not properly handle the failure—e.g., proceeds without reverting, leaves state inconsistent, or swallows the error without logging—the contract can continue execution under incorrect assumptions. Silent failures can lead to fund loss, corrupted state, or exploitable inconsistencies.

## Remediation
- In catch blocks, either revert with a clear message or update state to reflect the failure (e.g., mark operation as failed, emit event).
- Avoid proceeding with critical logic when the external call failed unless the failure is explicitly handled and documented.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Aggregator {
    function swap(address router, bytes calldata data) external {
        try IRouter(router).swap(data) returns (uint256 amountOut) {
            transferToUser(msg.sender, amountOut);
        } catch {
            // Silent: user gets nothing but tx succeeds; state may be inconsistent
        }
    }
}
```

### Fixed
```solidity
function swap(address router, bytes calldata data) external {
    try IRouter(router).swap(data) returns (uint256 amountOut) {
        transferToUser(msg.sender, amountOut);
    } catch {
        revert("Swap failed");
    }
}
```
**Fix:** Revert in the catch block so the transaction fails. Avoid `catch (bytes memory reason)` with string concatenation—`reason` may be a custom error selector, not a string.
