---
title: Improper Decimal Normalization in Price-Based Calculations
id: SCWE-088
alias: Improper-Decimal-Normalization-in-Price-Based-Calculations
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ORACLE]
  scsvs-scg: [SCSVS-ORACLE-1]
  cwe: [682]
status: new
---

## Relationships
- **CWE-681**:  [Incorrect Conversion between Numeric Types](https://cwe.mitre.org/data/definitions/681.html)
- **CWE-682**:  [Incorrect Calculation](https://cwe.mitre.org/data/definitions/682.html)


## Description
This issue arises when smart contracts perform arithmetic involving token values and price feeds without properly aligning decimal places across different sources (e.g. ERC-20 tokens with varying decimals and Chainlink oracles with fixed 8-decimal prices). Failing to normalize decimals before calculations can lead to severely inflated or deflated results, causing users to be overcharged, underpaid, or otherwise economically exploited.

## Impact
Smart contracts often rely on cross-asset conversions, such as paying fees in tokens or using collateralization logic involving price feeds. Improper decimal handling in these calculations may:
- Lead to gross overcharging or underpayment.
- Introduce systemic financial imbalances in vaults or accounting logic.
- Enable economic exploits by arbitraging rounding errors or precision gaps.
- Remain undetected during tests if decimals coincidentally align.
This issue is especially critical when:
- ERC-20 tokens with non-18 decimals (e.g., USDC = 6) are involved.
- Chainlink oracles return 8-decimal fixed-point prices.
- Arithmetic mixes native ETH values (in 18 decimals) with token values or prices.
---
## Remediation
- Always normalize decimals across all involved assets and feeds.
- Use centralized utility functions for all price/token conversions.
- Add sanity checks to detect outlier results (e.g., revert if output is >1000x expected range).
- When possible, emit intermediate calculation steps for auditing.

## Examples

- **❌ Vulnerable Code (Missing Decimal Normalization)**
```solidity
// Assume ETH/USD = 3000e8 (8 decimals), Token/USD = 1e8, and token has 6 decimals
uint256 tokenAmount = (ethAmountInWei * ethPriceInUsd) / tokenPriceInUsd;
// Result is in 18-decimal scale, not adjusted for the 6-decimal USDC token
```

- **✅ Safe Code (With Proper Decimal Alignment)**
```solidity
uint8 tokenDecimals = IERC20(token).decimals();

uint256 rawAmount = (ethAmountInWei * ethPriceInUsd) / tokenPriceInUsd;
uint256 adjustedAmount = rawAmount / (10 ** (18 - tokenDecimals));
// Now 'adjustedAmount' is in correct units for the target token
```


## Realistic Exploit Example
Assumptions:

```solidity
Registrar fee = 0.01 ETH = 1e16 wei

ETH/USD price = 3000 * 1e8 = 300000000000

USDC/USD price = 1 * 1e8 = 100000000

USDC has 6 decimals

Faulty Calculation:

result = (1e16 * 300000000000) / 100000000 = 3e19
return result / 1e6 = 3e13 (30 trillion base units = 30 million USDC)
Expected:

0.01 ETH * $3,000 = $30
→ 30 * 1e6 = 30,000,000 USDC units

Overcharge:

Actual charged: 30,000,000 USDC
Expected: 30 USDC
Overcharge: 999,900x
```
---
