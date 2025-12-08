---
id: SCSTG-TEST-0012
scsvs_cg_id:
- SCSVS-COMP
scsvs_scg_id:
- SCSVS-COMP-1
platform: []
title: Test Token Implementations (ERC20, ERC721, ERC1155)
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0012
---

### **Description**
Component-Specific Security focuses on ensuring that each specific component of a decentralized application (dApp) or smart contract ecosystem is securely implemented. This includes a wide range of areas such as token standards (ERC20, ERC721, ERC1155), NFTs, vaults, liquidity pools, and other components. Properly securing these components is essential to avoid vulnerabilities that can lead to funds being stolen, lost, or misused. This test will focus on validating the security considerations for the components listed in the controls, ensuring that each one is implemented securely and with the appropriate mechanisms to protect users and assets.

---

### **Test: Ensure Proper Token Implementation (ERC20, ERC721, ERC1155)**

#### **Vulnerable Code: **

```solidity
pragma solidity ^0.5.0;

contract SimpleERC20 {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    string public name = "Simple Token";
    string public symbol = "STK";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    // Unchecked approve function (vulnerable to approval race condition)
    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }
}
```

### **Why It’s Vulnerable**
- The `approve` function does not include a check for the current allowance before setting a new one, which could allow for the "approval race condition." This can result in a vulnerability where an attacker could bypass the allowance mechanism and transfer more tokens than intended.  
- This issue is a well-known vulnerability in ERC20 token implementations.


#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract SafeERC20 {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    
    string public name = "Safe Token";
    string public symbol = "STK";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    // Secure approve function to prevent race condition
    function approve(address spender, uint256 amount) public returns (bool) {
        require(amount == 0 || allowance[msg.sender][spender] == 0, "Approve: non-zero allowance");
        allowance[msg.sender][spender] = amount;
        return true;
    }
}
```

### **How to Check**
- **Code Review:** Look for the `approve` function in token contracts and ensure that it includes the necessary checks to prevent the race condition. The secure approach is to first set the allowance to zero before updating it to a new value, or to require that it is zero if being reset.
- **Static Analysis:** Use tools such as SolidityScan, MythX or Slither to check for the "approval race condition" and ensure the contract doesn't allow for this vulnerability.
- **Dynamic Testing:** Test token transfer functionality with edge cases where the allowance is set to non-zero values before calling `approve`. Verify that it works correctly and no unauthorized transfers are possible.
