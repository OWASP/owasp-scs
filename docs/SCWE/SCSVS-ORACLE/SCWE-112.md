---
title: Reliance on Low-Liquidity Spot Prices
id: SCWE-112
alias: low-liquidity-spot-price
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
Using a single on-chain DEX spot price from an illiquid pool lets attackers move the price with small trades or flash loans, then exploit inflated/deflated valuations for lending, liquidations, or swaps.

## Remediation
- Require minimum liquidity thresholds and sanity bounds before trusting a pool.
- Use robust oracles (Chainlink, TWAP, median of multiple feeds) instead of raw spot prices.
- Apply deviation checks against reference feeds and revert when deviation exceeds limits.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;

contract Lending {
    IUniswapV2Pair public pair;

    function getPrice() public view returns (uint256) {
        (uint112 r0, uint112 r1,) = pair.getReserves();
        return uint256(r1) * 1e18 / r0; // trusts small pool
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;

contract Lending {
    IAggregatorV3 public chainlink;

    function getPrice() public view returns (uint256) {
        (, int256 price,,,) = chainlink.latestRoundData();
        require(price > 0, "stale");
        return uint256(price);
    }
}
```

