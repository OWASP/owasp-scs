---
title: Price Oracle Manipulation
id: SCWE-028
alias: price-oracle-manipulation
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
Price Oracle manipulation refers to the exploitation of vulnerabilities in price oracles to manipulate contract logic. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data.
- Exploitation of the contract's logic.

## Remediation
- **Use decentralized oracles:** Leverage multiple decentralized oracles for price data.
- **Validate inputs:** Ensure all oracle data is properly validated before use.
- **Implement circuit breakers:** Add mechanisms to halt operations in case of suspicious activity.

## Examples
- **Vulnerable to Oracle Manipulation**- Exploiting Weak Price Feeds

- Flash Loan-Based Price Manipulation

    ```solidity
    pragma solidity ^0.8.0;

    interface Oracle {
        function getPrice() external view returns (uint);
    }

    contract VulnerableLending {
        Oracle public priceOracle;
        mapping(address => uint) public balances;

        constructor(address _oracle) {
            priceOracle = Oracle(_oracle);
        }

        function deposit() external payable {
            balances[msg.sender] += msg.value * priceOracle.getPrice();
        }

        function withdraw(uint amount) external {
            require(balances[msg.sender] >= amount, "Insufficient balance");
            balances[msg.sender] -= amount;
            (bool ok, ) = msg.sender.call{value: amount / priceOracle.getPrice()}(""); // Uses current price
            require(ok, "Transfer failed");
        }
    }
    ```

Why is this vulnerable?

- Flash loan attack: The attacker can manipulate the price before calling withdraw(), draining funds.
- No validation mechanism to reject manipulated prices.

- **Protected Against Oracle Manipulation** — Fixed Code: Price Deviation Guards

    ```solidity
    pragma solidity ^0.8.0;

    interface Oracle {
        function getPrice() external view returns (uint);
    }

    contract SecureLending {
        Oracle public priceOracle;
        mapping(address => uint) public balances;
        uint public lastValidPrice;

        constructor(address _oracle) {
            priceOracle = Oracle(_oracle);
            lastValidPrice = priceOracle.getPrice();
        }

        function updatePrice() external {
            uint newPrice = priceOracle.getPrice();
            require(newPrice > lastValidPrice * 95 / 100 && newPrice < lastValidPrice * 105 / 100, "Price deviation too high");
            lastValidPrice = newPrice;
        }

        function deposit() external payable {
            updatePrice(); // refresh price before use
            balances[msg.sender] += msg.value * lastValidPrice;
        }

        function withdraw(uint amount) external {
            updatePrice(); // refresh price before use
            require(balances[msg.sender] >= amount, "Insufficient balance");
            balances[msg.sender] -= amount;
            (bool ok, ) = msg.sender.call{value: amount / lastValidPrice}("");
            require(ok, "Transfer failed");
        }
    }
    ```

Fixes:
- Implements price deviation guards (5% max change) to reject manipulated or stale prices.
- Calls `updatePrice()` before deposit/withdraw to ensure `lastValidPrice` is current.
---