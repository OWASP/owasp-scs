---
title: Inadequate Gas Limit Handling
id: SCWE-036
alias: inadequate-gas-limit-handling
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-DEFI]
  scsvs-scg: [SCSVS-DEFI-1]
  cwe: [400]
status: new
---

## Relationships
- CWE-400: Uncontrolled Resource Consumption  
  [CWE-400 Link](https://cwe.mitre.org/data/definitions/400.html)

## Description  
Inadequate gas limit handling occurs when a contract fails to manage gas constraints efficiently, leading to performance bottlenecks and denial-of-service (DoS) risks. Poor gas handling can result in:
- Unoptimized execution: Unnecessary gas-heavy computations increasing costs.
- DoS vulnerabilities: Transactions failing due to excessive gas usage, blocking operations.
- Inefficient batch processing: Overloaded loops or storage updates causing out-of-gas (OOG) errors.

Unlike **SCWE-032**, which focuses on the protocol-level block gas limit, this issue arises due to poor gas management at the smart contract level.


## Remediation
- **Optimize gas usage:** Minimize gas consumption in contract operations.
- **Avoid unbounded loops:** Ensure loops have a fixed upper limit.
- **Test thoroughly:** Conduct extensive testing to ensure operations stay within gas limits.

## Examples
- **Inadequate Gas Handling**
    ```solidity
    pragma solidity ^0.8.0;

    contract InefficientProcessing {
        mapping(address => uint) public balances;

        function batchTransfer(address[] memory recipients, uint amount) public {
            for (uint i = 0; i < recipients.length; i++) {
                balances[recipients[i]] += amount; // Gas-intensive operation
            }
        }
    }
    ```

**Issue:** Processes large arrays in a single transaction, which can fail due to out-of-gas errors.

Why is this a problem?
- If recipients.length is too large, the transaction fails.
- Attackers can exploit this by submitting large recipient lists, causing a DoS attack.

- **Adequate Gas Handling**
    ```solidity
    pragma solidity ^0.8.0;

    contract GasOptimizedProcessing {
        mapping(address => uint) public balances;

        function batchTransfer(address[] memory recipients, uint amount) public {
            uint i = 0;
            while (i < recipients.length && gasleft() > 50000) { // Stop before out of gas
                balances[recipients[i]] += amount;
                i++;
            }
        }
    }
    ```
✔️ Fix: Uses gasleft() to gracefully exit before running out of gas, ensuring some transfers complete.
Why is this better?
✅ Prevents complete transaction failure by handling only as many iterations as gas allows.
✅ Reduces DoS risk by allowing partial execution instead of reverting everything.
✅ Enables retrying to complete all operations over multiple calls.

---