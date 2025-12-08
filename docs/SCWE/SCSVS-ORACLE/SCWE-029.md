---
title: Lack of Decentralized Oracle Sources
id: SCWE-029
alias: lack-of-decentralized-oracle-sources
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ORACLE]
  scsvs-scg: [SCSVS-ORACLE-1]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
Lack of decentralized oracle sources refers to the reliance on a single oracle for critical data, which can be manipulated or compromised. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data.
- Exploitation of the contract's logic.

## Remediation
- **Use multiple oracles:** Leverage multiple decentralized oracles for critical data.
- **Validate inputs:** Ensure all oracle data is properly validated before use.
- **Implement fallback mechanisms:** Use fallback oracles in case of failure.

## Examples
- **Single Oracle Source/ Single Point of Failure**
    ```solidity
    pragma solidity ^0.8.0;

    interface Oracle {
        function getPrice() external view returns (uint);
    }

    contract SingleOracle {
        Oracle public priceOracle;

        constructor(address _oracle) {
            priceOracle = Oracle(_oracle);
        }

        function getPrice() public view returns (uint) {
            return priceOracle.getPrice(); // Single source of truth
        }
    }
    ```

Why is this vulnerable?
- If the oracle fails, is compromised, or is manipulated, the contract has no fallback.
- Attackers could hijack the single oracle and return malicious data.

- **Decentralized Oracle Sources- Using Multiple Oracles & Fallbacks**
    ```solidity
    pragma solidity ^0.8.0;

    interface Oracle {
        function getPrice() external view returns (uint);
    }

    contract MultiOracle {
        Oracle[] public priceOracles;

        constructor(address[] memory _oracles) {
            for (uint i = 0; i < _oracles.length; i++) {
                priceOracles.push(Oracle(_oracles[i]));
            }
        }

        function getPrice() public view returns (uint) {
            uint totalPrice = 0;
            for (uint i = 0; i < priceOracles.length; i++) {
                totalPrice += priceOracles[i].getPrice();
            }
            return totalPrice / priceOracles.length; // Averaging multiple oracles
        }
    }
    ```
Fixes:
- Uses multiple oracles and computes an average to prevent manipulation.
- If one oracle fails or gets compromised, the contract still functions correctly.

---