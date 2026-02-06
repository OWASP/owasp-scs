---
title: ERC4626 Share Inflation via Donations
id: SCWE-135
alias: erc4626-donation-inflation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-COMP]
  scsvs-scg: [SCSVS-COMP-1]
  cwe: [682]
status: new
---

## Relationships
- CWE-682: Incorrect Calculation  
  [https://cwe.mitre.org/data/definitions/682.html](https://cwe.mitre.org/data/definitions/682.html)

## Description
ERC4626 vaults that do not guard against free-asset donations can skew `totalAssets` and share price. Attackers can donate assets to inflate share value and then mint shares cheaply before normalization, extracting value from existing holders.

## Remediation
- Normalize share price on every deposit/mint using current `totalAssets`.
- Optionally block unsolicited donations by reverting on direct transfers or sweeping them into reserves before new share mints.
- Add tests for donation and price-per-share edge cases.

## Examples

### Vulnerable
```solidity
// totalAssets rises from donation; shares minted at stale price benefit attacker
function mint(uint256 shares) external {
    uint256 assets = previewMint(shares);
    asset.transferFrom(msg.sender, address(this), assets);
    _mint(msg.sender, shares);
}
```

### Fixed
```solidity
function mint(uint256 shares) external {
    uint256 assets = previewMint(shares); // uses up-to-date totalAssets
    asset.transferFrom(msg.sender, address(this), assets);
    _mint(msg.sender, shares);
}
// plus sweep or adjust for unsolicited donations before preview math
```

