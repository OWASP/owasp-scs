---
title: Integer Overflows and Underflows
id: SCWE-047
alias: integer-overflows-underflows
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-CODE]
  scsvs-scg: [SCSVS-CODE-2]
  cwe: [190]
status: new
---

## Relationships
- CWE-190: Integer Overflow or Wraparound  
  [https://cwe.mitre.org/data/definitions/190.html](https://cwe.mitre.org/data/definitions/190.html)

## Description
Integer overflows and underflows occur when arithmetic operations exceed the bounds of the integer data type, causing the value to "wrap around" to an unexpected number.

## Remediation
- **Use Solidity 0.8.0 or later:** Leverage the compiler’s built-in overflow and underflow checks.  
- **Apply SafeMath libraries:** Use libraries like OpenZeppelin’s `SafeMath` for versions before 0.8.0.  

## Examples

### Vulnerable Contract Example

```solidity
pragma solidity ^0.4.0;

contract Vulnerable {
    uint8 public totalSupply;

    function addTokens(uint8 _value) public {
        totalSupply += _value; // May overflow
    }

    function subtractTokens(uint8 _value) public {
        totalSupply -= _value; // May underflow
    }
}
```
### Fixed Contract Example

```solidity
pragma solidity ^0.6.0;
import "@openzeppelin/contracts/math/SafeMath.sol";

contract Secure {
    using SafeMath for uint8;
    uint8 public totalSupply;

    function addTokens(uint8 _value) public {
        totalSupply = totalSupply.add(_value);
    }

    function subtractTokens(uint8 _value) public {
        totalSupply = totalSupply.sub(_value);
    }
}
```