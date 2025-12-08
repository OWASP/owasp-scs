---
title: Missing Payload Size Validation in Cross-Chain Messaging (Denial of Service/Stuck Funds)
id: SCWE-087
alias: Missing-Payload-Size-Validation-in-Cross-Chain-Messaging
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-BRIDGE]
  scsvs-scg: [SCSVS-BRIDGE-2]
  cwe: [1284]
status: new
---

## Relationships
- CWE-1284: Improper Validation of Specified Quantity in Input  
  [CWE-1284 Link](https://cwe.mitre.org/data/definitions/1284.html)
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description
This weakness arises when smart contracts performing cross-chain messaging fail to validate the size of payloads before emitting or sending them. In protocols using relayer-based messaging (e.g., LayerZero, Wormhole), data is typically encoded and emitted as a payload on the source chain, then relayed and decoded on the destination chain. If the encoded payload exceeds the maximum allowed size (often 10,000 bytes or similar, depending on the bridge/messaging protocol), the message transmission or decoding can revert—often because the large payload causes out-of-gas consumption during processing or fails explicit size checks. In lock-mint architectures, this can lead to permanent loss of user funds due to inability to unlock or mint assets on the destination chain.
## Impact
- **Denial of Service:** Oversized payloads will revert during cross-chain transmission, preventing legitimate state updates or token minting/unlocking on the destination chain.
- **Stuck or Lost Funds:** In bridges using lock-and-mint or burn-and-mint designs, users’ assets may be locked on the source chain with no way to release or claim them on the destination due to repeated transaction failure.
- **Operational Risk:** Malicious or unintentional submission of oversized payloads can be used to disrupt bridge operations, preventing protocol liveness or causing critical business logic to be inaccessible.
## Remediation
- Enforce maximum payload size validation on both source and destination chains.
- Perform defensive coding around payload encoding and decoding to catch out-of-gas or out-of-bound errors.
- Consider fallback or reversion handling strategies to safely refund or unlock funds when such failures occur.
## Examples
🧪  **Example: User-Supplied Merkle Proof in `lockTokens()`**

❌ **Vulnerable Code (No Payload Size Validation)**
```solidity
// SourceChain.sol
event Locked(address indexed user, uint256 amount, bytes payload);
function lockTokens(uint256 amount, bytes calldata merkleProof) external {
    require(amount > 0, "Invalid amount");
    // Lock tokens (ERC20 transferFrom)
    require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
    // Encode user, amount, timestamp, and the supplied Merkle proof
    bytes memory payload = abi.encode(msg.sender, amount, block.timestamp, merkleProof);
    // ⚠️ No payload size validation!
    emit Locked(msg.sender, amount, payload);
}
```
Destination Chain: Decode and Mint
```solidity
// DestinationChain.sol
function mintFromPayload(bytes calldata payload) external {
    // Will revert if payload is too large for decode!
    (address user, uint256 amount, uint256 timestamp, bytes memory merkleProof) =
        abi.decode(payload, (address, uint256, uint256, bytes));
    // Verification of Merkle proof, then mint tokens
    _mint(user, amount);
}
```
✅  Safe Code (With Payload Size Validation)
```solidity
// SourceChain.sol
event Locked(address indexed user, uint256 amount, bytes payload);
function lockTokens(uint256 amount, bytes calldata merkleProof) external {
    require(amount > 0, "Invalid amount");
    // Lock tokens (ERC20 transferFrom)
    require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");
    // Encode user, amount, timestamp, and the supplied Merkle proof
    bytes memory payload = abi.encode(msg.sender, amount, block.timestamp, merkleProof);
    // Check payload size
    require(payload.length <= 10_000, "Payload exceeds max allowed size");
    emit Locked(msg.sender, amount, payload);
}
```
Destination Chain: Decode and Mint (Optional Double Check)
```solidity
// DestinationChain.sol
function mintFromPayload(bytes calldata payload) external {
    require(payload.length <= 10_000, "Payload too large");
    (address user, uint256 amount, uint256 timestamp, bytes memory merkleProof) =
        abi.decode(payload, (address, uint256, uint256, bytes));
    // Proceed with Merkle proof verification and minting
    _mint(user, amount);
}

```