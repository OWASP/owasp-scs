---
title: Insecure Use of blockhash
id: SCWE-084
alias: insecure-use-of-blockhash
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CRYPTO]
  scsvs-scg: [SCSVS-CRYPTO-2]
  cwe: [20]
status: new
---

## Relationships  
- CWE-20: Improper Input Validation  
  [https://cwe.mitre.org/data/definitions/20.html](https://cwe.mitre.org/data/definitions/20.html)  

## Description
The `blockhash` function is often misused to generate randomness in smart contracts. However, `blockhash` is publicly available and can be influenced by miners, making it an unreliable and insecure source of randomness.

Attackers can manipulate `blockhash` by controlling which transactions are included in a block, reordering transactions, or discarding unfavorable blocks. This can lead to predictable random outcomes, allowing malicious actors to exploit lotteries, gaming, and other randomness-dependent mechanisms.

**Attack Scenarios**
- Lottery Manipulation: A miner can withhold or reorder transactions to ensure a favorable `blockhash` that lets them win.
- Game Exploitation: If a game outcome depends on `blockhash`, an attacker can predict future results and place bets accordingly.

## Remediation
Do not rely on `blockhash` for generating randomness. Use more secure and unpredictable sources of randomness, such as using Chainlink VRF or other trusted oracles.

### Vulnerable Contract Example
```solidity
// Vulnerable contract using blockhash for randomness
pragma solidity ^0.8.0;

contract InsecureRandomness {
    function getRandomNumber(uint256 _blockNumber) public view returns (uint256) {
        return uint256(blockhash(_blockNumber)); // Predictable randomness
    }
}
```
**Why is this insecure?**
- Miners control block production - They can reorder or discard blocks to manipulate `blockhash`.
- Predictability - Attackers can call this function for past block numbers, making randomness guessable.


### Fixed Contract Example- Secure Random Number Generation Using Chainlink VRF

```solidity
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract SecureLottery is VRFConsumerBase {
    address[] public players;
    bytes32 internal keyHash;
    uint256 internal fee;
    uint256 public randomResult;

    constructor()
        VRFConsumerBase(
            0x514910771AF9Ca656af840dff83E8264EcF986CA, // Chainlink VRF Coordinator
            0x514910771AF9Ca656af840dff83E8264EcF986CA // LINK Token address
        )
    {
        keyHash = 0x6c3699283bda56ad74f6b855546325b68d482e983852a617d11109b44b8aab01; 
        fee = 0.1 * 10**18; // 0.1 LINK (varies by network)
    }

    function enter() public payable {
        require(msg.value > 0.1 ether, "Minimum ETH required");
        players.push(msg.sender);
    }

    function requestRandomWinner() public returns (bytes32 requestId) {
        require(players.length > 0, "No players joined");
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK");
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        uint256 index = randomness % players.length;
        payable(players[index]).transfer(address(this).balance);
    }
}
```

**Why is this secure?**
- Uses `Chainlink VRF` (Verifiable Random Function), which provides unpredictable, tamper-proof randomness.
- Miners cannot manipulate the randomness as it is derived from a verifiable external source.
- Players cannot predict the outcome before participating.