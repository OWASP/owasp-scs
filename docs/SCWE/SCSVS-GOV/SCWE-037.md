---
title: Insufficient Protection Against Front-Running
id: SCWE-037
alias: insufficient-protection-against-front-running
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-GOV]
  scsvs-scg: [SCSVS-GOV-3]
  cwe: [20]
status: new
---

## Relationships
- CWE-20: Improper Input Validation  
  [CWE-20 Link](https://cwe.mitre.org/data/definitions/20.html)

## Description  
Insufficient protection against front-running refers to vulnerabilities that allow malicious actors to exploit the order of transactions for profit. This can lead to:
- Unauthorized actions by malicious actors.
- Loss of funds or data.
- Exploitation of the contract’s logic.

## Remediation
- **Use commit-reveal schemes:** Implement commit-reveal mechanisms to hide transaction details until they are finalized.
- **Add delays:** Introduce time delays for critical operations to reduce the risk of front-running.
- **Test thoroughly:** Conduct extensive testing to ensure front-running protection is effective.

## Examples
- **Vulnerable to Front-Running**
    ```solidity
    pragma solidity ^0.8.0;

    interface IERC20 {
        function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
        function balanceOf(address account) external view returns (uint256);
    }

    contract FrontRunningVulnerable {
        IERC20 public token;
        uint256 public price = 1 ether; // 1 token = 1 ETH

        constructor(address _token) {
            token = IERC20(_token);
        }

        function buyTokens(uint256 amount) public payable {
            require(msg.value >= amount * price, "Insufficient ETH");
            token.transferFrom(address(this), msg.sender, amount);
        }
    }
    ```
Why is this vulnerable?
- Attackers see the transaction in the mempool and execute a transaction to buy first, raising the price.
- Victim's transaction executes at a higher price or fails due to slippage.
- Attacker sells at a profit, exploiting sandwich attacks.

- **Protected Against Front-Running-  Commit-Reveal to Hide Trade Intent**
    ```solidity
    pragma solidity ^0.8.0;

    contract SecureTrade {
        mapping(address => bytes32) public commitments;
        uint256 public price = 1 ether; // 1 token = 1 ETH

        function commitTrade(bytes32 hash) public {
            commitments[msg.sender] = hash;
        }

        function executeTrade(uint256 amount, bytes32 secret) public payable {
            require(commitments[msg.sender] == keccak256(abi.encodePacked(amount, secret)), "Invalid commitment");
            require(msg.value >= amount * price, "Insufficient ETH");
            
            commitments[msg.sender] = 0; // Prevent reusing commitment
            // Execute trade after revealing the commitment
        }
    }
    ```
Why is this better?
- Traders commit to the trade off-chain before revealing the amount, preventing mempool sniping.
- Transactions cannot be front-run because attackers don’t know the amount until revealed.
---