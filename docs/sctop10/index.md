---
hide:
  - toc
search:
  exclude: true
---

# OWASP Smart Contract Top 10 : 2026

<a href="https://github.com/OWASP/www-project-smart-contract-top-10">:material-github: GitHub Repo</a> · <a href="https://owasp.org/www-project-smart-contract-top-10">:material-web: OWASP Project Page</a>

<img src="../assets/OWASP-2026-Smart-Contract.png" 
     align="right" 
     style="border-radius: 3px; margin: 0 0 1em 1em; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;" 
     width="550px" 
     height="400px">

The **OWASP Smart Contract Top 10** is a standard awareness document that aims to provide Web3 developers and security teams with insights into the top 10 vulnerabilities found in smart contracts.

- **Awareness**: Understand the most common and critical vulnerabilities affecting smart contracts.
- **Prevention**: Implement best practices to safeguard against these known issues.
- **Standard Compliance**: A reference to ensure secure development and assessment of smart contracts.

It serves as a reference to ensure that smart contracts are secured against the most critical weaknesses exploited or discovered in recent years. The **Smart Contract Top 10** can be used alongside other smart contract security projects to ensure comprehensive risk coverage.

> Note: The current **2026** Top 10 is **forward-looking**: its ordering and category definitions are derived from **security incidents and survey data collected during 2025**, and then used to forecast which risks are expected to be most significant in the upcoming year. In other words, 2025 breach and vulnerability data provides the empirical foundation, while the 2026 list reflects how those observations are projected into the near future.  
>  
> This ranking is intended to raise awareness among security researchers, auditors, developers, protocol owners, and the broader industry about the 10 most commonly occurring and impactful smart contract risks.

