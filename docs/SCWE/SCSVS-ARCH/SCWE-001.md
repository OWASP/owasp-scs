---
title: Improper Contract Architecture
id: SCWE-001
alias: improper-contract
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-1]
  cwe: [709]
status: new
---

## Relationships
- CWE-1008: Architectural Concepts
  [https://cwe.mitre.org/data/definitions/1008.html](https://cwe.mitre.org/data/definitions/1008.html)

## Description
Improper contract architecture refers to the flawed design of a smart contract’s structure, which compromises its security, scalability, and maintainability. This often occurs due to monolithic designs, inefficient inheritance structures, and poor separation of concerns. Such flaws create challenges in managing, upgrading, and auditing the contract. Key issues associated with improper architecture include:

- Difficulty in upgrading the contract without introducing risks.
- Increased complexity leading to hidden attack surfaces.
- Lack of flexibility in contract logic, making it hard to isolate bugs or exploits.

## Remediation
- **Modular design:** Break down contracts into smaller, more manageable modules to ensure a clean separation of concerns.
- **Proxy pattern implementation:** Use proxies to allow contract upgrades while preserving contract state.
- **Separate logic and state:** Keep business logic and data storage separate to improve scalability and maintainability.
- **Periodic code review and refactoring:** Regularly assess the architecture and refactor to maintain efficiency and security.

## Samples

### Improper Contract Architecture

```solidity
pragma solidity ^0.4.0;

contract MonolithicContract {
    uint public balance;

    function deposit() public {
        // Logic for deposit
    }

    function withdraw() public {
        // Logic for withdrawal
    }

    function transfer() public {
        // Logic for transfer
    }
}
```

### Improved Modular Contract Architecture

```solidity
pragma solidity ^0.4.0;

contract Deposit {
    uint public balance;

    function deposit() public {
        // Logic for deposit
    }
}

contract Withdraw {
    uint public balance;

    function withdraw() public {
        // Logic for withdrawal
    }
}

contract Transfer {
    uint public balance;

    function transfer() public {
        // Logic for transfer
    }
}
```