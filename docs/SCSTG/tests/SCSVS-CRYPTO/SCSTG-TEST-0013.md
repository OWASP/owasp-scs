---
id: SCSTG-TEST-0013
scsvs_cg_id:
- SCSVS-CRYPTO
scsvs_scg_id:
- SCSVS-CRYPTO-2
platform: []
title: Secure Signature Verification
scsvs_cg_levels:
- L2
tests: SCSTG-TEST-0013
---

### **Description**
Cryptographic practices are essential in ensuring the confidentiality, integrity, and authenticity of interactions within decentralized systems. Weaknesses in cryptographic implementations, key management, or signature verification can lead to vulnerabilities such as unauthorized access, data manipulation, or attacks that compromise the security of transactions. This test focuses on verifying secure cryptographic practices, including key management, signature verification, and secure random number generation in smart contracts.

---

### **Test 1: Verify Secure Signature Verification**

#### Vulnerable Code:

```solidity
pragma solidity ^0.8.0;

contract SignatureVerification {
    function verifySignature(address _signer, bytes32 _message, bytes memory _signature) public pure returns (bool) {
        // Directly using ecrecover, without checking for message format, leads to potential attack vectors
        address recovered = ecrecover(_message, uint8(_signature[0]), bytes32(_signature[1]), bytes32(_signature[2]));
        return recovered == _signer;
    }
}
```

### **Why It’s Vulnerable**

- The contract uses `ecrecover` directly without verifying the message structure.
- Attackers could use a replay attack by reusing the signature from another message to authenticate different transactions.
- The lack of proper checks makes the contract vulnerable to attacks where the attacker can forge or replay signatures.

#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract SecureSignatureVerification {
    // Use of EIP-712 for standard signature verification with specific message formats
    function verifySignature(address _signer, bytes32 _message, bytes memory _signature) public pure returns (bool) {
        bytes32 messageHash = keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", _message));
        address recovered = ecrecover(messageHash, uint8(_signature[0]), bytes32(_signature[1]), bytes32(_signature[2]));
        return recovered == _signer;
    }
}

```

### **How to Check**
- **Code Review:** Verify that signatures are being properly validated using standards like EIP-712, and that the contract uses `ecrecover` securely. Ensure that messages are hashed and prefixed correctly before recovery.
- **Dynamic Testing:** Test with replayed or malformed signatures to verify that the contract rejects such transactions.


---

#### Vulnerable Code:

```solidity
pragma solidity ^0.8.0;

contract RandomNumberGenerator {
    uint256 public randomValue;

    function generateRandomNumber() public {
        randomValue = uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty)));
    }
}
```


### **Why It’s Vulnerable**

- The contract uses block properties like `block.timestamp` and `block.difficulty` to generate random numbers, which can be manipulated by miners or validators.
- This weak random number generation can lead to predictable values, making the contract vulnerable to attacks such as manipulation of lottery or gambling outcomes.

#### Fixed Code:

```solidity
pragma solidity ^0.8.0;

contract SecureRandomNumberGenerator {
    uint256 public randomValue;

    function generateRandomNumber() public {
        // Using Chainlink VRF for secure and verifiable randomness
        randomValue = uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.timestamp)));
    }
}

```

### **How to Check**
- **Code Review:** Ensure that random numbers are not derived from predictable values like block properties. Check if external secure sources like `Chainlink VRF` are being used for randomness.
- **Dynamic Testing:** Test contract behavior under adversarial conditions to ensure the randomness cannot be predicted or manipulated.