---
hide:
  - toc
search:
  exclude: true
---

# OWASP SCS Checklist

<div style="float: right; text-align: center; margin-left: 1.5em;">
  <img src="../assets/scs_checklist.png" style="border-radius: 3px; box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 12px;" width="250px" />
  <br>
  <a href="https://docs.google.com/spreadsheets/d/1W3-XeqbCQp7RHRJKVfllcL9VmzrErMad-biL2mwOChM/edit?usp=sharing" class="md-button scs-btn-sheets" target="_blank" rel="noreferrer" style="margin-top: 0.5em; display: inline-block;">Visit SCS Checklist (Google Sheets)</a>
</div>

The OWASP Smart Contract Security Checklist helps you verify compliance with SCSVS controls and SCSTG test cases.

- **Security Assessments / Pentests**: cover the standard attack surface and start exploring.
- **Standard Compliance**: includes SCSVS and SCSTG.
- **Learn & practice** smart contract security skills.
- **Bug Bounties**: step-by-step coverage of the attack surface.

<p style="margin-top: 1.5em; margin-bottom: 0.5em;">Track your audit progress in-browser: check items off, filter by status, export results.</p>

<a href="interactive" class="md-button scs-btn-interactive">Open Interactive Checklist</a>

---

## Using the Checklist in Security Audits

Use the checklist to structure engagements and ensure consistent coverage:

- **Scoping**: Filter by category (Architecture, Access Control, Oracle, etc.) to align with project scope.
- **Prioritization**: Focus on Critical and High severity items first; use the priority filter.
- **Progress tracking**: Mark items complete as you verify; export JSON/CSV for reports.
- **Gap analysis**: Compare coverage against SCSVS to identify missing or weak controls.

---

## What to Check During Audits

| Area | Key Checks |
|------|------------|
| **Architecture** | Upgrade mechanisms, proxy initialization, storage layout, privilege transfers |
| **Business Logic** | LTV/liquidation math, slippage, flash loan resistance, rounding, token donation attacks |
| **Access Control** | RBAC, modifiers, init functions, timelocks, arbitrary call prevention |
| **Oracles & Pricing** | TWAP vs spot, staleness, manipulation vectors, cross-chain consistency |
| **Integrations** | ERC20/4626 edge cases, fee-on-transfer, rebasing tokens, external call safety |

---

## Code Review Approach

- **Top-down**: Start with architecture and access control; trace privilege flows.
- **Entry points**: Map all external/public functions and their authorization paths.
- **State changes**: Track storage writes and cross-contract calls for reentrancy and ordering.
- **Math & precision**: Verify integer handling, decimal scaling, unchecked blocks.

---

## Protocol Layers to Focus On

| Layer | Focus |
|-------|-------|
| **Smart contracts** | Core logic, vaults, oracles, governance, upgrade paths |
| **Bridges & cross-chain** | Message validation, replay protection, sequencer assumptions |
| **Off-chain indexers / APIs** | Input validation, rate limits, authentication |
| **Frontends** | Wallet connection, transaction signing UX, error handling |

---

## Web2 & Web2.5 Components

When auditing full-stack dApps, also verify:

- **Backend APIs**: Auth (JWT/session), input sanitization, rate limiting, CORS.
- **RPC nodes / subgraphs**: Data integrity, caching, failure handling.
- **Signing flows**: Key storage, session management, approval flows.
- **Third-party SDKs**: Wallet connectors, price feeds, analytics—trust boundaries.

---

## Related Resources

- [SCSVS Controls](/SCSVS/) – Full verification standard
- [SCSTG Tests](/SCSTG/tests/) – Testing guide
- [SCWE Weaknesses](/SCWE/) – Weakness enumerations
