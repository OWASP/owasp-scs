---
title: Misuse of Oracle Min/Max Price Band Without Validation
id: SCWE-085
alias: Misuse-of-Oracle-Min_Max-Price-Band-Without-Validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ORACLE]
  scsvs-scg: [SCSVS-ORACLE-1]
  cwe: [345]
status: new
---

## Relationships

- **CWE-345**: [Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- **CWE-20**:  [Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

---

## Description

This weakness occurs when smart contracts consume price oracle data (e.g., from Chainlink) without verifying whether the returned price falls within an expected or trusted range (e.g., `minPrice`/`maxPrice`). Oracles may return fallback floor or ceiling values when actual prices exceed internal limits or when the feed encounters data instability.

Failing to detect and reject such edge-case values can result in incorrect or exploitable logic paths in smart contracts. This weakness may allow attackers to:

- Trigger mispriced swaps or asset conversions.
- Exploit collateralization thresholds.
- Manipulate auction pricing or tiered reward structures.
- Influence governance systems based on price weightings.

These issues are especially dangerous during periods of high volatility or partial oracle outages, where fallback values may be automatically returned.

---

## Remediation

To mitigate this risk:

- Always verify that the oracle-provided price lies within an expected range.
- Check whether the returned value is a fallback boundary by comparing it against known `minPrice`/`maxPrice` values.
- Monitor and log unusual oracle values for off-chain alerts and incident response.

---

##  Example 

- Vulnerable contract 

```solidity
(int256 price,,,) = AggregatorV3Interface(oracle).latestRoundData();

// Uses price directly without checking for boundary values
uint256 tokenAmount = uint256(price) * userInput;
```
- Fixed Contract 

```solidity
(int256 price,,,) = AggregatorV3Interface(oracle).latestRoundData();

// Validate that the price is within trusted bounds
require(price > minPrice && price < maxPrice, "Price out of expected bounds");

uint256 tokenAmount = uint256(price) * userInput;
```
This ensures that the contract rejects unexpected oracle values that might be returned during errors or manipulation attempts.

## References
- **Chainlink Docs**: [Chainlink Price Feeds Documentation](https://docs.chain.link/data-feeds)
- **CWE-345**: [Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- **CWE-20**:  [Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
