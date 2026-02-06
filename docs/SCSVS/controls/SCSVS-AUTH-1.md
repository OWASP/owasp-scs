# SCSVS-AUTH-1


## S4.1 Role-Based Access Control (RBAC)

### Control Objective
Implement role-based access control to manage permissions and ensure that only authorized users can access specific functions. This includes validating identities, applying the least privilege principle, and ensuring appropriate access controls are in place.

### S4.1.A Multi-Signature Schemes

| **SCSVS&nbsp;VR&nbsp;ID**          | Requirement                                                                 | L1 | L2 | L3 | SCWE |
| ------------ | --------------------------------------------------------------------------- | -- | -- | -- | --- |
| S4.1.A1      | Ensure that the visibility modifier for all functions is appropriate, preventing unnecessary exposure of internal functions. |    | ✓  | ✓  |     |

### S4.1.B Identity Verification

| **SCSVS&nbsp;VR&nbsp;ID**          | Requirement                                                                 | L1 | L2 | L3 | SCWE |
| ------------ | --------------------------------------------------------------------------- | -- | -- | -- | --- |
| S4.1.B1      | Validate that unexpected addresses do not result in unintended behaviors, particularly when these addresses refer to contracts within the same protocol. |    | ✓  | ✓  |     |
| S4.1.B2      | Verify that functions like ecrecover handle all potential null addresses properly to avoid vulnerabilities arising from unexpected ecrecover outputs. |    | ✓  | ✓  |     |

### S4.1.C Least Privilege Principle

| **SCSVS&nbsp;VR&nbsp;ID**          | Requirement                                                                 | L1 | L2 | L3 | SCWE |
| ------------ | --------------------------------------------------------------------------- | -- | -- | -- | --- |
| S4.1.C1      | Use msg.sender (not tx.origin) for authorization to avoid phishing via malicious intermediary contracts. Optionally, require(tx.origin == msg.sender) restricts callers to EOAs only — use only when EOA-only access is explicitly required. |    | ✓  | ✓  |     |
| S4.1.C2      | Certain addresses might be blocked or restricted from receiving tokens (e.g., LUSD). Ensure that address restrictions are properly managed and verified. |    | ✓  | ✓  |     |
| S4.1.C3      | Ensure that Guard’s hooks (e.g., checkTransaction(), checkAfterExecution()) are executed to enforce critical security checks. |    | ✓  | ✓  |     |
| S4.1.C4      | Ensure that access controls are implemented correctly to determine who can use certain functions, and avoid unauthorized changes or withdrawals. |    | ✓  | ✓  |     |

