---
title: Chain Split Risks
id: SCWE-033
alias: chain-split-risks
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
Chain split risks refer to vulnerabilities that arise when a blockchain splits into multiple chains, such as during a hard fork. This can lead to:
- Confusion or inconsistencies in contract logic.
- Loss of funds or data.
- Exploitation of vulnerabilities in cross-chain operations.

## Remediation
- **Handle chain splits:** Implement logic to handle potential chain splits.
- **Use chain identifiers:** Include chain identifiers in cross-chain communications.
- **Test thoroughly:** Conduct extensive testing to ensure contract logic is robust.

## Examples
- **Vulnerable to Chain Splits**
    ```solidity
    pragma solidity ^0.8.0;

    contract ChainSplitVulnerable {
        function processTransaction(bytes memory data) public {
            // Process transaction without chain split handling
        }
    }
    ```

- **Protected Against Chain Splits**
    ```solidity
    pragma solidity ^0.8.0;

    contract ChainSplitProtected {
        uint public chainId;

        constructor(uint _chainId) {
            chainId = _chainId;
        }

        function processTransaction(bytes memory data, uint transactionChainId) public {
            require(transactionChainId == chainId, "Invalid chain ID");
            // Process transaction
        }
    }
    ```

---
