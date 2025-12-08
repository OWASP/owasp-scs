---
title: Missing Validation of Oracle Response Fields (Stale or Incomplete Data)
id: SCWE-086
alias: missing-oracle-response-validation
platform: []
profiles: [L1]
mappings:
  scsvs-cg: [SCSVS-ORACLE]
  scsvs-scg: [SCSVS-ORACLE-1]
  cwe: [345]
status: new
---

## Relationships
- **CWE-345**: [Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- **CWE-20**:  [Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)

## Description
This weakness occurs when smart contracts consume data from oracles (e.g., Chainlink) without validating critical fields in the response such as `answeredInRound`, `timestamp`, or even the `answer` itself. Failing to validate these fields can lead to:

- Use of stale price data from old oracle rounds.
- Acceptance of incomplete oracle responses (e.g., `timestamp == 0`).
- Execution based on invalid or zero-priced data.

This can severely affect the security of DeFi protocols or any smart contract relying on accurate, fresh data feeds.

## Remediation
- **Validate `answer` field:** Ensure the value returned is greater than zero and not malformed.
- **Check `answeredInRound >= roundId`:** Confirms that the data is not from a stale round.
- **Verify `timestamp != 0`:** Ensures that the oracle actually returned a complete result.

Additional best practices include:
- Using fallback mechanisms or thresholds for deviation checks.
- Halting sensitive functions if oracle data is suspect or missing.

## Examples

- **❌ Vulnerable Code (No Response Validation)**  
    ```solidity
    (, int256 answer,,,) = AggregatorV3Interface(oracle).latestRoundData();
    require(uint256(answer) > 0, "Zero price"); // Minimal check only
    ```

- **✅ Secure Code (With Full Oracle Validation)**  
    ```solidity
    (uint80 roundID, int256 answer,, uint256 timestamp, uint80 answeredInRound) = 
        AggregatorV3Interface(oracle).latestRoundData();

    require(answer > 0, "Invalid price: <= 0");
    require(answeredInRound >= roundID, "Stale round data");
    require(timestamp != 0, "Incomplete oracle response");
    ```

## References
- [Chainlink Oracle Security Best Practices](https://docs.chain.link/data-feeds/security/)