??? info "Open Call: 2026 Top 10 Survey"

    **Objective:** Collect structured, anonymised, real-world signals from the Web3 security community to inform re-ordering, emerging vulnerability classes, and gaps in the current 2025 list.

    **Target contributors:** Smart contract auditors, protocol security leads, L1/L2 infra teams, wallet/custody engineers, incident response, bug bounty, and red/blue team practitioners.

    **Action:** [Participate in the survey](https://forms.gle/1vCRSrjYvhUgBonr8) if you have 2025 experience.

<button class="scs-button" onclick="window.location.href='https://owasp.org/www-project-smart-contract-top-10/';"> Visit the Smart Contract Top 10</button>


### Behind the Rankings

The methodology, statistics, and data sources behind the 2026 ordering are documented in:

- [Ranking Methodology](methodology.md) — Elicitation model, aggregation formulas, computed statistics, and reasoning.
- [Data Sources](data-sources.md) — Practitioner survey, 2025 incident data, and external references.

## Changes

![OWASP 2025 to 2026 Mapping](../assets/Top10mapping2025-2026.png)

### 2026 Ranking

* SC01:2026 - [Access Control Vulnerabilities](SC01-AccessControlVulnerabilities.md)
* SC02:2026 - [Business Logic Vulnerabilities](SC02-BusinessLogicVulnerabilities.md)
* SC03:2026 - [Price Oracle Manipulation](SC03-PriceOracleManipulation.md)
* SC04:2026 - [Flash Loan–Facilitated Attacks](SC04-FlashLoanAttacks.md)
* SC05:2026 - [Lack of Input Validation](SC05-LackOfInputValidation.md)
* SC06:2026 - [Unchecked External Calls](SC06-UncheckedExternalCalls.md)
* SC07:2026 - [Arithmetic Errors](SC07-ArithmeticErrors.md)
* SC08:2026 - [Reentrancy Attacks](SC08-ReentrancyAttacks.md)
* SC09:2026 - [Integer Overflow and Underflow](SC09-IntegerOverflowUnderflow.md)
* SC10:2026 - [Proxy & Upgradeability Vulnerabilities](SC10-ProxyAndUpgradeabilityVulnerabilities.md)

### Overview

| Title | Description |
| -- | -- |
| SC01 - Access Control Vulnerabilities | Access control flaws allow unauthorized users or roles to invoke privileged functions or modify critical state, often leading to full protocol compromise when admin, governance, or upgrade paths are exposed. |
| SC02 - Business Logic Vulnerabilities | Design-level flaws in lending, AMM, reward, or governance logic that break intended economic or functional rules, enabling attackers to extract value even when low-level checks appear correct. |
| SC03 - Price Oracle Manipulation | Weak oracles and unsafe price integrations that let attackers skew reference prices, enabling under-collateralized borrowing, unfair liquidations, and mispriced swaps as part of larger exploit chains. |
| SC04 - Flash Loan–Facilitated Attacks | Attacks that use large, uncollateralized flash loans to magnify small bugs (in logic, pricing, or arithmetic) into large drains, by executing complex multi-step sequences in a single transaction. |
| SC05 - Lack of Input Validation | Missing or weak validation of user, admin, or cross-chain inputs that allows unsafe parameters to reach core logic, corrupting state, breaking assumptions, or enabling direct fund loss. |
| SC06 - Unchecked External Calls | Unsafe interactions with external contracts or addresses where failures, reverts, or callbacks are not safely handled, often enabling reentrancy or inconsistent state. |
| SC07 - Arithmetic Errors | Subtle bugs in integer math, scaling, and rounding; especially in share, interest, and AMM calculations; that can be repeatedly exploited to cause precision loss, or siphon value, particularly when paired with flash loans. |
| SC08 - Reentrancy Attacks | Situations where external calls can re-enter vulnerable functions before state is fully updated, allowing repeated withdrawals or state changes from outdated views of contract state. |
| SC09 - Integer Overflow and Underflow | Dangerous arithmetic on platforms or code paths without robust overflow checks, leading to wrapped values, broken invariants, and potential drains of liquidity or mis-accounting. |
| SC10 - Proxy & Upgradeability Vulnerabilities | Misconfigured or weakly governed proxy, initialization, and upgrade mechanisms that let attackers seize control of implementations or reinitialize critical state. |

### Honourable Mentions

These categories did not rank in the 2026 Top 10 but remain relevant and should be considered during design and audit:

- **Permit front-running & nonce DoS** — An attacker can front-run a `permit()` call to consume the user's nonce, causing the original deposit/stake transaction to revert. Affects protocols that compose permit within larger flows; no fallback approval path can cause permanent DoS. 
- **Front-Running & MEV** — Transaction ordering and sandwich attacks can extract value from users. Consider MEV protection (e.g., private mempools, commit–reveal) for sensitive flows.
- **Cross-chain MEV (Symbiosis, Aug–Oct 2025)** — Source-chain event leakage enabled sandwich attacks on the destination chain before transactions reached the mempool; attackers extracted $5.27M. Demonstrates cross-chain information asymmetry and MEV in bridged flows.
- **DoS & Griefing via Gas, Loops, and State Bloat** — Poorly bounded loops, attacker-controlled iteration, and unbounded state growth (e.g., ever-growing arrays/mappings) can make critical functions unaffordable or permanently unusable, enabling economic denial of service without direct fund theft.
- **Governance-Specific Attack Vectors** — Malicious or rushed proposals, flash-loan-amplified voting power, timelock bypasses, and weak quorum/threshold design can be abused to seize protocol control, drain treasuries, or disable safety mechanisms under the guise of governance.
- **Cryptographic & Signature-Scheme Vulnerabilities** — Ambiguous or non-standard signing flows (e.g., misuse of signature-related EIPs), replayable or cross-domain signatures, and incorrect domain separation can allow attackers to reuse approvals or authorizations beyond their intended scope.

### Beyond Smart Contracts: Alternate Top 15 Web3 Attack Vectors

Many of the largest losses in Web3 for the year 2025 stem from **off-chain and operational** threats rather than solely smart contract bugs: multisig manipulation/hijacking, supply chain attacks, drainer malware, fake interviews, phishing, and exchange breaches. The **Alternate Top 15** catalogues these non-smart-contract attack vectors.

![OWASP Web3 Attack Vectors Top 15 2026](../assets/alternateWA-top15.png)

<br>

<button class="scs-button" onclick="window.location.href='Web3-Attack-Vectors-Top15/';"> View Alternate Top 15 Attack Vectors</button>

### Data Sources

The 2026 Top 10 is anchored in **2025 smart contract incident data** and **practitioner input**, as detailed on the dedicated Data Sources page. In summary:

**Key 2025 incident insights (Smart Contract-only):**

- **Total protocols analysed:** 122 smart-contract incidents (deduplicated).
- **Total loss analysed:** ≈ **$905.4M** in 2025 smart-contract involved losses only.
- **Role in the ranking:** Validates and supports the 2026 Top 10 ordering.

### SolidityScan's Web3HackHub

![SolidityScan Web3HackHub 2025](../assets/solidityscan-web3hackhub2025.png)

<button class="scs-button" onclick="window.location.href='data-sources/';"> View Data Sources</button>

## Licensing

The OWASP Smart Contract Top 10 (2026) is licensed under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), the Creative Commons Attribution-ShareAlike 4.0 license. Some rights reserved.
