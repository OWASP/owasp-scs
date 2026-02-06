---
title: Weak VRF Parameterization or Callback Validation
id: SCWE-115
alias: weak-vrf-validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-1]
  cwe: [330]
status: new
---

## Relationships
- CWE-330: Use of Insufficiently Random Values  
  [https://cwe.mitre.org/data/definitions/330.html](https://cwe.mitre.org/data/definitions/330.html)

## Description
Using VRF services without validating `requestId`, sender, or subscription can let attackers spoof fulfillments or drain subscription balances. Misconfigured key hashes, gas limits, or shared subscriptions can cause predictable failures and force fallback logic that leaks randomness.

## Remediation
- Bind VRF fulfillments to tracked `requestId` values and trusted coordinator addresses.
- Use dedicated subscriptions, appropriate key hashes, and sane callback gas limits.
- Revert on unexpected fulfillments and avoid using fallback pseudo-randomness.

## Examples

### Vulnerable
```solidity
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is VRFConsumerBaseV2 {
    uint256 public randomWord;

    function fulfillRandomWords(uint256, uint256[] memory words) internal override {
        randomWord = words[0]; // no requestId or sender validation
    }
}
```

### Fixed
```solidity
pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

contract Lottery is VRFConsumerBaseV2 {
    uint256 public pending;

    function request() external { pending = COORDINATOR.requestRandomWords(/* params */); }

    function fulfillRandomWords(uint256 requestId, uint256[] memory words) internal override {
        require(requestId == pending, "unknown request");
        pending = 0;
        // use words[0]...
    }
}
```

