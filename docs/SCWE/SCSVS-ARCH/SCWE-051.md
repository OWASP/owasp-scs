---
title: Improper Use of CREATE2 for Contract Deployment
id: SCWE-051
alias: improper-create2-deployment
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ARCH]
  scsvs-scg: [SCSVS-ARCH-2]
  cwe: [706]
status: new
---

## Relationships  
- **CWE-706: Use of Incorrectly-Resolved Name or Reference**  
  [https://cwe.mitre.org/data/definitions/706.html](https://cwe.mitre.org/data/definitions/706.html)  

## Description  
The `CREATE2` opcode allows for deterministic contract deployment, meaning the contract's address can be precomputed before deployment. However, improper handling of the salt parameter, constructor arguments, or contract bytecode can lead to vulnerabilities such as address predictability, re-deployment attacks, and malicious contract substitution. If an attacker can influence the salt or code, they may deploy a contract at a known address before the legitimate one, leading to security risks.

## Remediation  
To prevent misuse of `CREATE2`:  
- Use unpredictable and unique salt values (e.g., incorporating nonces, sender addresses, or randomness).  
- Ensure the deployed contract logic remains consistent to prevent re-deployment attacks.  
- Hash important contract parameters into the salt to prevent unintended address collisions.  

### Vulnerable Contract Example  
```solidity
contract Factory {
    function deploy(bytes32 salt, bytes memory bytecode) public {
        address deployed;
        assembly {
            deployed := create2(0, add(bytecode, 0x20), mload(bytecode), salt)
        }
    }
}
```

**Why is this vulnerable?**

- If `salt` is predictable (e.g., user-supplied or a static value), an attacker can precompute and front-run the deployment.
- The same contract address can be re-used by deploying different bytecode, leading to logic changes at a fixed address.
- No validation ensures that the deployed contract is safe or expected.

### Fixed Contract Example

```solidity
contract SecureFactory {
    function deploy(bytes32 salt, bytes memory bytecode) public returns (address) {
        require(bytecode.length > 0, "Bytecode cannot be empty");

        // Ensure the salt includes sender information to prevent front-running
        bytes32 secureSalt = keccak256(abi.encodePacked(msg.sender, salt));

        address deployed;
        assembly {
            deployed := create2(0, add(bytecode, 0x20), mload(bytecode), secureSalt)
        }

        require(deployed != address(0), "Deployment failed");
        return deployed;
    }
}
```

**Why is this safe?**
- Uses `keccak256(abi.encodePacked(msg.sender, salt))` to make the salt unique per sender.
- Ensures the contract bytecode is non-empty before deploying.
- Validates that the deployed contract is nonzero, ensuring a successful deployment.

**By securing CREATE2 deployments, developers can prevent predictable contract addresses, front-running risks, and contract replacement vulnerabilities.**

