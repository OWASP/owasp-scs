---
title: Lack of Modularity
id: SCWE-003
alias: lack-of-modularity
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [1047]
status: new
---

## Relationships
- CWE-1047: Modules with Circular Dependencies
  [https://cwe.mitre.org/data/definitions/1047.html](https://cwe.mitre.org/data/definitions/1047.html)

## Description
Lack of modularity refers to a design flaw where a system's components are not sufficiently separated into independent, reusable modules. This deficiency leads to tightly coupled code, making the system difficult to understand, maintain, and extend. In the context of smart contracts, this manifests as monolithic contracts where all functionalities are bundled together, increasing complexity and the potential for errors.

## Remediation
- **Modular Design:** Break down the contract into smaller, focused modules that handle specific responsibilities.
- **Use of Libraries:** Leverage existing, well-tested libraries to handle common functionalities, reducing the need for custom code.
- **Simplify Logic:** Avoid unnecessary complexity by streamlining the contract's logic and removing redundant code.
- **Regular Audits:** Conduct periodic code reviews and audits to identify and address areas of excessive complexity.

## Examples

### Example of Lack of Modularity:

```solidity
pragma solidity ^0.8.0;

contract TightlyCoupledContract {
    mapping(address => uint) public balances;
    mapping(address => mapping(address => uint)) public allowances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient funds");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function transfer(address to, uint amount) public {
        require(balances[msg.sender] >= amount, "Insufficient funds");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    function approve(address spender, uint amount) public {
        allowances[msg.sender][spender] = amount;
    }

    function transferFrom(address from, address to, uint amount) public {
        require(allowances[from][msg.sender] >= amount, "Allowance exceeded");
        allowances[from][msg.sender] -= amount;
        balances[from] -= amount;
        balances[to] += amount;
    }
}
```

**Problem:** Instead of separating concerns into independent, reusable modules, everything is handled within one contract.

Why is this lack of modularity?

- Single contract handling multiple responsibilities (balance management, approvals, transfers).
- Code is not reusable: If another contract needs balance functions, it must copy-paste this logic.
- Testing is harder: Changing transfer() might break withdraw(), as they're tightly coupled.

### Refactored with Modular Design:

```solidity
pragma solidity ^0.8.0;

library BalanceLibrary {
    struct Data {
        mapping(address => uint) balances;
    }

    function deposit(Data storage self, address user, uint amount) internal {
        self.balances[user] += amount;
    }

    function withdraw(Data storage self, address user, uint amount) internal {
        require(self.balances[user] >= amount, "Insufficient funds");
        self.balances[user] -= amount;
        payable(user).transfer(amount);
    }
}

library AllowanceLibrary {
    struct Data {
        mapping(address => mapping(address => uint)) allowances;
    }

    function approve(Data storage self, address owner, address spender, uint amount) internal {
        self.allowances[owner][spender] = amount;
    }

    function transferFrom(
        Data storage self,
        BalanceLibrary.Data storage balances,
        address from,
        address to,
        uint amount
    ) internal {
        require(self.allowances[from][msg.sender] >= amount, "Allowance exceeded");
        require(balances.balances[from] >= amount, "Insufficient funds");

        self.allowances[from][msg.sender] -= amount;
        balances.balances[from] -= amount;
        balances.balances[to] += amount;
    }
}

contract ModularContract {
    using BalanceLibrary for BalanceLibrary.Data;
    using AllowanceLibrary for AllowanceLibrary.Data;

    BalanceLibrary.Data private balances;
    AllowanceLibrary.Data private allowances;

    function deposit() public payable {
        balances.deposit(msg.sender, msg.value);
    }

    function withdraw(uint amount) public {
        balances.withdraw(msg.sender, amount);
    }

    function approve(address spender, uint amount) public {
        allowances.approve(msg.sender, spender, amount);
    }

    function transferFrom(address from, address to, uint amount) public {
        allowances.transferFrom(balances, from, to, amount);
    }
}

```

**Solution:** Use libraries for shared functionality and separate contract concerns. Now, storage is separated, reusable libraries are used, and responsibilities are divided!
