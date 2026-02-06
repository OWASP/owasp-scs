---
title: Insufficient TWAP Window or Single Observation
id: SCWE-113
alias: insufficient-twap-window
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ORACLE]
  scsvs-scg: [SCSVS-ORACLE-2]
  cwe: [346]
status: new
---

## Relationships
- CWE-346: Origin Validation Error  
  [https://cwe.mitre.org/data/definitions/346.html](https://cwe.mitre.org/data/definitions/346.html)

## Description
TWAP oracles that use very short windows or a single cumulative observation can be manipulated within a block or a few trades. Attackers can swing the average price temporarily to borrow, liquidate, or mint at a favorable rate.

## Remediation
- Use sufficiently long averaging windows and multiple observations with minimum elapsed time.
- Enforce maximum per-block updates to prevent same-block manipulation.
- Cross-check TWAP output against external reference feeds or deviation thresholds.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract PriceFeed {
    IUniswapV2Pair public pair;

    function twap() external view returns (uint256) {
        (uint price0,,,) = pair.observe(0); // single short observation
        return price0;
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract PriceFeed {
    IUniswapV2Pair public pair;

    function twap() external view returns (uint256) {
        (uint price0,,) = pair.currentCumulativePrices();
        // ensure enough time elapsed between checkpoints
        // and use multiple observations before trusting
        return price0;
    }
}
```

