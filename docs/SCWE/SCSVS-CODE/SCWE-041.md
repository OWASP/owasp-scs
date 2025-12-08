---
title: Unsafe Downcasting
id: SCWE-041
alias: unsafe-downcasting
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-1]
  cwe: [681]
status: new
---

## Relationships  
- **CWE-681: Incorrect Conversion between Numeric Types**  
  [https://cwe.mitre.org/data/definitions/681.html](https://cwe.mitre.org/data/definitions/681.html)  

## Description  
Unsafe downcasting occurs when a larger integer type is implicitly or explicitly converted to a smaller type, leading to precision loss, unintended value changes, or integer overflows. Solidity does not automatically check for overflow when performing explicit type conversions, making it possible to unintentionally truncate values.

## Remediation  
To prevent unsafe downcasting:  
- Always validate that the value fits within the target data type before casting.  
- Use safe mathematical libraries like OpenZeppelin's `SafeCast` to ensure proper conversions.  
- Avoid unnecessary downcasting unless explicitly needed for gas optimization.  

### Vulnerable Contract Example  
```solidity
contract UnsafeDowncasting {
    function truncateValue(uint256 largeNumber) public pure returns (uint8) {
        return uint8(largeNumber);  // ⚠️ Potential data loss if largeNumber > 255
    }
}
```

**Why is this vulnerable?**
- If `largeNumber > 255`, the higher bits will be truncated, resulting in unexpected values.
- No validation ensures that `largeNumber` fits within `uint8`, leading to silent failures.


### Fixed Contract Example

```solidity
import "@openzeppelin/contracts/utils/math/SafeCast.sol";

contract SafeDowncasting {
    using SafeCast for uint256;

    function safeTruncateValue(uint256 largeNumber) public pure returns (uint8) {
        return largeNumber.toUint8();  // ✅ Ensures safe conversion
    }
}
```
**Why is this safe?**

- Uses OpenZeppelin’s `SafeCast` library to enforce safe downcasting.
- If `largeNumber` exceeds `uint8` limits, the transaction will revert instead of silently truncating.
- Prevents unexpected behavior and potential security vulnerabilities.

**By properly handling type conversions, developers can avoid integer truncation issues and maintain data integrity in smart contracts.**
