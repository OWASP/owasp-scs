---
title: Lack of Zero Value Check in Token Transfers
id: SCWE-091
alias: Lack-Zero-Value-Check-Token-Transfers
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [754]
status: new
---

## Relationships
- CWE-754: Improper Check for Unusual or Exceptional Conditions  
  [CWE-754 Link](https://cwe.mitre.org/data/definitions/754.html)

## Description  
This weakness occurs when smart contracts perform ERC20 token transfers without first validating that the transfer amount is greater than zero. While most ERC20 tokens allow zero‑value transfers, some implementations (e.g., LEND and others) revert when the amount is zero. This inconsistency can cause unexpected reverts in production, disrupt execution flow, and prevent critical contract logic from completing successfully.  
Common risks include:  
- Unexpected revert when interacting with non‑standard ERC20 tokens that disallow zero‑value operations.  
- Potential denial‑of‑service conditions if an attacker or integration repeatedly triggers zero‑value transfers.  
- Broken integrations when protocols assume uniform ERC20 behavior across diverse tokens.  

## Remediation  
- **Validate transfer amounts:** Ensure `amount > 0` before calling `transfer`/`transferFrom`.  
- **Treat zero as a no‑op if acceptable:** Early‑return when `amount == 0` rather than calling token methods.  
- **Use robust token wrappers:** Centralize token operations (e.g., via OpenZeppelin `SafeERC20`) and standardize zero‑value handling.  
- **Integration testing:** Include zero‑value cases for all integrated tokens (especially known non‑standard tokens like LEND).  
- **Input sanitization:** Validate and sanitize externally supplied amounts prior to token interactions.  

## Examples  
- **Vulnerable Code (No Zero Value Check)**  
    ```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.7.0;

    import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

    contract ExampleContract {
        using SafeERC20 for IERC20;
        IERC20 public inToken;
        address public vault;

        function transferTokens(uint256 feeTokenAmount) external {
            // No validation → may revert with some ERC20 tokens
            inToken.safeTransfer(vault, feeTokenAmount);
        }
    }
    ```

- **Safe Code (With Zero Value Check)**  
    ```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.7.0;

    import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

    contract ExampleContract {
        using SafeERC20 for IERC20;
        IERC20 public inToken;
        address public vault;

        function transferTokens(uint256 feeTokenAmount) external {
            require(feeTokenAmount > 0, "Amount must be greater than zero");
            inToken.safeTransfer(vault, feeTokenAmount);
        }
    }
    ```

- **Alternative Safe Pattern (No‑op on Zero)**  
    ```solidity
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.7.0;

    import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";

    contract ExampleContract {
        using SafeERC20 for IERC20;
        IERC20 public inToken;
        address public vault;

        function transferTokens(uint256 feeTokenAmount) external {
            if (feeTokenAmount == 0) {
                return; // Skip calling token methods to avoid non-standard reverts
            }
            inToken.safeTransfer(vault, feeTokenAmount);
        }
    }
    ```


