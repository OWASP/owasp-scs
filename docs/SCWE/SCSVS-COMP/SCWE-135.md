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
// totalAssets() uses balanceOf; donations inflate it and skew share price
function mint(uint256 shares) external {
    uint256 assets = previewMint(shares);
    asset.transferFrom(msg.sender, address(this), assets);
    _mint(msg.sender, shares);
}
```

### Fixed
```solidity
uint256 private _accountedAssets; // internal balance; excludes direct transfers

function totalAssets() public view override returns (uint256) {
    return _accountedAssets; // donations do not affect share price
}

function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
    uint256 before = asset.balanceOf(address(this));
    shares = super.deposit(assets, receiver);
    _accountedAssets += (asset.balanceOf(address(this)) - before);
}

function withdraw(uint256 assets, address receiver, address owner) public override returns (uint256 shares) {
    shares = super.withdraw(assets, receiver, owner);
    _accountedAssets -= assets;
}
```

