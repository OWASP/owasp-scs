---
title: Hardcoded Constants
id: SCWE-008
alias: hardcoded-constants
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [547]
status: new
---

## Relationships
- CWE-547: Use of Hard-coded, Security-relevant Constants
  [https://cwe.mitre.org/data/definitions/547.html](https://cwe.mitre.org/data/definitions/547.html)

## Description
Hardcoded constants refer to values that are embedded directly into the code and cannot be easily changed without modifying the code itself. These constants may include critical parameters, addresses, or settings that could be subject to change based on external factors or evolving needs. Hardcoding these values in the code introduces several issues:

- **Lack of flexibility**: Once the contract is deployed, these hardcoded values cannot be changed without deploying a new version, leading to inefficiency and reduced adaptability.
- **Security risks**: Hardcoded values may expose sensitive information or create vulnerabilities if they are not properly protected.
- **Upgrade challenges**: Contracts with hardcoded constants cannot easily evolve to support new functionality or parameters without requiring costly redeployment.

## Remediation
- **Use variables instead of constants**: Instead of hardcoding values, define them as variables that can be updated through administrative actions.
- **Implement upgradeable contract patterns**: Use proxy contracts or other patterns that support upgrades to allow flexibility in modifying constants.
- **External configuration**: Use off-chain storage for configuration values that can be updated without needing to deploy new contract versions.

## Examples

### Contract with Hardcoded Constants

```solidity
pragma solidity ^0.4.0;

contract HardcodedConstants {
    address public owner = 0x1234567890abcdef1234567890abcdef12345678; // Hardcoded address
    uint public maxSupply = 1000000; // Hardcoded supply limit

    function setOwner(address newOwner) public {
        owner = newOwner;
    }

    function setMaxSupply(uint newMaxSupply) public {
        maxSupply = newMaxSupply;
    }
}
```
In this example, the `owner` address and `maxSupply` are hardcoded values that cannot be changed without redeploying the contract. This reduces flexibility and creates potential security risks.


### Improved Contract with External Configuration
```solidity

pragma solidity ^0.4.0;

contract ConfigurableContract {
    address public owner;
    uint public maxSupply;

    constructor(address initialOwner, uint initialMaxSupply) public {
        owner = initialOwner;
        maxSupply = initialMaxSupply;
    }

    function setOwner(address newOwner) public {
        owner = newOwner;
    }

    function setMaxSupply(uint newMaxSupply) public {
        maxSupply = newMaxSupply;
    }
}
```

In this improved example, the `owner` address and `maxSupply` are configurable through the constructor, allowing for more flexibility without the need for redeployment.