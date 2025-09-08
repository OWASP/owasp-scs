---
title: Insufficient Gas Limit Validation in LayerZero Message Sending
id: SCWE-094
alias: insufficient-gas-limit-validation-layerzero
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-2]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description
This weakness arises when a smart contract using LayerZero for cross-chain communication fails to validate the minimum gas limit in the adapter parameters. Attackers (or misconfigured clients) can specify an adapter params gas value that is too low for the destination chain execution. As a result, message processing reverts before reaching business logic or error-handling, and the message is recorded as a failed payload on the destination chain. Accumulating failed payloads can disrupt protocol liveness by blocking the cross-chain communication pathway until manual intervention is performed.

## Impact
- **Denial of Service:** Destination chain message execution reverts due to insufficient gas, preventing critical state changes or callbacks.
- **Message Backlog/Failed Payloads:** Messages accumulate in failed payload storage/queues, increasing operational burden.
- **Operational Risk:** Requires manual retries, clearing, or rescue flows to restore liveness; prolonged outages can impact user operations (e.g., bridging, synchronization, DeFi actions).

## Remediation
- **Validate minimum gas limit:** Decode LayerZero adapter parameters and enforce a protocol-defined minimum gas limit per message type.
- **Use safe defaults:** Provide default adapter params with adequate gas and reject user-supplied values below the threshold.
- **Granular minima:** If different message types have varying complexity, define per-endpoint or per-function minimum gas values.
- **Robust failure handling:** Implement operational procedures and tooling to safely retry or clear failed payloads without compromising security.

## Examples
🧪  Example

❌ Vulnerable Code (Lack of gas limit validation allows pathway blocking)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@layerzerolabs/solidity-examples/contracts/lzApp/NonblockingLzApp.sol";

contract VulnerableLzApp is NonblockingLzApp {
    constructor(address _endpoint) NonblockingLzApp(_endpoint) {}

    function sendMessage(uint16 _dstChainId, bytes calldata _payload, bytes calldata _adapterParams) external payable {
        // No validation on _adapterParams, attacker can specify low gas
        _lzSend(_dstChainId, _payload, payable(msg.sender), address(0), _adapterParams, msg.value);
    }
}
```

✅ Safe Code (Enforces minimum gas limit to prevent blocking)
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "@layerzerolabs/solidity-examples/contracts/lzApp/NonblockingLzApp.sol";

contract FixedLzApp is NonblockingLzApp {
    uint256 public constant MIN_GAS_LIMIT = 200000;

    constructor(address _endpoint) NonblockingLzApp(_endpoint) {}

    function sendMessage(uint16 _dstChainId, bytes calldata _payload, bytes calldata _adapterParams) external payable {
        require(_extractGasLimit(_adapterParams) >= MIN_GAS_LIMIT, "low gas");
        _lzSend(_dstChainId, _payload, payable(msg.sender), address(0), _adapterParams, msg.value);
    }

    function _extractGasLimit(bytes calldata _adapterParams) internal pure returns (uint256 gasLimit) {
        require(_adapterParams.length >= 34, "bad params");
        assembly { gasLimit := calldataload(add(_adapterParams.offset, 2)) }
    }
}
```


