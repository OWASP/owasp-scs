---
id: SCSTG-TEST-0010
scsvs_cg_id:
- SCSVS-CODE
scsvs_scg_id:
- SCSVS-CODE-2
platform: []
title: Test Compiler Version and Deprecated Functions
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0010
---

### **Description**
Proper management of development policies, secure coding standards, code clarity, and test coverage ensures that smart contracts are secure, maintainable, and resilient to vulnerabilities. This test focuses on ensuring adherence to best practices and guidelines for developing and reviewing smart contracts. This includes the use of current compilers, avoiding deprecated functions, thorough code reviews, and ensuring proper test coverage. Code clarity is also critical for maintaining contracts over time and ensuring they remain understandable and auditable.

---

### **Test 1: Verify Compiler Version and Avoid Deprecated Functions**

#### Vulnerable Code:

```solidity
pragma solidity ^0.4.0;

contract Example {
    uint256 public value;

    function setValue(uint256 _value) public {
        value = _value;
    }
}
```
#### **Why It’s Vulnerable**
- The contract uses an outdated compiler version (^0.4.0). Using old versions of Solidity may lead to known security vulnerabilities and lack of support for modern features.
- Older compiler versions also lack optimizations and security fixes that are available in newer versions.

#### Fixed:

```solidity
pragma solidity ^0.8.0;  // Update to the latest stable version

contract Example {
    uint256 public value;

    function setValue(uint256 _value) public {
        value = _value;
    }
}
```
#### **How to Check**
- Code Review: Ensure that the pragma directive specifies an up-to-date version of Solidity (e.g., ^0.8.x) and not outdated ones such as ^0.4.x.
- Automated Check: Use Solidity linting tools or automated CI/CD pipelines to flag usage of outdated compiler versions.

---

### **Test 2: Ensure Code Review Processes and Avoid Deprecated Functions**

#### **Vulnerable Code:**

```solidity
pragma solidity ^0.4.24;

contract Token {
    string public name = "Token";
    uint public totalSupply = 1000000;

    // Deprecated function in Solidity 0.4.x
    function transfer(address recipient, uint amount) public {
        require(msg.sender != recipient, "Cannot transfer to yourself");
        require(amount <= totalSupply, "Amount exceeds total supply");

        totalSupply -= amount;
        // Deprecated: The transfer method below is obsolete
        recipient.transfer(amount);
    }
}

```

#### Why It’s Vulnerable
- The function transfer in the above example uses a deprecated `transfer()` method to send Ether to the recipient.
- The `transfer()` method was removed in Solidity 0.5.x, and it’s recommended to use `call()` instead to prevent errors due to changes in gas limits and transfer behavior in newer Solidity versions.
- Using deprecated functions can make your contract incompatible with future versions of Solidity and leave it vulnerable to unexpected behavior.

#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract Token {
    string public name = "Token";
    uint public totalSupply = 1000000;

    function transfer(address payable recipient, uint amount) public {
        require(msg.sender != recipient, "Cannot transfer to yourself");
        require(amount <= totalSupply, "Amount exceeds total supply");

        totalSupply -= amount;
        // Replaced deprecated transfer method with call to ensure proper handling
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Transfer failed");
    }
}

```

#### Why the Fix Works
- The updated code uses the `call()` method instead of the deprecated `transfer()` method to send Ether.
- The `call()` method is more flexible and is recommended in Solidity 0.5.x and later, as it allows specifying gas and properly handling errors.
- This change ensures that the contract is compatible with newer Solidity versions (>=0.5.x) and avoids potential issues with future upgrades.

#### How to Check
- Code Review: Ensure the contract is not using any deprecated or obsolete functions. Look for any `transfer()`, `send()`, or other outdated methods, and replace them with the more secure `call()` method when sending Ether.
- Static Analysis Tools: Use tools like SolidityScan, MythX, Slither, or linters to detect deprecated features and provide suggestions for updating the code.
- Testing: Test the contract using the latest Solidity version and verify that no deprecated functions are used, ensuring compatibility with newer compilers.
